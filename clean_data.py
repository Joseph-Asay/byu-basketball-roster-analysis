from pathlib import Path

import pandas as pd

# Load scraped dataset
players = pd.read_csv("data/scraped_players.csv")


# Convert jersey numbers from strings like "#24" into numeric values
players["jersey_number"] = pd.to_numeric(
    players["number"].str.replace("#", "", regex=False),
    errors="coerce"
).astype("Int64")


# Convert heights from feet and inches into centimeters
# First remove the inch symbol and split the height into feet and inches
height_split = players["height"].str.replace("″", "", regex=False).str.split("′", expand=True)

feet = pd.to_numeric(height_split[0], errors="coerce")
inches = pd.to_numeric(height_split[1], errors="coerce")

# Convert total inches into centimeters (1 inch = 2.54 cm)
players["height_cm"] = ((feet * 12 + inches) * 2.54).round(1)


# Separate the state or country from the hometown column
# Hometowns are formatted like "Provo, Utah" or "Dakar, Senegal"
location = players["hometown"].str.split(",").str[-1].str.strip()


# Create binary column indicating whether a player is from Utah
# 1 = Utah, 0 = Anywhere else
players["utah"] = (location == "Utah").astype(int)


# List of international countries found in our scraped dataset
# IMPORTANT! You will need to update this or change the method if 
# you decide to scrape across all coaching tenures and not just the past three
international_countries = [
    "Argentina", "Australia", "Austria", "Bahamas", "Brazil",
    "Canada", "China", "Egypt", "France", "Ivory Coast",
    "Lithuania", "Mali", "Mexico", "Netherlands", "New Zealand",
    "Nigeria", "Russia", "Senegal", "Serbia", "Tanzania"
]

# Create binary column indicating whether a player is international
# 1 = Outside the United States, 0 = United States
players["international"] = location.isin(international_countries).astype(int)


# Find the data folder inside this repository
# This will work even if we run the script from another folder
data_folder = Path(__file__).resolve().parent / "data"
data_folder.mkdir(exist_ok=True)

# Load the dataset created by scraper.py
players = pd.read_csv(data_folder / "scraped_players.csv")
