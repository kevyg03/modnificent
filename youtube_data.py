from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# from selenium_stealth import stealth
from pprint import pprint
import json
import pandas as pd

usernames = ["https://www.youtube.com/@DisguisedToast"]  # "YasoobKhalid"
proxy = "server:port"

output = {}

### --------- HELPERS START --------- ###


def parse_num(str_num):
    last_letter = str_num[-1]
    int_views = 0
    if last_letter in "0123456789":
        int_views = str_num
    elif last_letter == "K":
        int_views = float(str_num[:-1]) * 1000
    elif last_letter == "M":
        int_views = float(str_num[:-1]) * 1000000
    elif last_letter == "B":
        int_views = float(str_num[:-1]) * 1000000000

    return int(int_views)


### --------- HELPERS END --------- ###


def prepare_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--proxy-server={proxy}")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=chrome_options)
    # stealth(driver,
    #         user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
    #         languages= ["en-US", "en"],
    #         vendor=  "Google Inc.",
    #         platform=  "Win32",
    #         webgl_vendor=  "Intel Inc.",
    #         renderer=  "Intel Iris OpenGL Engine",
    #         fix_hairline= False,
    #         run_on_insecure_origins= False,
    #         )
    return driver


def scrape(driver, creator_url, search_term):
    # Possible keys:
    # channel, subs, avg_last_10_views, total_channel_views, total_videos, channel_description,
    # location
    output = {"search_term:": search_term}

    # # Scrape from creatur_url/videos
    # # Gets the channel name, subscriber count, and average views of the last 10 videos
    video_url = f"{creator_url}/videos"

    driver.get(video_url)
    print(f"Attempting: {driver.current_url}")
    if "login" in driver.current_url:
        return "Failed/ redir to login"
    else:
        try:
            channel_name = driver.find_element(
                By.XPATH, '//yt-formatted-string[contains(@class, "ytd-channel-name")]'
            ).text
        except:
            channel_name = ""

        try:
            subscriber_count = driver.find_element(
                By.XPATH, '//yt-formatted-string[@id="subscriber-count"]'
            ).text
            subscriber_count = parse_num(subscriber_count.split(" subscribers")[0])
        except:
            subscriber_count = ""

        # Mitigate unresolved error where some channels don't give video.text
        try:
            videos_views = driver.find_elements(By.ID, "metadata-line")
            videos_views = [video.text.splitlines()[0] for video in videos_views]
            remove_views = [view.split(" views")[0] for view in videos_views]
            float_views = [parse_num(view) for view in remove_views]

            if len(float_views) > 10:
                float_views = float_views[:10]
                avg_videos_views = sum(float_views) / 10
            else:
                avg_videos_views = sum(float_views) / len(float_views)

            output["avg_last_10_views"] = avg_videos_views

        except:
            output["avg_last_10_views"] = ""

        output["channel"] = channel_name
        output["subs"] = subscriber_count

    # Scrape from creator_url/about
    # Get total views and channel description
    about_url = f"{creator_url}/about"

    driver.get(about_url)
    print(f"Attempting: {driver.current_url}")
    if "login" in driver.current_url:
        return "Failed/ redir to login"
    else:
        try:
            channel_about = driver.find_elements(
                By.XPATH,
                '//yt-formatted-string[contains(@class, "style-scope ytd-channel-about-metadata-renderer")]',
            )
        except:
            channel_about = ""

        try:
            info_list = [info.text for info in channel_about]
            # print(info_list)  # Can extra more info from this if desired

            if "Stats" in info_list:
                idx = info_list.index("Stats")

                join_time = (
                    info_list[idx + 1]
                    if len(info_list) > idx and "Joined" in info_list[idx + 1]
                    else ""
                )

                if len(info_list) > idx + 1 and "views" in info_list[idx + 2]:
                    num_channel_views_str = info_list[idx + 2]
                    num_channel_views = int(
                        num_channel_views_str.split(" ")[0].replace(",", "")
                    )
                else:
                    num_channel_views = ""

                output["join_time"] = join_time
                output["total_channel_views"] = num_channel_views

            if "Location:" in info_list:
                idx = info_list.index("Location:")
                location = info_list[idx + 1]
                output["location"] = location

            if "For business inquires:" in info_list:
                idx = info_list.index("For business inquires:")
                email = info_list[idx + 1]
                output["email"] = email

        except:
            output["total_channel_views"] = ""
            output["location"] = ""
            output["email"] = ""

        try:
            total_videos = driver.find_element(
                By.XPATH, '//yt-formatted-string[@id="videos-count"]'
            ).text
        except:
            total_videos = ""

        try:
            channel_description = driver.find_element(
                By.XPATH,
                '//yt-formatted-string[@id="description"]',
            ).text
        except:
            channel_description = ""

        output["total_videos"] = total_videos
        output["channel_description"] = channel_description

    output_df = pd.DataFrame(output, index=[0])
    return output_df


def youtube_data_main(save_path, driver, creator_url_list):
    creator_df = pd.DataFrame(
        columns=[
            "search_term",
            "channel",
            "subs",
            "avg_last_10_views",
            "total_channel_views",
            "total_videos",
            "email",
            "channel_description",
            "location",
        ]
    )

    for creator_tuple in creator_url_list:
        creator_url, search_term = creator_tuple

        creator_df = pd.concat(
            [creator_df, scrape(driver, creator_url, search_term)], ignore_index=True
        )

    creator_df.to_csv(save_path)


if __name__ == "__main__":
    save_path = "test.csv"
    driver = webdriver.Chrome()
    youtube_data_main(save_path, driver, usernames)
