# Note: load_dotenv() will automatically parse the .env file we created earlier 
# and the key/value pair will be loaded into system environment variable which 
# can be accessed via os.getenv() later.

from dotenv import load_dotenv
load_dotenv()

import os
import requests
from bs4 import BeautifulSoup

# Now we will declare several constant variables and use a list to include the items we are interested in getting the update.

# We use os.gentenv() to retrieve the environment variable we set earlier and use the token to form our Telegram /sendMessage API URL, 
# note that we are using f-Strings for TELEGRAM_API_SEND_MSG, it was introduced in Python 3.6 and aim to make string formatting easier and cleaner.
# On the other hand, we can have several entries in items.

BASE_URL = 'https://www.kogan.com/nz/'
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
TELEGRAM_API_SEND_MSG = f'https://api.telegram/bot{TOKEN}/sendMessage'

items = [
    'buy/kogan-35-curved-219-ultrawide-75hz-freesync-gaming-monitor-b/',
    'buy/kogan-full-rgb-mechanical-keyboard-brown-switch/'
]

# Finally, we use a loop to go through the items and scrape their name and price using BeautifulSoup’s HTML parser, 
# then send the data to Telegram API using our TOKEN and CHAT_ID.

def main(event={}, context={}):
    for item in items:
        url = BASE_URL + item
        r = requests.get(url)

        # Note: With BeautifulSoup, we can use CSS selectors to traverse through HTML and find our element of interest then extract data out of it.
        
        soup = BeautifulSoup(r.text, 'html.parser')
        name = soup.select_one('h1[itemprop="name"]').get_text()
        price = soup.select_one('h3[itemprop="price"]')['content']

        # The data dictionary contains the parameters to be sent to Telegram /sendMessage API using POST request. 
        # chat_id and text are required parameters while parse_mode is an optional one, we use Markdown parse mode to show bold and inline URL in our message.

        data = {
            'chat_id': CHAT_ID,
            'text': f'*${price}*\n[{name}]({url})',
            'parse_mode': 'Markdown'
        }

        r = requests.post(TELEGRAM_API_SEND_MSG, data=data)

if __name__ == '__main__':
    main()
