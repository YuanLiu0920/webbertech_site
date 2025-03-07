import React, { useEffect, useState } from 'react';
import BankAccounts from './BankAccounts';
import StockList from './StockList';

const App: React.FC = () => {

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/health', { cache: "no-store" })
      .then((response) => response.json())
      .then((data) => {
        console.log("Tables received:", data);
      })
      .catch((err) => console.error("❌ Error fetching tables:", err));
  }, []);

  return (
    <div className="App">
      <h1>Investment Tracker</h1>
      <BankAccounts />
    </div>
  );
};

export default App;
