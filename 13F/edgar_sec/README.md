Database Schema 

-- `13f`.companies definition
CREATE TABLE `companies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `company_name` varchar(255) NOT NULL,
  `cik_key` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1969019 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- `13f`.stock_holdings definition
CREATE TABLE `stock_holdings` (
  `cik_key` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `holding_name` varchar(255) DEFAULT NULL,
  `total_value` varchar(20) DEFAULT NULL,
  `shares_owned` varchar(20) DEFAULT NULL,
  `filing_date` date DEFAULT NULL,
  PRIMARY KEY (`cik_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

cik-lookup-data.txt contains all public & private companies along with their corresponding CIK keys

TODO: Planning to add changes to stock_holdings so FK cik_key in companies table references PK cik_key in stock_holdings table