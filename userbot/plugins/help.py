from telethon import functions

from userbot import catub

from ..Config import Config
from ..core import CMD_INFO, GRP_INFO, PLG_INFO
from ..core.managers import edit_or_reply

cmdprefix = Config.COMMAND_HAND_LER

plugin_category = "tools"


def get_key(val):
    for key, value in PLG_INFO.items():
        for cmd in value:
            if val == cmd:
                return key
    return None


def getkey(val):
    for key, value in GRP_INFO.items():
        for plugin in value:
            if val == plugin:
                return key
    return None


async def cmdinfo(input_str, event, plugin=False):
    if input_str[0] == cmdprefix:
        input_str = input_str[1:]
    try:
        about = CMD_INFO[input_str]
    except KeyError:
        if plugin:
            await edit_delete(
                event,
                f"**There is no plugin or command as **`{input_str}`** in your bot.**",
            )
            return None
        await edit_delete(
            event, f"**There is no command as **`{input_str}`** in your bot.**"
        )
        return None
    except Exception as e:
        await edit_delete(event, f"**Error**\n`{str(e)}`")
        return None
    outstr = f"**Command :** `{cmdprefix}{input_str}`\n"
    plugin = get_key(input_str)
    if plugin is not None:
        outstr += f"**Plugin :** `{plugin}`\n"
        category = getkey(plugin)
        if category is not None:
            outstr += f"**Category :** `{category}`\n\n"
    outstr += f"**Intro**\n{about[0]}"
    return outstr


async def plugininfo(input_str, event):
    try:
        cmds = PLG_INFO[input_str]
    except KeyError:
        outstr = await cmdinfo(input_str, event, plugin=True)
        return outstr
    except Exception as e:
        await edit_delete(event, f"**Error**\n`{str(e)}`")
        return None
    outstr = f"**Plugin : **`{input_str}`\n"
    outstr += f"**Commands Available :** `{len(cmds)}`\n"
    category = getkey(input_str)
    if category is not None:
        outstr += f"**Category :** `{category}`\n\n"
    for cmd in cmds:
        outstr += f"•  **cmd :** `{cmdprefix}{cmd}`\n"
        try:
            outstr += f"•  **info :** `{CMD_INFO[cmd][1]}`\n\n"
        except IndexError:
            outstr += f"•  **info :** `None`\n\n"
    outstr += f"**Usage : ** `{cmdprefix}help <command name>`\
        \n**Note : **If command name is same as plugin name then use this `{cmdprefix}help -c <command name>`."
    return outstr


async def grpinfo():
    outstr = "**Plugins in Catuserbot are:**\n\n"
    category = ["admin", "bot", "extra", "fun", "misc", "tools", "utils"]
    for cat in category:
        outstr += f"**•  Category : **`{cat}`\n"
        plugins = GRP_INFO[cat]
        for plugin in plugins:
            outstr += f"`{plugin}`  "
        outstr += "\n\n"
    outstr += f"**Usage : ** `{cmdprefix}help <plugin name>`"
    return outstr


@catub.cat_cmd(
    pattern="help ?(-c)? ?(\.*)?",
    command=("help", plugin_category),
    info={
        "header": "To get guide for catuserbot.",
        "description": "To get information or guide for the command or plugin",
        "flags": {
            "c": "if command name and plugin name is same then you get guide for plugin. So by using this flag you get command guide.",
        },
        "usage": [
            "{tr}help (plugin/command name)",
            "{tr}help -c (command name)",
        ],
        "examples": ["{tr}help help", "{tr}help -c help"],
    },
)
async def _(event):
    "To get guide for catuserbot."
    flag = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    if flag and input_str:
        outstr = await cmdinfo(input_str, event)
        if outstr is None:
            return
    elif input_str:
        outstr = await plugininfo(input_str, event)
        if outstr is None:
            return
    else:
        outstr = await grpinfo()
    await edit_or_reply(event, outstr)


@catub.cat_cmd(
    pattern="dc$",
    command=("dc", plugin_category),
    info={
        "header": "To show dc of your account.",
        "description": "Dc of your account and list of dc's will be showed",
        "usage": "{tr}dc",
    },
)
async def _(event):
    "To get dc of your bot"
    result = await event.client(functions.help.GetNearestDcRequest())
    result = f"**Dc details of your account:**\
              \n**Country :** {result.country}\
              \n**Current Dc :** {result.this_dc}\
              \n**Nearest Dc :** {result.nearest_dc}\
              \n\n**List Of Telegram Data Centres:**\
              \n**DC1 : **Miami FL, USA\
              \n**DC2 :** Amsterdam, NL\
              \n**DC3 :** Miami FL, USA\
              \n**DC4 :** Amsterdam, NL\
              \n**DC5 : **Singapore, SG\
                "
    await edit_or_reply(event, result)
