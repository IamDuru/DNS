from DnsXMusic import app
import random
import time
from pyrogram import filters

# Reactions list
reactions = [
    '👍', '👎', '❤️', '🔥', '🥰', '👏', '😁', '🤔', '🤯', '😱', '🤬', '😢', '🎉', '🤩', '🤮', '💩', '🙏', '👌',
    '🕊', '🤡', '🥱', '🥴', '😍', '🐳', '❤️‍🔥', '🌚', '🌭', '💯', '🤣', '⚡️', '🍌', '🏆', '💔', '🤨', '😐',
    '🍓', '🍾', '💋', '🖕', '😈', '😴', '🤓', '👻', '👨‍💻', '👀', '🎃', '🙈', '😇', '😨', '🤝', '✍️', '🤗',
    '🫡', '🎅', '🎄', '☃️', '💅', '🤪', '🗿', '🆒', '💘', '🙉', '🦄', '😘', '💊', '🙊', '😎', '👾', '🤷‍♂️',
    '🤷‍♀️', '😭', '🤫', '💃', '🕺', '👋', '🐷', '🌹', '💖', '🌈', '🖤', '😡', '😳', '🥳', '🤖', '🦸', '🦹',
    '🧙‍♂️', '🧙‍♀️', '🧝‍♂️', '🧝‍♀️', '🧛‍♂️', '🧛‍♀️', '🧟‍♂️', '🧟‍♀️', '🧞‍♂️', '🧞‍♀️', '🧜‍♂️', '🧜‍♀️',
    '🧚‍♂️', '🧚‍♀️', '🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐻‍❄️', '🐨', '🐯', '🦁', '🐮', '🐷',
    '🐸', '🐵', '🙈', '🙉', '🙊', '🐒', '🐔', '🐧', '🐦', '🐤', '🐣', '🐥', '🦆', '🦅', '🦉', '🦜', '🐓', '🦃',
    '🐬', '🐟', '🐠', '🐡', '🦈', '🐙', '🐚', '🐌', '🐞', '🐜', '🦋', '🐝', '🐧', '🦗', '🕷', '🕸', '🦕', '🦖',
    '🦎', '🐢', '🐍', '🦂', '🦟', '🦠', '🐲', '🐉', '🦜', '🐳', '🐋', '🐬'
]


# Global variable to track reaction status (default off)
is_reaction_on = False

@app.on_message(filters.command(["reaction", "react", "eaction", "eact"], prefixes=["/", "!", ".", "R", "r"]))
def toggle_reaction(client, message):
    global is_reaction_on
    command_parts = message.text.split()
    if len(command_parts) == 2:
        if command_parts == "on":
            is_reaction_on = True
            message.reply_text("Reaction spam is now ON 😈")
        elif command_parts == "off":
            is_reaction_on = False
            message.reply_text("Reaction spam is now OFF 😌")
        else:
            message.reply_text("Invalid command. Use /reaction on or /reaction off")
    else:
        message.reply_text("Invalid command. Use /reaction on or /reaction off")

@app.on_message(filters.all)
def auto_react(_, message):
    global is_reaction_on
    if is_reaction_on:
        reaction = random.choice(reactions)
        time.sleep(0.5)
        message.react(reaction)
