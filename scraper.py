import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

def scrape_moca_dashboard():
    url = "https://www.civilaviation.gov.in/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This dictionary will store our data row
        row_data = {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}
        
        # Target the dashboard items based on the classes seen in the site source
        items = soup.find_all('div', class_='views-field')
        
        for item in items:
            label = item.find('span', class_='views-label')
            value = item.find('span', class_='field-content')
            
            if label and value:
                clean_label = label.text.strip().replace(":", "")
                clean_value = value.text.strip().replace(",", "")
                if clean_value: # Only add if there's actual data
                    row_data[clean_label] = clean_value

        if len(row_data) > 1:
            file_path = 'moca_data.csv'
            file_exists = os.path.isfile(file_path)
            
            # Using DictWriter ensures data aligns even if the site adds new categories
            with open(file_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=row_data.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(row_data)
            print("Successfully updated moca_data.csv")
        else:
            print("Search failed: No data found in the dashboard containers.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_moca_dashboard()
