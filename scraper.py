import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Function to scrape top gaming desktop CPUs
def get_top_desktop_cpus():
    url = "https://www.cpubenchmark.net/top-gaming-cpus.html"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch CPU benchmark page.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    chart_list = soup.find("ul", class_="chartlist")

    cpus = []
    if chart_list:
        for li in chart_list.find_all("li", class_="platform-cpu"):
            if "desktop" not in li.get("class", []):
                continue
            name_tag = li.find("span", class_="prdname")
            score_tag = li.find("span", class_="count")
            if name_tag and score_tag:
                name = name_tag.text.strip()
                score = score_tag.text.strip().replace(",", "")
                cpus.append((name, score))
    return cpus

# Function to get lowest price of CPU from salidzini.lv
def get_cpu_price_selenium(cpu_name, driver):
    base_url = "https://www.salidzini.lv/cena?q="
    query = quote_plus(cpu_name)
    full_url = base_url + query

    try:
        driver.get(full_url)
        # Wait for page to load (can adjust time or use WebDriverWait)
        time.sleep(random.uniform(3, 5))

        # Extract prices using regex or by element class
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        price_spans = soup.select("div.item_price span")

        prices = []
        for span in price_spans:
            try:
                price_text = span.get_text().replace(",", ".").replace(" ", "")
                price = float(price_text)
                prices.append(price)
            except ValueError:
                continue

        if not prices:
            print(soup.prettify())
        return min(prices) if prices else None
    except Exception as e:
        print(f"Error scraping price for {cpu_name}: {e}")
        return None

# Main execution
def main():
    cpus = get_top_desktop_cpus()

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without GUI

    driver = webdriver.Chrome(options=chrome_options)

    print("Top Gaming Desktop CPUs with Prices in Latvia:\n")
    for i, (name, score) in enumerate(cpus[:5], 1):
        # price = get_cpu_price(name, session)
        price = get_cpu_price_selenium(name, driver)
        price_str = f"€{price:.2f}" if price else "Not Found"
        print(f"{i}. {name} - Score: {score} - Price: {price_str}")
        time.sleep(random.uniform(1, 4))

    driver.quit()

if __name__ == "__main__":
    main()
