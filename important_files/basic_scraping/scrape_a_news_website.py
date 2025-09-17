from bs4 import BeautifulSoup
import requests
import json
import csv

# Extracts the News title and the link to the page and stores it in a JSON file and a csv file

url = "https://www.thehindu.com/sci-tech/technology/?page=1"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
raw = requests.get(url, headers=headers)

soup = BeautifulSoup(raw.text, 'html.parser')
# To use lxml we need to install it: pip install lxml

articles = soup.find_all('div', class_="element")

# Title And rows definition for storing data to be exported to CSV files
fields = ["Title", "URL"]
rows = []

# This is to store the Dictionary data to be converted to JSON
news_list = []
for item in articles:
    if item:
        heading_full = item.find("h3", class_="title big")
        if heading_full:
            link_tag = heading_full.find("a")
            if link_tag and link_tag.has_attr('href'):  # check if the link tag has the attribute href
                title = link_tag.text.strip()   # strip off the extra white spaces from the title
                link = link_tag['href']     # Extract the link
                print(title)
                print(link)
                print()
                news_list.append({"title": title, "link": link})
                rows.append([title, link])

# Sve as JSON
with open("news_data.json", "w", encoding="utf-8") as f:
    json.dump(news_list, f, indent=4, ensure_ascii=False)
print("\n\nJSON File Saved!")

# Save as CSV
with open("news_data.csv", "w", encoding="utf-8") as f:
    # Create a csv writer object
    csvwriter = csv.writer(f)
    # Write the data 
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)
print("CSV File Saved!")
# The encoding and ansure_ascii is not strictly necassary but useful while handling non-ASCII charecters
