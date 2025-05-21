
# Web Scraper for Guru.com Jobs and PeoplePerHour Freelancers

This Python script scrapes job listings from [Guru.com](https://www.guru.com/d/jobs) and freelancer profiles from [PeoplePerHour](https://www.peopleperhour.com/hire-freelancers). The data is saved into separate Excel files for tracking and analysis.

---

## 📦 Install Requirements

Make sure you have **Python 3.7+** installed on your system.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/freelance-job-scraper.git
cd freelance-job-scraper
```

### 2. Install Required Libraries

Install dependencies using `pip`:

```bash
pip install -r requirements.txt
```

Or install them manually:

```bash
pip install requests beautifulsoup4 pandas openpyxl html5lib
```

---

## 🚀 Run the Script

After installing the dependencies, run the script with:

```bash
python scraper.py
```

---

## 📁 Output Files

- `guru_jobs_data.xlsx` – Contains job listings scraped from Guru.com.
- `freelancer_data.xlsx` – Contains freelancer profiles scraped from PeoplePerHour.

Each entry includes a timestamp indicating when the data was scraped.

---

## ✅ Example Use Case

Use this script to:

- Track freelance job opportunities across platforms.
- Analyze required skills and trends in freelance markets.
- Find and categorize freelancers by expertise and description.

---
