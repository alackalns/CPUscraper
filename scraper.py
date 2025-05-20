import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from tqdm import tqdm
import time
import random

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
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.item_price span"))
        )

        items = driver.find_elements(By.CSS_SELECTOR, "div.item_box_sub")  # Each item block
        lowest_price = float("inf")
        lowest_link = None

        for item in items:
            try:
                price_span = item.find_element(By.CSS_SELECTOR, "div.item_price span")
                price_text = price_span.text.replace(",", ".").replace(" ", "")
                price = float(price_text)

                link_tag = item.find_element(By.CSS_SELECTOR, "a.item_link")
                item_link = link_tag.get_attribute("href")

                if price < lowest_price:
                    lowest_price = price
                    lowest_link = item_link
            except Exception:
                continue

        return (lowest_price if lowest_price != float("inf") else None, lowest_link)
    except Exception as e:
        print(f"Error scraping price for {cpu_name}: {e}")
        return None, None

# Main execution
def main():
    cpus = get_top_desktop_cpus()

    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless")  # Run without GUI
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    driver = uc.Chrome(options=chrome_options)

    print("Top Gaming Desktop CPUs with Prices in Latvia:")
    cpu_data = []
    for i, (name, score) in enumerate(tqdm(cpus[:5], desc="Scraping CPUs"), 1):
        price, link = get_cpu_price_selenium(name, driver)
        try:
            score_val = float(score)
        except ValueError:
            score_val = None

        if price and score_val:
            score_per_eur = score_val / price
            score_per_eur_str = f"{score_per_eur:.2f}"
        else:
            score_per_eur_str = "N/A"

        price_str = f"€{price:.2f}" if price else "Not Found"
        link_str = link if link else "No Link Found"

        cpu_data.append({
            "Rank": i,
            "CPU Name": name,
            "Score": score,
            "Price (EUR)": price_str,
            "Score/EUR": score_per_eur_str,
            "Link": link_str
        })

        if i < len(cpus[:5]):
            time.sleep(random.uniform(0.5, 1.5))

    driver.quit()

    df = pd.DataFrame(cpu_data)
    df.to_excel("cpus.xlsx", index=False)
    print("\nData has been exported to 'cpus.xlsx'.")

if __name__ == "__main__":
    main()
