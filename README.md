# Freelancer Data Scraper

This Python script scrapes freelancer profiles from PeoplePerHour and job listings from Guru.com, then saves the data to Excel files.

## Features

- Scrapes freelancer profiles from PeoplePerHour (pages 1-10)
  - Collects title, URL, budget, skills, hourlies, and member stats
- Scrapes job listings from Guru.com (all available pages)
  - Collects title, URL, budget, description, and required skills
- Saves data to separate Excel files with timestamps
- Handles errors and timeouts gracefully

## Requirements

- Python 3.6+
- Libraries listed in `requirements.txt`

## Installation

1. Clone this repository or download the script
2. Install required packages:
pip install -r requirements.txt

## Usage

Run the script:
python scraper.py


The script will generate two Excel files:
- `peopleperhour_freelancer_data.xlsx`
- `guru_jobs_data.xlsx`

## Notes

- The script may need updates if the target websites change their HTML structure
- Be respectful with scraping - don't overload the servers
- Consider adding delays between requests if running frequently

## Disclaimer

This script is for educational purposes only. Please check the websites' terms of service before scraping.
