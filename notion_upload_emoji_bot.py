import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
NOTION_EMAIL = os.getenv("NOTION_EMAIL")
NOTION_PASSWORD = os.getenv("NOTION_PASSWORD")


def login(driver):
    # 1) go to Notion login
    driver.get("https://www.notion.so/login")
    time.sleep(2)

    # 2) click Google SSO
    google_btn = driver.find_element(By.XPATH,
        "//*[@id='notion-app']/div/div[1]/div/div/main/div[1]/section/div/div/div/div[2]/div[1]/div[1]/div[1]/div"
    )
    google_btn.click()
    time.sleep(5)

    # 3) switch to Google login window if needed
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])

    # 4) enter email
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "identifierId"))
    )
    email_input.send_keys(NOTION_EMAIL)
    email_input.send_keys(Keys.RETURN)
    time.sleep(3)

    # 5) enter password
    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "Passwd"))
    )
    password_input.send_keys(NOTION_PASSWORD)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

    # 6) switch back to main window
    driver.switch_to.window(driver.window_handles[0])
    WebDriverWait(driver, 15).until(
        lambda d: "notion.so" in d.current_url
    )
    time.sleep(5)


def open_emoji_settings(driver):
    time.sleep(3)

    # open workspace menu
    workspace_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='Clever']"))
    )
    workspace_btn.click()
    time.sleep(2)

    # click Settings
    settings_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='Settings']"))
    )
    driver.execute_script("arguments[0].click();", settings_btn)
    time.sleep(2)

    # click Emoji tab
    emoji_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='Emoji']"))
    )
    emoji_tab.click()
    time.sleep(2)


def upload_all_emojis():
    opts = Options()
    # opts.add_argument("--headless")  # uncomment to run without UI
    driver = webdriver.Chrome(options=opts)

    try:
        login(driver)
        open_emoji_settings(driver)

        for fname in os.listdir("emojis"):
            path = os.path.abspath(os.path.join("emojis", fname))
            name, _ = os.path.splitext(fname)
            print(f"Processing emoji: {name}")

            # 1) click "Add emoji"
            add_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                    "//div[@role='button' and contains(text(),'Add emoji')]"
                ))
            )
            driver.execute_script("arguments[0].click();", add_btn)
            time.sleep(1)

            # 2) stub out native input.click to prevent Finder
            driver.execute_script(
                "window.__origInputClick = HTMLInputElement.prototype.click;"
                "HTMLInputElement.prototype.click = function(){};"
            )

            # 3) trigger Notion to inject the file input
            upload_trigger = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH,
                    "//div[contains(text(),'Upload an image')]"
                ))
            )
            upload_trigger.click()
            time.sleep(1)

            # 4) restore native click
            driver.execute_script(
                "HTMLInputElement.prototype.click = window.__origInputClick;"
            )

            # 5) locate the injected file input
            file_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            driver.execute_script(
                "arguments[0].style.display='block';"
                "arguments[0].style.visibility='visible';"
                "arguments[0].style.opacity=1;",
                file_input
            )

            print(f"Uploading {path!r}, exists? {os.path.exists(path)}")
            file_input.send_keys(path)
            time.sleep(1)

            # 6) set the emoji name
            name_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "emojiName"))
            )
            name_input.clear()
            name_input.send_keys(name)
            name_input.send_keys(Keys.TAB)
            time.sleep(0.5)

            # 7) click Save
            save_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                    "//div[@role='button' and text()='Save']"
                ))
            )
            driver.execute_script("arguments[0].click();", save_btn)
            time.sleep(2)

            # 8) handle duplicate name error
            try:
                err = driver.find_element(
                    By.XPATH, "//div[contains(text(),'Name already taken')]"
                )
                if err.is_displayed():
                    cancel = driver.find_element(
                        By.XPATH, "//div[@role='button' and contains(text(),'Cancel')]"
                    )
                    cancel.click()
                    print(f"Emoji '{name}' exists, skipped.")
                    time.sleep(1)
                    continue
            except:
                print(f"Uploaded emoji '{name}' successfully.")

        print("Finished processing all emojis!")

    finally:
        driver.quit()


if __name__ == "__main__":
    upload_all_emojis()
