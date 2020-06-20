# ========================================================================
# Get SUV info from wikipedia, create a file of manufactor, model 
#
from bs4 import BeautifulSoup
import requests

def reducecol(part):
    if part.find("a"):
        part = part.find("a") 
    if  type(part.contents) == list:
        part = part.contents[0]
    return part

url = "https://en.wikipedia.org/wiki/List_of_sport_utility_vehicles"

resp = requests.get(url)
if resp.status_code != 200:
    raise Exception("ERROR: Can't read url: %s" % url)

soup = BeautifulSoup(resp.text, 'html.parser')
table = soup.find("table")
rows = table.findAll("tr")

suvs = []
for row in rows:
    cols = row.findAll("td")
    if len(cols) > 1:
        suvs.append ((reducecol(cols[0]), reducecol(cols[1])))

with open("car.csv","w") as out: 
    for make,model in suvs:
        out.write("'{}','{}'\n".format(make.strip(), model.strip()))

print("Count of cars data is {}".format(len(suvs)))
