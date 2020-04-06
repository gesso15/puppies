import requests
from bs4 import BeautifulSoup
import time
import re
from random import randint

current_num_puppies = 0
delay = 300  # figure 5 minutes is a often, but not too often
max_delay_add = 47

while True:
    url = "https://www.milofoundation.org/adopt.cfm?Species=Dog&Name=&Gender=&age=Kitten+or+Puppy&Breed1=&Weight=&btn_search=Search"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    puppies = soup.find_all("span", class_="BodyFont") # this is where the number of puppies is on the page...
    if len(puppies) is not 0:
        puppy_string = puppies[0]
        # TODO this is gross and brittle...
        num_puppies = int(re.sub('[\s+]', '', (str(puppy_string))).split(">")[4].split("-")[0].strip('Dogsfound'))
        if num_puppies != current_num_puppies:
            # TODO send email or toast or something?
            print(f'{num_puppies - current_num_puppies} new puppies!')
            current_num_puppies = num_puppies
        else:
            print("no new puppies :(")
    else:
        print("failed to parse web page")
    print(f"trying again in {delay} seconds + some for detection avoidance")
    time.sleep(delay + randint(1, max_delay_add))

