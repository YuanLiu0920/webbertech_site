# 13F Database

---------------------------------------------
The database supports financial analysis and investment research by storing and organizing data on 13F stock holdings of 
institutions/companies. It allows users to track company ownership trends, analyze investment strategies, and monitor regulatory 
filings efficiently.
---------------------------------------------

## How to run the code

### Step 1 install python package

* `pip3 install pandas`
* `pip3 install bs4`
* `pip3 install lxml`
* `pip3 install webdriver-manager`

In ubuntu, run the following,

`sudo apt install chromium-chromedriver`

### Test driver

It is a binary,

```
(base) xiaofengli@xiaofenglx:~/git/webbertech_site/13F/edgar_sec$ chromedriver
Starting ChromeDriver 133.0.6943.53 (9a80935019b0925b01cc21d254da203bc3986f04-refs/branch-heads/6943@{#1389}) on port 0
Only local connections are allowed.
Please see https://chromedriver.chromium.org/security-considerations for suggestions on keeping ChromeDriver safe.
ChromeDriver was started successfully on port 36357.
(base) xiaofengli@xiaofenglx:~/git/webbertech_site/13F/edgar_sec$ which chromedriver
/usr/bin/chromedriver
```

Run `headless_chrome_driver_test.py` and make sure you don't see any crash or errors.

### Step 2

Run `13F.py`

## CIK

Stores information about companies that have investment holdings reported in 13F filings.
Each company is uniquely identified by a CIK (Central Index Key), a 10-digit identifier assigned by the SEC.

**cik-lookup-data.txt:** [How did we get this file? Not being used?]
Contains all public & private companies names and corresponding identifier of a 10-digit CIK key

---------------------------------------------

- id - The index corresponding to the company_name and cik_key.

- company_name - The name of the institution/company.

- cik_key - a 10 digit number associated with corresponding institution/company.

---------------------------------------------

## Database Schema

1. companies table:

-- `13f`.companies definition

```sql
CREATE TABLE `companies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `company_name` varchar(255) NOT NULL,
  `cik_key` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1969019 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

2. stock_holdings Table:

-- `13f`.stock_holdings definition

```sql
CREATE TABLE `stock_holdings_snapshot` (
  `cik_key` varchar(20),
  `holding_name` varchar(255) DEFAULT NULL,
  `value` varchar(20) DEFAULT NULL,
  `shares_owned` varchar(20) DEFAULT NULL,
  `filing_date` date DEFAULT NULL,
  `snapshot_date` date DEFAULT Date(),
  PRIMARY KEY (`cik_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

The idea is that for certain company, for all the aggregation of one stock, we can see the holdings of shares are deceasing or increasing 
compared with last filing.

## Business Logic

---------------------------------------------
Captures detailed stock holdings reported by institutional investors.

Each entry is linked to a company via the cik_key, establishing a relationship between investment firms and their holdings.

---------------------------------------------
Holding Name – The name of the security held.
Total Value – The reported value of the holdings.
Shares Owned – The number of shares held at the time of filing.
Filing Date – The date the 13F report was filed.
---------------------------------------------


## TODO

**Use CIK Lookup API from python package** (Don't do this yet)
https://sec-edgar.github.io/sec-edgar/about.html

Please see `CIKLookupTest.py`, and we find it is actually parsing the following json file.

https://www.sec.gov/files/company_tickers.json

**https://www.sec.gov/Archives/edgar/data/1067983/000095012325002701/xslForm13F_X02/39042.xml** (High priority)

Just pandas import the link, aggregate using groupBy companies on columns 4 and 5.
Verify total holding and total value of each stock of the top 5 using third party website or resources.
Try to understand 13F format.

**https://www.sec.gov/files/company_tickers.json** (check the following ids are findable)

1350694,1037389,1610520

Worse secario, manual lookup.

**Future Updates:**
---------------------------------------------
TODO: Planning to add changes to stock_holdings so FK cik_key in companies table references PK cik_key in stock_holdings table

## Ref

- https://www.sec.gov/submit-filings/filer-support-resources/how-do-i-guides/look-central-index-key-cik-number
- https://www.sec.gov/search-filings/cik-lookup
- https://www.edgarcompany.sec.gov/