# Standard library
import random
import time

# Third-party libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Identify myself and give my email for good ethical practic
headers = {
    "User-agent": "BYURosterResearchBot/1.0 (Stat_386_Assignment; contact: jasay1@byu.edu)"
}

# Initialize data dictionary with values we are going to be scraping for dataset
data_dict = {
    "name": [],
    "number": [],
    "height": [],
    "year": [],
    "hometown": [],
    "previous_team": [],
    "head_coach": [],
    "season": []
}


# Function to find head coach - this way we only have to find the head coach once per page
def find_coach(soup, tag, class_name, string):
    # We first find the card that has "head coach" as the title, most secure way to make sure we get the head coach
    coach_title = soup.find(tag, class_=class_name, string=string)
    coach_card = coach_title.find_parent("div", class_="roster-card-item__heading")
    return coach_card.find("a", {"class": "roster-card-item__title-link"}).text.strip()


# Helps find element if it exists or return None
def find_element(card, tag, class_name):
    element = card.find(tag, class_=class_name)
    return element.get_text(strip=True) if element else None


# Height and year have the same `class_name` so it is easiest to make a separate function to find the two
def find_height_year(card, tag, class_name):
    elements = card.find_all(tag, class_=class_name)

    if len(elements) >= 2:
        height = elements[0].get_text(strip=True)
        year = elements[1].get_text(strip=True)
        return height, year

    return None, None


# We are looking at the previous three coaching tenures so we will only go back until 2005-2006
targeted_seasons = [
    "2026-2027", "2025-2026", "2024-2025", "2023-2024",
    "2022-2023", "2021-2022", "2020-2021", "2019-2020",
    "2018-2019", "2017-2018", "2016-2017", "2015-2016",
    "2014-2015", "2013-2014", "2012-2013", "2011-2012",
    "2010-2011", "2009-2010", "2008-2009", "2007-2008",
    "2006-2007", "2005-2006"
]


for season in targeted_seasons:
    # Load Roster Website
    url = f"https://byucougars.com/sports/mens-basketball/roster/season/{season}?view=card"

    r = requests.get(url, timeout=15, headers=headers)
    r.raise_for_status()

    # Acquire page html
    soup = BeautifulSoup(r.text, "html.parser")

    # This grabs only cards for basketball players intsead of all staff members.
    cards = soup.select('div[class="roster-card-item"]')

    head_coach = find_coach(soup, "div", "roster-card-item__position", "Head Coach")

    # Iterate through each player card and scrape data for our data dictionary
    for card in cards:
        name = find_element(card=card, tag="a", class_name="roster-card-item__title-link")
        number = find_element(card=card, tag="strong", class_name="roster-card-jersey-number roster-card-item__jersey-number")
        height, year = find_height_year(card=card, tag="span", class_name="roster-player-card-profile-field__value roster-player-card-profile-field__value--basic")
        hometown = find_element(card=card, tag="span", class_name="roster-player-card-profile-field__value roster-player-card-profile-field__value--hometown")
        previous_team = find_element(card=card, tag="span", class_name="roster-player-card-profile-field__value roster-player-card-profile-field__value--previous-school")       

        #  Append values to data dictionary
        data_dict["name"].append(name)
        data_dict["number"].append(number)
        data_dict["height"].append(height)
        data_dict["year"].append(year)
        data_dict["hometown"].append(hometown)
        data_dict["previous_team"].append(previous_team)
        data_dict["head_coach"].append(head_coach)
        data_dict["season"].append(season)

    # add additional time between requests so as to know overload the servers
    time.sleep(random.uniform(3,5))


# Create dataframe
players = pd.DataFrame(data_dict)

# write players to csv
players.to_csv("data/scraped_players.csv", index=False)



