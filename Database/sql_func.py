import sqlite3
import csv
import pandas as pd
import os


conn = sqlite3.connect(":memory:")
c = conn.cursor()

# Change the directory to Documentation Scraper
path = os.path.realpath(__file__)
dir = os.path.dirname(path)
dir = dir.replace('Database','Documentation_Scraper')
os.chdir(dir)
df = pd.read_csv('numpy_items.csv')

df.to_sql('numpy_functions', conn, if_exists='append', index=False)


def get_func_by_name(func):
    c.execute("SELECT * FROM numpy_functions WHERE title = :title", {'title': func})
    return c.fetchall()

while (1):
    print (get_func_by_name('numpy.' + input("Search numpy function: numpy.")))

