import React, { useEffect, useState } from 'react';
import BankAccounts from './BankAccounts';
import StockList from './StockList';  // ✅ Import StockList

const App: React.FC = () => {
  const [tables, setTables] = useState<string[]>([]);
  const [selectedTable, setSelectedTable] = useState<string | null>(null);  // ✅ Declare selectedTable

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/tables', { cache: "no-store" })
      .then((response) => response.json())
      .then((data) => {
        console.log("📌 Tables received:", data);
        setTables(data);
        if (data.length > 0) {
          setSelectedTable(data[0]); // Default to first table
        }
      })
      .catch((err) => console.error("❌ Error fetching tables:", err));
  }, []);

  return (
    <div className="App">
      <h1>Investment Tracker</h1>

      {/* Debugging: Show API response */}
      <p>Available Tables (Debug): {JSON.stringify(tables)}</p>

      {/* Buttons to switch between tables */}
      <div>
        {tables.length === 0 ? (
          <p>Loading tables...</p>
        ) : (
          tables.map((table) => (
            <button key={table} onClick={() => setSelectedTable(table)}>
              Show {table.replace('_', ' ')}
            </button>
          ))
        )}
      </div>

      <p>Selected Table: {selectedTable}</p>

      {/* Conditionally Render Tables */}
      {selectedTable === "bank_accounts" && <BankAccounts />}
      {selectedTable === "stocks" && <StockList />}
      {selectedTable === "bond" && <p>Bonds will be displayed here!</p>}
    </div>
  );
};

export default App;
