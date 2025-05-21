import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import pandas as pd
from tqdm import tqdm
import time
import random

def get_cpu_price_from_dateks(cpu_name):
    base_url = "https://www.dateks.lv/meklet?q="
    query = quote_plus(cpu_name)
    full_url = base_url + query
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36"
    }

    try:
        response = requests.get(full_url, headers=headers, timeout=12)
        if response.status_code != 200:
            print(f"Failed to fetch CPU: {cpu_name} price page.")
            return None, None

        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.select("div.prod")

        if not products:
            return None, None

        lowest_price = float("inf")
        lowest_link = None

        for prod in products:
            try:
                price_text = prod.select_one("div.price-info div.price").text.strip()
                price = float(price_text.replace("€", "").replace(",", ".").replace(" ", ""))

                relative_link = prod.select_one("a.imp")["href"]
                full_link = "https://www.dateks.lv" + relative_link

                if price < lowest_price:
                    lowest_price = price
                    lowest_link = full_link

            except Exception:
                continue

        return (lowest_price if lowest_price != float("inf") else None, lowest_link)

    except Exception as e:
        print(f"Error scraping price for {cpu_name}: {e}")
        return None, None


# Function to scrape top gaming desktop CPUs
def get_top_desktop_cpus():
    url = "https://www.cpubenchmark.net/top-gaming-cpus.html"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch CPU benchmark page.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    chart_list = soup.find("ul", class_="chartlist")

    cpus = LinkedList()
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

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.length = 0

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node
        self.length += 1

    def __iter__(self):
        self._iter_node = self.head
        return self

    def __next__(self):
        if not self._iter_node:
            raise StopIteration
        data = self._iter_node.data
        self._iter_node = self._iter_node.next
        return data

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def __len__(self):
        return self.length

# Main execution
def main():
    cpus = get_top_desktop_cpus()
    print("Top Gaming Desktop CPUs with Prices in Latvia:")

    cpu_data = LinkedList()

    for i, (name, score) in enumerate(tqdm(cpus, desc="Scraping CPUs")):
        price, link = get_cpu_price_from_dateks(name)

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
            "CPU Name": name,
            "Score": score,
            "Price (EUR)": price_str,
            "Score/EUR": score_per_eur_str,
            "Link": link_str
        })

        if i < len(cpus):
            time.sleep(random.uniform(0.5, 1.5))  # Random sleep to avoid being blocked

    # Convert linked list to regular list for DataFrame export
    df = pd.DataFrame(cpu_data.to_list())
    df.to_excel("cpus.xlsx", index=False)
    print("\nData has been exported to 'cpus.xlsx'.")

if __name__ == "__main__":
    main()
