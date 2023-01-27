import pandas as pd
import urllib
import requests
from bs4 import BeautifulSoup

df = pd.read_csv('C:\\Workspace\\thesis\\boundaries\\tribes_pnw_4326.csv')

for tribe in df['NAMELSAD'].values:
    query = tribe + " tribe flag"
    print(query)
