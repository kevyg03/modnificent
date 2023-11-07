from selenium import webdriver
from selenium.webdriver.common.by import By
from pprint import pprint
import json
usernames = ["dlwlrma", "disguisedtoast"]
output = {}


def parse_data(username, user_data):
    captions = []
    if len(user_data['edge_owner_to_timeline_media']['edges']) > 0:
        for node in user_data['edge_owner_to_timeline_media']['edges']:
            if len(node['node']['edge_media_to_caption']['edges']) > 0:
                if node['node']['edge_media_to_caption']['edges'][0]['node']['text']:
                    captions.append(
                        node['node']['edge_media_to_caption']['edges'][0]['node']['text']
                    )
                
    output[username] = {
        'name': user_data['full_name'],
        'category': user_data['category_name'],
        'followers': user_data['edge_followed_by']['count'],
        'posts': captions,
    }

def scrape(username):
    url = f'https://instagram.com/{username}/?__a=1&__d=dis'
    driver = webdriver.Chrome()
    driver.get(url)
    print (f"Attempting: {driver.current_url}")
    if "login" in driver.current_url:
        print ("Failed/ redir to login")
        driver.quit()
    else:
        print ("Success")
        resp_body = driver.find_element(By.TAG_NAME, "body").text
        data_json = json.loads(resp_body)
        print(data_json)
        user_data = data_json['graphql']['user']
        parse_data(username, user_data)
        driver.quit()

def main():
    for username in usernames:
        scrape(username)

if __name__ == '__main__':
    main()
    pprint(output)