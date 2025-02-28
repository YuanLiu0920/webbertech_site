from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
from bs4 import BeautifulSoup

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

"""
param: cik_key (https://www.sec.gov/files/company_tickers.json)
return: the source code of the url of the following,
 
https://www.sec.gov/edgar/browse/?cik=1350694

For invert and forward search of company name using Edgar Search please refer to the URLs in the README.md in this folder.
"""
def get_page_source(cik_key):
    # required to access sec gov pages (via documentation)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")
    chrome_path = ChromeDriverManager().install()
    print("debugging")
    print(chrome_path)
    if "THIRD_PARTY_NOTICES.chromedriver" in chrome_path:
        chrome_path = chrome_path.replace("THIRD_PARTY_NOTICES.chromedriver", "chromedriver")
    service = Service(chrome_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(f"https://www.sec.gov/edgar/browse/?cik={cik_key}")
    driver.implicitly_wait(20)

    page_source = driver.page_source
    driver.quit()
    return page_source

""" 
param: cik_key
return: top holdings of the specified company.


"""
def find_stock_holdings(cik_key):
    page_source = get_page_source(cik_key)
    soup = BeautifulSoup(page_source, "html.parser")

    # finds first htm link on the sec gov page and then fetches it
    def find_htm_link():
        data_export_div = soup.find("div", {"data-export": "Quarterly report filed by institutional managers, Holdings "})

        if data_export_div:
            a_tag = data_export_div.find_all("a", class_="filing-link-all-files")
            if a_tag:
                href = a_tag[0].get("href")  
                filing_url = "https://sec.gov" + href
                print("Found the .htm link:", filing_url)
                return filing_url
            else:
                print("No .htm link found within the div.")
        else:
            print("Div with the data-export attribute not found.")

    headers = {
        "User-Agent": "darrenliu101@gmail.com"
    }
    response = requests.get(find_htm_link(), headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        date_div = soup.find('div', class_='formGrouping')
        filing_date = date_div.find('div', class_='info').get_text().strip()

        links = soup.find_all('a', href=True)
        # eg:
        # `url: https://www.sec.gov/Archives/edgar/data/1350694/000117266125000823/0001172661-25-000823-index.htm`
        infotable_links = [link.get('href') for link in links if link.get('href').endswith('.xml')]
        if infotable_links:
            # eg:
            # https://www.sec.gov/Archives/edgar/data/1350694/000117266125000823/infotable.xml
            xml_doc_url = f"https://www.sec.gov/{infotable_links[-1]}"

            print("\nLast XML url:", xml_doc_url)

            xml_response = requests.get(xml_doc_url, headers=headers)
            xml_content = xml_response.text
            soup = BeautifulSoup(xml_content, 'xml')
            info_tables = soup.find_all('infoTable')

            data = []
            for info in info_tables:
                company_name = info.find('nameOfIssuer').text if info.find('nameOfIssuer') else 'None'
                total_value = int(info.find('value').text) if info.find('value') else 0
                shares_table = info.find('shrsOrPrnAmt')
                shares_owned = int(shares_table.find('sshPrnamt').text) if shares_table and shares_table.find('sshPrnamt') else 0

                data.append({'Company Name': company_name,
                            "Total Value": total_value,
                            "Shares Owned": shares_owned,
                            "Filing Date": filing_date
                            })        

            df = pd.DataFrame(data)
            df = df.groupby('Company Name', as_index=False).agg({
                'Total Value': 'sum',
                'Shares Owned': 'sum',
                'Filing Date': 'first'
            })

            df.sort_values(by='Total Value', ascending=False, inplace=True)

            # Convert shares and total value of each stock held into billions(B), millions(M), & K depending on the value
            def divisibleBy(number):
                string = ''
                if number >= 1000000000: 
                    string =  str(round(number / 1000000000)) + "B"
                elif number >= 1000000:  
                    string = str(round(number / 1000000)) + "M"
                else:
                    string = str(round(number / 1000)) + "K"
                return string
        
            df['Total Value'] = df['Total Value'].astype(str)
            df['Shares Owned'] = df['Shares Owned'].astype(str)

            for index, row in df.iterrows():
                total_value = int(row['Total Value'])
                shares_owned = int(row['Shares Owned'])

                df.at[index, 'Total Value'] = divisibleBy(total_value)
                df.at[index, 'Shares Owned'] = divisibleBy(shares_owned)
            
            return df

        else:
            print("No XML files found.")
    else:
        print("Failed to get the filing page")



"""
Finds overlapping stocks based on *args number of stock dataframes placed into the parameter
Make sure you use the find_stock_holdings() function to generate stock holding dataframes and 
input them into this function.
"""
def aggregate_holdings(*args):
    if not args:
        return "No DataFrame/s provided."

    company_sets = [set(df['Company Name']) for df in args if 'Company Name' in df.columns]

    if not company_sets:
        return "No 'Company Name' column found in any DataFrame."

    overlapping_stocks = set.intersection(*company_sets)

    if not overlapping_stocks:
        return "No matches found."

    return ", ".join(overlapping_stocks)

#Feature 1 - Aggregating Stocks from various companies (10 digit number is cik key)
find_stock_holdings('0001350694')

#Feature 2 - Aggregating Stocks from various companies to get shared overlapping stocks (10 digit number is cik key)

def find_common_holdings_multi_cik():
    df1 = find_stock_holdings('1350694')  # Bridgewater Associates
    df2 = find_stock_holdings('1067983')  # Berkshire Hathaway
    df3 = find_stock_holdings('1037389')  # Renaissance Technologies
    df4 = find_stock_holdings('1610520')  # UBS Group AG
    same_holdings = aggregate_holdings(df1, df2, df3, df4)

    # TODO Print all original names of the company from CIK
    print("\nSame Stock Holdings:")
    print(same_holdings)

if __name__ == "__main__":
    find_common_holdings_multi_cik()