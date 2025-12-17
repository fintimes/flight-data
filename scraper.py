import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

def scrape_moca():
    url = "https://www.civilaviation.gov.in/in-focus"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table') # Targets the main data table
        
        if not table:
            return

        rows = table.find_all('tr')
        data_to_save = []
        
        for row in rows[1:]: # Skip header
            cols = [td.text.strip() for td in row.find_all('td')]
            if cols:
                # Add a timestamp so you know when it was collected
                cols.insert(0, datetime.now().strftime("%Y-%m-%d"))
                data_to_save.append(cols)

        file_path = 'moca_data.csv'
        file_exists = os.path.isfile(file_path)

        with open(file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['ScrapeDate', 'S.No', 'Title', 'Type', 'Date', 'Download'])
            writer.writerows(data_to_save)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_moca()
