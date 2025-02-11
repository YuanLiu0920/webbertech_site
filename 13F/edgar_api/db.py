import mysql.connector
import re

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="darrenliu",
    database="13f"
)
cursor = db.cursor()

with open(r"13F/edgar_api/cik-lookup-data.txt", "r") as file:
    for line in file:
        if line.strip():
            match = re.match(r"(.*?)(\d{10})\s*:", line.strip())
            if match:
                company_name = match.group(1).strip()  
                cik_key = match.group(2).strip() 
                print(f"Company Name: {company_name}, CIK: {cik_key}")
                cursor.execute("INSERT INTO companies (company_name, cik_key) VALUES (%s, %s)", (company_name, cik_key))
            else:
                print(f"No match for line: {line.strip()}")

db.commit()
cursor.close()
db.close()
