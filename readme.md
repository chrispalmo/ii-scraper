# ii-scraper-2

---

#### About

ii-scraper-2 is a python script built for members of https://www.intelligentinvestor.com.au/ that extracts, summarizes and analyzes investment recommendations, saving output as an excel ".xlsx" file.

#### Readme

Before running, create "keys.py" in the root directory:

    KEYS = {
        'username': 'YOUR_USERNAME_HERE',
        'password': 'YOUR_PASSWORD_HERE'
    }

#### Project setup notes:

###### Git initialization

> ii-scraper-2> git init .

###### Virtual environment setup

> ii-scraper-2> py -m venv ./venv
> ii-scraper-2> .\venv\scripts\activate.ps1

###### Package installation

> (venv) ii-scraper-2> pip install selenium
> (venv) ii-scraper-2> pip install pandas

###### Virtual environment deactivation

> ii-scraper-2> deactivate

#### Other useful tools used in development

- "XPath Helper Wizard" Chrome plugin
