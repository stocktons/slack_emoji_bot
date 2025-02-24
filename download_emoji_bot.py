import requests
from emoji import emoji_data


def download_emoji():
    for emoji_name, emoji_url in emoji_data.items():
        emoji_path = f"emojis/{emoji_name}.png"
        response = requests.get(emoji_url)
        with open(emoji_path, "wb") as f:
            f.write(response.content)


if __name__ == "__main__":
    download_emoji()
