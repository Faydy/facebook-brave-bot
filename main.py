import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
custom_profile_path = r"C:\BraveBot"
profile_dir_name = "Profile 2"
image_path = r"C:\Users\samma\Pictures\Banner.png"
success_url = "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2JldGowbnBrcHZqM2Fjcm5hazl6ZTdyaGNiYnJoMHNjdWQ4eTFuNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QhmboW0R7eUbm/giphy.gif"

options = Options()
options.binary_location = brave_path
options.add_argument(f"--user-data-dir={custom_profile_path}")
options.add_argument(f"--profile-directory={profile_dir_name}")
options.add_experimental_option("detach", True)
# Dezactiveaza notificarile care pot bloca butonul de Post
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=options)

with open("text.txt", 'r', encoding="utf-8") as f:
    post_text = f.read()

with open("links.txt", 'r') as f:
    links = [line.strip() for line in f.readlines() if line.strip()]

errors = 0

for i, url in enumerate(links):
    try:
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Write something')]"))
        ).click()

        textbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='textbox' and @contenteditable='true' and (starts-with(@aria-placeholder, 'Write something') or starts-with(@aria-placeholder, 'Create a public post'))]"))
        )
        
        driver.execute_script("arguments[0].click();", textbox)
        
        pyperclip.copy(post_text)
        textbox.send_keys(Keys.CONTROL, "v")
        
        

        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//input[@type='file']"))
        )

        file_input.send_keys(image_path)
        time.sleep(3)
        # Asteptam ca butonul Post sa devina activ (clickable) dupa incarcarea imaginii
        post_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='dialog']//div[@aria-label='Post']"))
        )
        
        post_button.click()

        # Timp necesar pentru ca Facebook sa proceseze upload-ul inainte de a schimba pagina
        time.sleep(6)
        
        print(f"Postat cu succes pe linkul {i + 1}.")

    except Exception as e:
        print(f"Eroare la linkul {url}: {e}")
        errors += 1
        continue

print(f"Finished with {errors} errors")
driver.get(success_url)