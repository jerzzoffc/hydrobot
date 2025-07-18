from config import CMD_HELP, bot_username, nama_bot
from Userbot import nlx
from Userbot.helper.database import dB
from Userbot.helper.tools import Emojik, h_s, zb

from .graph import upload_media

MODULES = "Group"


def help_string(org):
    return h_s(org, "help_grup")

@zb.ubot("help|menu|moire")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    query = c.get_arg(m)
    if not query:
        try:
            x = await c.get_inline_bot_results(bot_username, "help")
            await c.send_inline_bot_result(
                m.chat.id,
                x.query_id,
                x.results[0].id
            )
            # (Opsional) Hapus pesan .help agar chat lebih bersih
            # await m.delete()
            return
        except Exception as error:
            return await m.reply(f"{em.gagal}Error: {error}")
    else:
        if query == "pic":
            value = await upload_media(m)
            dB.set_var(c.me.id, "HELP_PIC", value)
            return await m.reply(f"{em.sukses}Done set help pic")
        elif query == "reset":
            dB.remove_var(c.me.id, "HELP_PIC")
            return await m.reply(f"{em.sukses}Done remove help pic")
        else:
            if query in CMD_HELP:
                prefix = c.get_prefix(c.me.id)
                return await m.reply(
                    f"{CMD_HELP[query].help_string(c.me.id).format(next((p) for p in prefix))}"
                    + f"<b>🤖 Moire-Userbot </b>"
                )
            else:
                return await m.reply(
                    f"{em.gagal}<b>Tidak ada modul bernama <code>{query}</code></b>"
                )