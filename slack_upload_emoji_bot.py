import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

load_dotenv()
slack_workspace = os.getenv("SLACK_WORKSPACE")
slack_emoji_url = f"https://{slack_workspace}.slack.com/customize/emoji"
add_custom_emoji_button = '//*[@id="list_emoji_section"]/div/div/div/div[1]/button[2]'
upload_image_file_input = '//*[@id="emojiimg"]'
name_emoji_input = '//*[@id="emojiname"]'
sign_in_with_password_link = '//*[@id="page_contents"]/div/div/div[2]/div[3]/div/span/a'
email_input = '//*[@id="email"]'
password_input = '//*[@id="password"]'
sign_in_button = '//*[@id="signin_btn"]'
save_button = "button[data-qa='customize_emoji_add_dialog_go']"


def upload_emoji():
    driver = webdriver.Chrome()
    driver.get(slack_emoji_url)
    time.sleep(1)
    driver.find_element(By.XPATH, sign_in_with_password_link).click()
    time.sleep(1)
    driver.find_element(By.XPATH, email_input).send_keys(os.getenv("SLACK_EMAIL"))
    time.sleep(1)
    driver.find_element(By.XPATH, password_input).send_keys(os.getenv("SLACK_PASSWORD"))
    time.sleep(1)
    driver.find_element(By.XPATH, sign_in_button).click()
    time.sleep(1)
    driver.get(slack_emoji_url)
    time.sleep(1)
    for file in os.listdir("emojis"):
        print(file)
        emoji_path = f"/Users/sarah/Projects/slack-emoji-bot/emojis/{file}"
        driver.find_element(By.XPATH, add_custom_emoji_button).click()
        time.sleep(1)
        driver.find_element(By.XPATH, upload_image_file_input).send_keys(emoji_path)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, save_button).click()
        time.sleep(1)


def main():
    upload_emoji()


if __name__ == "__main__":
    main()


