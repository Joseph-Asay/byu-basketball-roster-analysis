
# BYU Basketball Roster Analysis

This project uses Python web scraping to build an original dataset of BYU men's basketball rosters. The goal is to explore how roster composition has changed across the three most recent head-coaching tenures: Dave Rose, Mark Pope, and Kevin Young.

**Question of interest:** How have BYU men's basketball rosters changed across coaching eras in player height, class, hometown geography, and previous school?

The current scraper covers **22 seasons, from 2005–2006 through 2026–2027**. The original dataset contains **346 player-season observations**. Each row represents one player on one season's roster, so players who appear across multiple seasons will have multiple observations.

## Data Source

The data comes from the official [BYU men's basketball roster pages](https://byucougars.com/sports/mens-basketball/roster).

The `scraper.py` script uses `requests` to retrieve each season's roster page and `BeautifulSoup` to extract player information.

Example URL:

https://byucougars.com/sports/mens-basketball/roster/season/2026-2027?view=card

The scraper also identifies itself with a user-agent and pauses between requests to avoid overloading the website.

## Repository Contents

| File | Description |
| --- | --- |
| `scraper.py` | Scrapes player rosters and saves the raw dataset. |
| `clean_data.py` | Cleans the scraped dataset and creates new numeric variables. |
| `pyproject.toml` | Defines the Python dependencies. |
| `uv.lock` | Records dependency versions for reproducibility. |
| `.gitignore` | Excludes unnecessary files from GitHub. |
| `data/` | Contains the generated CSV datasets after running the scripts. |

The two generated datasets are:

- `data/scraped_players.csv`: Original scraped dataset.
- `data/cleaned_players.csv`: Cleaned dataset with additional variables for analysis.

## Requirements

To reproduce this project, you will need:

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Internet access to scrape the BYU roster pages

The Python packages used are:

- `requests`
- `beautifulsoup4`
- `pandas`

These dependencies are already specified in `pyproject.toml`.

## How to Reproduce the Dataset

### Step 1: Clone the repository

Open your terminal and clone this repository:

```bash
git clone https://github.com/YOUR-USERNAME/byu-basketball-roster-analysis.git
```

Navigate into the project folder:

```bash
cd byu-basketball-roster-analysis
```

### Step 2: Install dependencies

Run the following command:

```bash
uv sync --locked
```

This installs the necessary Python packages using the dependency versions recorded in `uv.lock`.

### Step 3: Run the scraper

```bash
uv run --locked python scraper.py
```

This script visits the BYU roster pages for each season specified in `targeted_seasons`.

It collects eight variables:

- `name`: Player name
- `number`: Jersey number
- `height`: Height in feet and inches
- `year`: Player's class
- `hometown`: Hometown and state/country
- `previous_team`: Previous school or team
- `head_coach`: Head coach for that season
- `season`: Roster season

The script saves the results to:

`data/scraped_players.csv`

### Step 4: Run the cleaning script

```bash
uv run --locked python clean_data.py
```

This script reads the scraped dataset and creates four additional variables:

- `jersey_number`: Numeric version of the player's jersey number.
- `height_cm`: Player height converted into centimeters.
- `utah`: Binary variable (1 = from Utah, 0 = not from Utah).
- `international`: Binary variable (1 = outside the United States, 0 = United States).

The original eight columns are preserved, resulting in a dataset with **12 columns**.

The cleaned dataset is saved to:

`data/cleaned_players.csv`

This is the dataset intended for exploratory data analysis.

**Important:** Run `scraper.py` before `clean_data.py`, since the cleaning script requires the scraped dataset.

## Updating the Dataset

There are two important things to consider when using this project for a different time period.

### 1. Updating the seasons in scraper.py

The scraper currently collects data from the **2005–2006 through 2026–2027 seasons**, covering the coaching tenures of:

- Dave Rose (2005–2006 through 2018–2019)
- Mark Pope (2019–2020 through 2023–2024)
- Kevin Young (2024–2025 through 2026–2027)

The seasons are specified in a list called `targeted_seasons` in `scraper.py`.

**If you run this project after the 2026–2027 season**, you will need to manually add newer seasons to the beginning of this list.

For example, you could add `"2027-2028"` once that season's roster is available.

Similarly, if you want to collect data from seasons before Dave Rose's coaching tenure, you will need to extend the list beyond `"2005-2006"`.

The scraper identifies the head coach directly from each season's roster page, rather than manually assigning coaches to years.

Make sure the roster pages you are requesting still exist and follow the expected HTML format.

### 2. Updating international_countries in clean_data.py

The cleaning script creates an `international` variable using a manually defined list called `international_countries`.

This list includes the countries represented in the original dataset from **2005–2006 through 2026–2027**.

The script checks the player's hometown against this list to determine whether they are international.

**If you change the years being analyzed, you should review and update `international_countries`.**

Additional seasons may include players from countries not currently included in the list. If those countries are not added, those players could incorrectly be classified as domestic players.

An alternative would be to use a more comprehensive method of distinguishing U.S. states from international countries.

For the current dataset, the manually defined list is sufficient.

## Reproducibility Notes

This repository is designed so others can recreate the data acquisition and cleaning process.

A few important notes:

- The original dataset contains 346 player-season observations across 22 seasons.
- The same player may appear multiple times if they played in multiple seasons.
- Missing jersey numbers are preserved as missing values during cleaning.
- The scripts automatically create the `data/` folder if it does not already exist.
- The `.gitignore` currently excludes generated CSV files, so users need to run the scripts to reproduce the datasets.
- The `uv.lock` file records the dependency versions used in the project.

Because the scraper retrieves information from a live website, future runs may produce slightly different results if BYU updates its roster pages or changes its website structure.

The code and dependency versions are reproducible, but identical scraped data cannot be guaranteed indefinitely.