import os

emoji_list = [
    "extraspicy.png",
    "link_run.png",
    "mew.png",
    "oh_the_drama.png",
    "okayguy.png",
]


def delete_emoji():
    for emoji in emoji_list:
        emoji_path = f"/Users/sarah/Projects/slack-emoji-bot/emojis/{emoji}"
        os.remove(emoji_path)


if __name__ == "__main__":
    delete_emoji()

