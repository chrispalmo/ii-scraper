import keys

"""
create "keys.py" file containing the below:

KEYS = {
    'username': '[INSERT_USERNAME_HERE]',
    'password': '[INSERT_PASSWORD_HERE]'
}

"""

KEYS = keys.KEYS

DRIVER_LOCATION = r'C:\Users\chris\Dropbox\PythonProjects\II_scraper\chromedriver.exe'

DEV_MODE = False #if config.DEV_MODE: (Load data from pickle file) else (start chrome and scrape)
LOAD_PICKLE_NAME = 'test_data.pickle'
SAVE_PICKLE = True
SAVE_PICKLE_NAME = 'test_data.pickle'
