import requests
import json
from collections import Counter
from bs4 import BeautifulSoup
import pandas as pandas

with open("13F/13f.info/13f-urls.json","r") as urls:
    if urls:
        companies_file = json.load(urls)
    else:
        print("error")

companies = companies_file.get("companies")

companies_data = []

for company_url in companies:
  response = requests.get(company_url)
  scraper = BeautifulSoup(response.text, "html.parser")
  
  most_recent_filing = scraper.find('span', class_="group-hover:bg-white group-hover:relative group-hover:px-1 group-hover:-ml-1 group-hover:rounded group-hover:shadow")
  company_name = scraper.find('h1', class_="leading-8 mb-2").get_text().strip()
  
  if most_recent_filing:
      companies_data.append({
          "Company Name": company_name,
          "Most Recent Stocks Filed": most_recent_filing.text.strip()
      })
  else:
      companies_data.append({
          "Company Name": company_name,
          "Most Recent Stocks Filed": "STOCKS NOT FOUND."
      })
1

company_and_stocks = pandas.DataFrame(companies_data)
company_and_stocks.index += 1




"""Shows company names along with most recent stock filings for 13F quarter"""
def recent_company_stock_filing():
  print(company_and_stocks)


"""Shows accumlated stock holdings from most to least in the most recent 13F quarter"""
def most_stocks_held():
  all_stocks = []

  for stock_list in company_and_stocks['Most Recent Stocks Filed']:
      if stock_list != "STOCKS NOT FOUND.":
          all_stocks.extend(stock_list.split(', '))

  stock_counts = Counter(all_stocks)
  stock_counts_df = pandas.DataFrame(stock_counts.items(), columns=['Stock', 'Count'])
  sorted_stock_counts_df = stock_counts_df.sort_values(by='Count', ascending=False)
  sorted_stock_counts_df = sorted_stock_counts_df.reset_index(drop=True)
  sorted_stock_counts_df.index = sorted_stock_counts_df.index + 1
  
  print(sorted_stock_counts_df)


if __name__ == '__main__':
    recent_company_stock_filing()
    most_stocks_held()