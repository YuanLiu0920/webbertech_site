import React, { useEffect, useState } from 'react';
import './index.css';

interface BankAccount {
  id: number;
  bank_name: string;
  account_name: string;
  account_number: string;
  routing_number: string;
  deposit_amount: number;
  current_amount: number;
  maturity_date: string;
  current_rate: string;
  comments: string;
}

const BankAccounts: React.FC = () => {
  const [accounts, setAccounts] = useState<BankAccount[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    fetch('/api/bank_accounts')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data: BankAccount[]) => {
        setAccounts(data);
        setLoading(false);
      })
      .catch((err: Error) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading bank accounts...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h2>Bank Accounts</h2>
      <table className="table-with-border">
        <thead>
          <tr>
            <th>ID</th>
            <th>Bank Name</th>
            <th>Account Name</th>
            <th>Account Number</th>
            <th>Routing Number</th>
            <th>Current Amount</th>
            <th>Maturity Date</th>
          </tr>
        </thead>
        <tbody>
          {accounts.map((account) => (
            <tr key={account.id}>
              <td>{account.id}</td>
              <td>{account.bank_name}</td>
              <td>{account.account_name}</td>
              <td>{account.account_number}</td>
              <td>{account.routing_number}</td>
              <td>{account.current_amount}</td>
              <td>{account.maturity_date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BankAccounts;
