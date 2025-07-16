import re
from math import ceil
from typing import List

from pyrogram.helpers import ikb, kb
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            InlineQueryResultArticle, InputTextMessageContent)
from pytz import timezone

from config import bot_id, bot_username, nama_bot, the_cegers
from Userbot import bot, nlx

from ..database import dB

COLUMN_SIZE = 4  # Controls the button number of height
NUM_COLUMNS = 2  # Controls the button number of width

def pingx_button(user_id: int):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🏓 Ping Now", callback_data=f"pingx_now_{user_id}"
                )
            ]
        ]
    )
  
class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text

def paginate_modules(page_n, module_dict, prefix, chat=None):
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULES__,
                    callback_data="{}_module({},{})".format(
                        prefix, x.__MODULES__.lower(), page_n
                    ),
                )
                for x in module_dict.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULES__,
                    callback_data="{}_module({},{},{})".format(
                        prefix, chat, x.__MODULES__.lower(), page_n
                    ),
                )
                for x in module_dict.values()
            ]
        )

    pairs = [modules[i : i + NUM_COLUMNS] for i in range(0, len(modules), NUM_COLUMNS)]

    max_num_pages = ceil(len(pairs) / COLUMN_SIZE) if len(pairs) > 0 else 1
    modulo_page = page_n % max_num_pages

    keyboard = []

    if len(pairs) > COLUMN_SIZE:
        page_pairs = pairs[modulo_page * COLUMN_SIZE : COLUMN_SIZE * (modulo_page + 1)]
        keyboard.extend(page_pairs)
        keyboard.append([
            EqInlineKeyboardButton(
                "\u2cfb",  # ◻ Tombol kiri/prev
                callback_data="{}_prev({})".format(
                    prefix,
                    modulo_page - 1 if modulo_page > 0 else max_num_pages - 1,
                ),
            ),
            EqInlineKeyboardButton(
                f"{modulo_page + 1} / {max_num_pages}",  # Jumlah halaman
                callback_data="ignore"  # Agar tidak error jika ditekan
            ),
            EqInlineKeyboardButton(
                "\u2cfa",  # ◺ Tombol kanan/next
                callback_data="{}_next({})".format(prefix, modulo_page + 1),
            ),
        ])
    else:
        keyboard.extend(pairs)
        keyboard.append([
            EqInlineKeyboardButton(
                "\ud81a\udc68",  # Icon back (atau ganti sesuai style Anda)
                callback_data="{}_help_back({})".format(prefix, 0),
            ),
            EqInlineKeyboardButton("\u274c", callback_data="close"),
        ])
      
    return keyboard

def is_url(text):
    regex = r"(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:[/?]\S+)?|tg://\S+"
    matches = re.findall(regex, text)
    if matches:
        return True
    return False

def is_angka(text):
    try:
        int(text)
        return True
    except ValueError:
        return False

def is_copy(text: str):
    pattern = r"copy:"

    return bool(re.search(pattern, text))

def cek_tg(text):

    tg_pattern = r"https?:\/\/files\.catbox\.moe\/\S+"
    match = re.search(tg_pattern, text)

    if match:
        tg_link = match.group(0)
        non_tg_text = text.replace(tg_link, "").strip()
        return tg_link, non_tg_text
    else:
        return (None, text)

def get_msg_button(texts: str):
    btn = []
    for z in re.findall(r"\[(.*?)\|(.*?)\]", texts):
        text, url = z
        urls = url.split("|")
        url = urls[0]
        if len(urls) > 1:
            btn[-1].append([text, url])
        else:
            btn.append([[text, url]])

    txt = texts
    for z in re.findall(r"\[.+?\|.+?\]", texts):
        txt = txt.replace(z, "")

    return txt.strip(), btn

def create_button(text: str, data: str, with_suffix: str = "") -> InlineKeyboardButton:
    data = data.strip()
    if is_url(data):
        return InlineKeyboardButton(text=text, url=data)
    elif is_angka(data):
        return InlineKeyboardButton(text=text, user_id=int(data))
    elif is_copy(data):
        return InlineKeyboardButton(text=text, copy_text=data.replace("copy:", ""))
    return InlineKeyboardButton(
        text=text, callback_data=f"{data}_{with_suffix}" if with_suffix else data
    )

def create_inline_keyboard(
    buttons: List[List], suffix: str = ""
) -> InlineKeyboardMarkup:
    keyboard = []
    for row in buttons:
        if len(row) > 1:
            keyboard.append([create_button(text, data, suffix) for text, data in row])
        else:
            text, data = row[0]
            keyboard.append([create_button(text, data, suffix)])
    return InlineKeyboardMarkup(keyboard)

class Button:
    def deak(user_id, count):
        button = ikb(
            [
                [
                    ("⬅️ Kembali ", f"prev_ub {int(count)}"),
                    ("Setujui ✅", f"deak_akun {int(count)}"),
                ]
            ]
        )
        pass

    def expired():
        button = ikb([[(f"{nama_bot}", f"https://t.me/{bot.me.username}", "url")]])
        pass

class Button:
    @staticmethod
    def start(message):
        # PATCH: Tambah baris Loyalty Point di atas semua button.
        if message.from_user.id not in the_cegers:
            button = kb(
                [
                    [("✨ Loyalty Point")],  # Loyalty Point baris atas
                    [("🤖 Buat Userbot"), ("⚙️ Status Akun")],
                    [("🛠️ Cek Fitur"), (f"🇲🇨 Bahasa")],
                    [("🆘 Dukungan")],
                    [("🔄 Reset Emoji"), ("🔄 Reset Prefix")],
                    [("🔄 Restart Userbot"), ("🔄 Reset Text")],
                ],
                resize_keyboard=True,
                one_time_keyboard=True,
            )
        else:
            button = kb(
                [
                    [("✨ Loyalty Point")],  # Loyalty Point baris atas
                    [("🤖 Buat Userbot"), ("⚙️ Status Akun")],
                    [("🔄 Reset Emoji"), ("🔄 Reset Prefix")],
                    [("🔄 Restart Userbot"), ("🔄 Reset Text")],
                    [("🚀 Updates"), ("👥 Cek User"), ("🛠️ Cek Fitur")],
                    [(f"🇲🇨 Bahasa")],
                ],
                resize_keyboard=True,
                one_time_keyboard=True,
            )
        return button
    #refferal
    @staticmethod
    def referral_menu(ref_code=None):
        btns = [
            [("Claim Referral", "referral_claim")],
            [("Lewati", "referral_skip")]
        ]
        if ref_code:
            btns.append([("Salin Kode", f"copy:{ref_code}")])
        btns.append([("Referral Menu", "referral_menu")])  # Ganti Kembali dengan Referral Menu
        return ikb(btns)

    @staticmethod
    def referral_claim_back():
        # Hanya tombol Referral Menu, TIDAK ADA tombol kembali!
        return ikb([[("Referral Menu", "referral_menu")]])
      
    @staticmethod
    def loyalty_menu():
        # Inline keyboard: judul, lalu 2x2 tombol loyalty point, lalu kembali
        return ikb([
            [("Menu Loyalty Point :", "loyalty_label")],
            [("MyPoint", "loyalty_mypoint"), ("Claim Reward", "loyalty_claim")],
            [("Leaderboard", "loyalty_leaderboard")],
        ])

    @staticmethod
    def loyalty_back():
        return ikb([
            [("Kembali ke Menu Loyalty", "loyalty_menu")]
        ])

    def userbot(user_id, count):
        button = ikb(
            [
                [
                    (
                        "Hapus Dari Database",
                        f"del_ubot {int(user_id)}",
                    )
                ],
                [
                    (
                        "Cek Nomor",
                        f"get_phone {int(count)}",
                    )
                ],
                [
                    (
                        "Cek Kadaluarsa",
                        f"cek_masa_aktif {int(user_id)}",
                    )
                ],
                [
                    (
                        "Cek Otp",
                        f"get_otp {int(count)}",
                    )
                ],
                [
                    (
                        "Cek Verifikasi 2L",
                        f"get_faktor {int(count)}",
                    )
                ],
                [
                    ("❮", f"prev_ub {int(count)}"),
                    ("❯", f"next_ub {int(count)}"),
                ],
                [
                    ("Tutup", f"close_mbot"),
                ],
            ]
        )
        return button


def Ads():
    txt = dB.get_var(bot_id, "ads")
    if txt:
        msg = txt
    else:
        msg = "\n<b><u>[List VPS](https://t.me/moire_market/5)</u></b>"
    return msg
 
class MSG:
    def EXPIRED_MSG_BOT(X):
        return f"""
<b>❏ Notifikasi</b>
<b>├ Akun :</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>├ ID:</b> <code>{X.me.id}</code>
<b>╰ Masa Aktif Telah Habis</b>
"""

    def START(message):
        msg = f"""
<b><blockquote>📢 Halo! <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a></b>
<b><u>[{nama_bot}](https://t.me/{bot.me.username})</u> siap bantu kamu bikin Userbot Telegram dengan fitur lengkap, multi bahasa dan bonus menarik!.</blockquote></b>
<b><blockquote>⭐️ Loyalty Point:</b>
Setiap kali kamu memperpanjang masa aktif userbot, kamu akan mendapatkan loyalty point.
Kumpulkan point dan tukarkan otomatis untuk memperpanjang masa aktif secara gratis!</blockquote>
<b><blockquote>🤝 Referral Code:</b>
Bagikan kode referral ke temanmu.
Saat temanmu menggunakan kode tersebut, kamu langsung dapat bonus loyalty point!</blockquote>
<b><blockquote>📋 Syarat dan ketentuan akun telegram!.</b>
<b><u>[BACA DISINI](https://telegra.ph/RESIKO-USERBOT-03-26-3)</u> ketentuanya!.</u></b>
<b>Ads: {Ads()}</b></blockquote>
"""
        return msg

    def USERBOT(count):
        expired_date = dB.get_expired_date(nlx._ubot[int(count)].me.id)
        expir = expired_date.astimezone(timezone("Asia/Jakarta")).strftime(
            "%Y-%m-%d %H:%M"
        )
        return f"""
<b>❏ Userbot ke </b> <code>{int(count) + 1}/{len(nlx._ubot)}</code>
<b> ├ Akun:</b> <a href=tg://user?id={nlx._ubot[int(count)].me.id}>{nlx._ubot[int(count)].me.first_name} {nlx._ubot[int(count)].me.last_name or ''}</a> 
<b> ├ ID:</b> <code>{nlx._ubot[int(count)].me.id}</code>
<b> ╰ Expired</b> <code>{expir}</code>
"""

    def POLICY():
        return f"""
<blockquote><u><b>🤖 {nama_bot} </b></u></blockquote>
<blockquote><u><b>↪️ Kebijakan Pengembalian</b></u>
Setelah melakukan pembayaran, jika Anda belum memperoleh/menerima manfaat dari pembelian, Anda dapat menggunakan hak penggantian dalam waktu 2 hari setelah pembelian. Namun, jika Anda telah menggunakan/menerima salah satu manfaat dari pembelian, termasuk akses ke fitur pembuatan userbot, maka Anda tidak lagi berhak atas pengembalian dana.</blockquote>
<blockquote><u><b>🆘 Dukungan</b></u>
Untuk mendapatkan dukungan, Anda dapat:
❍ Mengikuti prosedur pembelian dibot ini
❍ Resiko userbot bisa [Baca Disini](https://telegra.ph/RESIKO-USERBOT-03-26-3)
❍ Beli Userbot = SETUJU DAN PAHAM RESIKO</blockquote>
<blockquote><b><u>👉🏻 Tekan tombol 📃 Saya Setuju</u></b> untuk menyatakan bahwa Anda telah
membaca dan menerima ketentuan ini dan melanjutkan
pembelian. <b><u>Jika tidak, tekan tombol 🏠 Menu Utama.</u></b>
<b>Ads: {Ads()}</b></blockquote>
"""


class INLINE:
    def query(func):
        async def wrapper(client, iq, *args):
            users = nlx._my_id
            if iq.from_user.id not in users:
                return await client.answer_inline_query(
                    iq.id,
                    cache_time=0,
                    results=[
                        (
                            InlineQueryResultArticle(
                                title=f"Anda Belum Melakukan Pembelian {bot_username}",
                                input_message_content=InputTextMessageContent(
                                    f"Kamu Bisa Melakukan Pembelian {bot_username} Agar Bisa Menggunakan"
                                ),
                            )
                        )
                    ],
                )
            else:

                return await func(client, iq, *args)

        return wrapper

    def data(func):
        async def wrapper(client, cq, *args):
            users = nlx._my_id
            if cq.from_user.id not in users:
                return await cq.answer(
                    f"Silakan Order Bot {bot_username} Agar Bisa Menggunakan Bot Ini",
                    True,
                )
            else:

                return await func(client, cq, *args)

        return wrapper
