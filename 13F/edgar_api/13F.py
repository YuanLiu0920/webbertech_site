from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import pandas as pd
from bs4 import BeautifulSoup

pd.set_option('display.max_rows', None)  
pd.set_option('display.max_columns', None)  
pd.set_option('display.width', None) 
pd.set_option('display.max_colwidth', None)

headers = {
    "User-Agent": "darrenliu101@gmail.com"
}

chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")

#cik_keys (im gonna put this into mysql db so we can just look up them easier):
"""https://www.sec.gov/Archives/edgar/cik-lookup-data.txt"""

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

cik = '1067983'  #replace with any cik number

driver.get(f"https://www.sec.gov/edgar/browse/?CIK={cik}")

# waits for the page to load completely and for the div with data-export
driver.implicitly_wait(20)  

page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")

# finds the htm links associated with 13f filing (first one is always most recent filed)
data_export_div = soup.find("div", {"data-export": "Quarterly report filed by institutional managers, Holdings "})

if data_export_div:
    a_tag = data_export_div.find_all("a", class_="filing-link-all-files")
    if a_tag:
        for link in a_tag:
            href = link.get("href")
            if href and href.endswith(".htm"):
                print("Found the .htm link:", "https://sec.gov" + href)
                break
    else:
        print("No .htm link found within the div.")
else:
    print("Div with the specified data-export attribute not found.")

filing_url = "https://sec.gov" + href
print(filing_url)

response = requests.get(filing_url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    #Date of the 13F filing
    date_div = soup.find('div',class_='formGrouping')

    date = date_div.find('div',class_='info').get_text()

    print(date)

    links = soup.find_all('a', href=True)
    infotable_links = [link.get('href') for link in links if link.get('href').endswith(('.xml'))]
    
    if infotable_links:
        xml_doc_url = f"https://www.sec.gov/{infotable_links[-1]}"
        print("\nLast XML url:", xml_doc_url)
        
        xml_response = requests.get(xml_doc_url, headers=headers)
        xml_content = xml_response.text
        soup = BeautifulSoup(xml_content, 'xml')
        info_tables = soup.find_all('infoTable')
        
        data = []

        for info in info_tables:
            company_name = info.find('nameOfIssuer').text if info.find('nameOfIssuer') else 'None'
            total_value = info.find('value').text if info.find('value') else 'None'
            shares_table = info.find('shrsOrPrnAmt')
            
            if shares_table:
                shares_owned = shares_table.find('sshPrnamt').text if shares_table.find('sshPrnamt') else 'None'
            else:
                shares_owned = 'None'
            
            data.append({'Company Name': company_name,
                         "Total Value": total_value,
                         "Shares Owned": shares_owned})

        df = pd.DataFrame(data)
        
        #prints the dataframe (to showcase stock holdings with total value, and shares owned from each)
        #print(df)
        
    else:
        print("No xml files found.")
else:
    print("Failed to get the filing page")

driver.quit()
