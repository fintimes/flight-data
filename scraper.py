import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

def scrape_moca_dashboard():
    url = "https://www.civilaviation.gov.in/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This targets the 'Domestic Traffic' and 'International Traffic' sections
        data_points = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Looking for the specific text labels and their associated numbers
        # The MoCA site uses specific classes for these dashboard items
        items = soup.find_all('div', class_='views-field')
        
        extracted_values = {"Timestamp": timestamp}
        
        for item in items:
            label = item.find('span', class_='views-label')
            value = item.find('span', class_='field-content')
            
            if label and value:
                clean_label = label.text.strip().replace(":", "")
                clean_value = value.text.strip().replace(",", "")
                extracted_values[clean_label] = clean_value

        if len(extracted_values) > 1:
            file_path = 'moca_dashboard.csv'
            file_exists = os.path.isfile(file_path)
            
            with open(file_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=extracted_values.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(extracted_values)
            print("Dashboard data updated successfully.")
        else:
            print("No dashboard data found. The site structure may have changed.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_moca_dashboard()
