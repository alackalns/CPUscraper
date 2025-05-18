import requests
from bs4 import BeautifulSoup

url = "https://www.cpubenchmark.net/top-gaming-cpus.html"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(f"Failed to retrieve page. Status: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# Locate the chart list container
chart_list = soup.find("ul", class_="chartlist")

cpus = []
if chart_list:
    for li in chart_list.find_all("li", class_="platform-cpu"):
        name_tag = li.find("span", class_="prdname")
        score_tag = li.find("span", class_="count")


        if name_tag and score_tag:
            name = name_tag.text.strip()
            score = score_tag.text.strip()
            cpus.append((name, score))

# Display results
print("Top Gaming CPUs:\n")
for i, (name, score) in enumerate(cpus, 1):
    print(f"{i}. {name} - Score: {score}")
