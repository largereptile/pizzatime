from fake_useragent import UserAgent
from selenium import webdriver
from random import randint
from itertools import chain, combinations
import time


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def add_dots(positions, string):
    string = list(string)
    for pos in positions:
        string.insert(pos, ".")
    return ''.join(string)


def generate_alts(email):
    length = len(email)
    combos = powerset([x for x in range(length)])
    return [add_dots(combo, email) for combo in combos]


def get_pizza(driver, url, email, number, store_name):
    driver.get(url)
    time.sleep(1)
    fill_form(driver, email, number, store_name)
    driver.refresh()
    time.sleep(1)
    fill_form(driver, email, number, store_name)
    driver.find_element_by_id("submit-signup").click()


def fill_form(driver, email, number, store_name):
    driver.find_element_by_name("fullname").send_keys("test test")
    driver.find_element_by_name("email").send_keys(email)
    driver.find_element_by_name("mobile").send_keys(number)
    el = driver.find_element_by_name("store")
    for option in el.find_elements_by_tag_name("option"):
        if option.text == store_name:
            option.click()
            break
    driver.find_element_by_id("submit-signup").click()


if __name__ == "__main__":
    # CONFIG
    main_email_prefix = "dominospizzatestemail"
    email_suffix = "gmail.com"
    place = "city"
    store_name = "storename"

    ua = UserAgent(verify_ssl=False)
    user_agent = ua.random

    print("USER AGENT: " + user_agent)

    firefox_opts = webdriver.FirefoxOptions()
    firefox_opts.add_argument("user-agent=" + user_agent)
    driver = webdriver.Firefox(options=firefox_opts)

    url = f"https://mydominos.co.uk/tot/{place}"
    alts = generate_alts(main_email_prefix)

    for prefix in alts:
        print(prefix)
        get_pizza(driver, url, f"{prefix}@{email_suffix}", f"07{randint(100000000, 999999999)}", )
