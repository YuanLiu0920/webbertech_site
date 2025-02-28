# 13F Database

---------------------------------------------
The database supports financial analysis and investment research by storing and organizing data on 13F stock holdings of institutions/company. It allows users to track company ownership trends, analyze investment strategies, and monitor regulatory filings efficiently.


## Database Schema:


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

**CIK**

Stores information about companies that have investment holdings reported in 13F filings.
Each company is uniquely identified by a CIK (Central Index Key), a 10-digit identifier assigned by the SEC.

---------------------------------------------
id - The index corresponding to the company_name and cik_key.
company_name - The name of the institution/company.
cik_key - a 10 digit number associated with corresponding institution/company.
---------------------------------------------

**cik-lookup-data.txt:** [How did we get this file?]
Contains all public & private companies names and corresponding identifier of a 10-digit CIK key

2. stock_holdings Table:

-- `13f`.stock_holdings definition

```sql
CREATE TABLE `stock_holdings` (
  `cik_key` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `holding_name` varchar(255) DEFAULT NULL,
  `total_value` varchar(20) DEFAULT NULL,
  `shares_owned` varchar(20) DEFAULT NULL,
  `filing_date` date DEFAULT NULL,
  PRIMARY KEY (`cik_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

---------------------------------------------
Captures detailed stock holdings reported by institutional investors.

Each entry is linked to a company via the cik_key, establishing a relationship between investment firms and their holdings.

---------------------------------------------
Holding Name – The name of the security held.
Total Value – The reported value of the holdings.
Shares Owned – The number of shares held at the time of filing.
Filing Date – The date the 13F report was filed.
---------------------------------------------


**Future Updates:**
---------------------------------------------
TODO: Planning to add changes to stock_holdings so FK cik_key in companies table references PK cik_key in stock_holdings table
