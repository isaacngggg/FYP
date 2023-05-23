#%%
import sqlite3
import csv
import pandas as pd
import os


## connect to the sqlite database
conn = sqlite3.connect("numpy_items.db")

## set up cursor to use any SQL commands
c = conn.cursor()

## create the table but you can't execute this twice

# cur.execute("""
#     CREATE TABLE functions(
#         title text,
#         description text,
#         linking_urls text
#     )
# """)

# ## Read files from a sibiling file directory: https://www.geeksforgeeks.org/python-read-file-from-sibling-directory/
# path = os.path.realpath(__file__)
# dir = os.path.dirname(path)
# dir = dir.replace('Database','Documentation_Scraper')

# # Change the directory to Documentation Scraper
# os.chdir(dir)

# df = pd.read_csv('numpy_items.csv')


df = pd.read_csv('numpy_items.csv')
df.to_sql('numpy_functions', conn, if_exists='append', index=False)

## committing those changes to the database
conn.commit()

## closing the database
conn.close()

#%%
conn = sqlite3.connect("numpy_items.db")

## set up cursor to use any SQL commands
c = conn.cursor()

c.execute("SELECT * FROM numpy_functions")

print(c.fetchall())



