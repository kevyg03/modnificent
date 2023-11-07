from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# from selenium_stealth import stealth
import time
import youtube_data
import argparse
import random


# search_terms = ["boba"]

### --------- HELPERS START --------- ###


def get_items_from_txt(filename):
    with open(filename, "r") as f:
        items = f.readlines()
        items = [item.strip() for item in items]
        return items


### --------- HELPERS END --------- ###


def scrape(driver, term):
    driver.get(f"https://www.youtube.com/results?search_query={term}")
    titles = driver.find_elements(By.ID, "channel-thumbnail")
    time.sleep(3)
    creator_url_list = [(elem.get_attribute("href"), term) for elem in titles]
    return creator_url_list


def youtube_creator_main(save_path, search_terms):
    driver = webdriver.Chrome()

    creator_url_set = set()
    for term in search_terms:
        creator_url_set = creator_url_set.union(scrape(driver, term))

    print("creator url set: ", creator_url_set)

    youtube_data.youtube_data_main(save_path, driver, creator_url_set)

    driver.quit()


if __name__ == "__main__":
    # "/Users/joleneh/jolenehuey@berkeley.edu - Google Drive/My Drive/Extracurriculars Self Learning/SMMP/Social Media Model Project (Gravidy)/Coding [confidential]/Creator Sourcing Scraping/creator-csvs"

    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "-save_directory",
    #     type=str,
    #     help="directory to save csvs to, ideally shared drive",
    #     required=True,
    # )
    # parser.add_argument("-search_terms_path", type=str, default="input.txt")

    # args = parser.parse_args()

    save_path = "csv_files"

    method = input(
        "Select a method to search for creators (enter the number): \n 1. Search terms \n 2. With creator URL's (sourcing from channel pages) \n Any other ideas? Let C-SWE know.\n"
    )

    if "1" in method:
        key_words = input(
            "Enter the key words you'd like to search for creators with, separated by commas: \n"
        )
        search_terms = key_words.split(",")
        # remove outer spaces from search terms
        search_terms = [term.strip() for term in search_terms]

        current = time.time()
        save_path = f"{save_path}/including-{random.sample(search_terms, 1)[0]}.csv"
        youtube_creator_main(save_path, search_terms)
    else:
        print(
            "Sorry, this isn't implemented yet. We will help you download the updated version when it is ready."
        )
