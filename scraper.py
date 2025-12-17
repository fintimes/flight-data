import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

def scrape_moca_dashboard():
    url = "https://www.civilaviation.gov.in/"
    # Headers make the request look like a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # The data in your image is stored in 'views-row' or card containers
        # We will extract all labels and their corresponding numbers
        stats = {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}
        
        # Target the specific blocks for Domestic and International Traffic
        cards = soup.find_all('div', class_='views-field')
        
        for card in cards:
            label_tag = card.find('span', class_='views-label')
            value_tag = card.find('span', class_='field-content')
            
            if label_tag and value_tag:
                label = label_tag.text.strip().replace(":", "")
                value = value_tag.text.strip()
                if value: # Only add if there is a number
                    stats[label] = value

        if len(stats) > 1:
            file_path = 'moca_data.csv'
            file_exists = os.path.isfile(file_path)
            
            with open(file_path, 'a', newline='', encoding='utf-8') as f:
                # Use DictWriter to handle varying columns if the site updates
                writer = csv.DictWriter(f, fieldnames=stats.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(stats)
            print("Data captured successfully.")
        else:
            print("Could not find dashboard data. The site structure may have changed.")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    scrape_moca_dashboard()
