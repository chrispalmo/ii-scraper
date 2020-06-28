# ii-scraper

---

#### About

ii-scraper is a python script built for members of https://www.intelligentinvestor.com.au/ that extracts, summarizes and analyzes investment recommendations, saving output as an excel ".xlsx" file.

#### Readme

Before running, create "keys.py" in the root directory:

    KEYS = {
        'username': 'YOUR_USERNAME_HERE',
        'password': 'YOUR_PASSWORD_HERE'
    }
    DRIVER_LOCATION = r'ABSOLUTE_PATH_TO_PROJECT_DIRECTORY\chromedriver.exe'

#### Project setup notes:

###### Git initialization

> ii-scraper> git init .

###### Virtual environment setup

> ii-scraper> py -m venv ./venv
> ii-scraper> .\venv\scripts\activate.ps1

###### Package installation

> (venv) ii-scraper> pip install selenium
> (venv) ii-scraper> pip install pandas

###### Virtual environment deactivation

> ii-scraper> deactivate

#### Other useful tools used in development

- "XPath Helper Wizard" Chrome plugin
