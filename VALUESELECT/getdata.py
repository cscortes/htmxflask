# ========================================================================
# Sample Data Retrieval Script
# 
# This script demonstrates how to scrape car data from Wikipedia to create
# the car.csv file used by the VALUESELECT example.
#
# Usage: python getdata.py
# Output: Creates car.csv with make,model pairs
# ========================================================================

from bs4 import BeautifulSoup
import requests

def reducecol(part):
    """Extract text content from BeautifulSoup element, handling nested links."""
    if part.find("a"):
        part = part.find("a") 
    if type(part.contents) == list:
        part = part.contents[0]
    return part

# Wikipedia URL containing SUV data
url = "https://en.wikipedia.org/wiki/List_of_sport_utility_vehicles"

print("Fetching SUV data from Wikipedia...")
resp = requests.get(url)
if resp.status_code != 200:
    raise Exception("ERROR: Can't read url: %s" % url)

print("Parsing HTML content...")
soup = BeautifulSoup(resp.text, 'html.parser')
table = soup.find("table")
rows = table.findAll("tr")

# Extract make and model data from table rows
suvs = []
for row in rows:
    cols = row.findAll("td")
    if len(cols) > 1:
        make = reducecol(cols[0])
        model = reducecol(cols[1])
        suvs.append((make, model))

# Write data to CSV file
print("Writing data to car.csv...")
with open("car.csv", "w") as out: 
    for make, model in suvs:
        out.write("'{}','{}'\n".format(make.strip(), model.strip()))

print("Successfully created car.csv with {} car entries".format(len(suvs)))
print("Data includes makes and models from the Wikipedia SUV list")
