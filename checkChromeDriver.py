from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Correct path to your chromedriver.exe
CHROMEDRIVER_PATH = "C:\\Users\\Gili\\Woot Scrapper\\chromedriver-win64\\chromedriver.exe"

# Setup Chrome options
options = Options()
options.add_argument("--headless")  # Run in background
options.add_argument("--window-size=1920,1080")

# Setup service
service = Service(CHROMEDRIVER_PATH)

# Launch browser
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://example.com")
print(driver.title)
driver.quit()
