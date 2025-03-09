import React, { useEffect, useState } from 'react';
import './index.css';

 {/*
      (id, bond_name, bond_type, bond_term, amount, maturity_date, apy, platform, comment)*/}
interface Bond {
  id: number;
  bond_name: string;
  bond_type: string;
  bond_term: string;
  amount: number;
  maturity_date: string;
  apy: number;
  platform: string;
  comment: string;
}

const Bonds: React.FC = () => {
  const [bonds, setBonds] = useState<Bond[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    fetch('/api/bonds')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data: Bond[]) => {
        setBonds(data);
        setLoading(false);
      })
      .catch((err: Error) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading bonds accounts...</p>;
  if (error) return <p>Error: {error}</p>;


  return (
    <div>
      <h2>Bonds</h2>
      <table className="table-with-border">
        <thead>
          <tr>
            <th>ID</th>
            <th>bond_name</th>
            <th>bond_type</th>
            <th>bond_term</th>
            <th>amount</th>
            <th>maturity_date</th>
            <th>apy</th>
            <th>platform</th>
            <th>comment</th>
          </tr>
        </thead>
        <tbody>
          {bonds.map((it) => (
            <tr key={it.id}>
              <td>{it.id}</td>
              <td>{it.bond_name}</td>
              <td>{it.bond_type}</td>
              <td>{it.bond_term}</td>
              <td>{it.amount}</td>
              <td>{it.maturity_date}</td>
              <td>{it.apy}</td>
               <td>{it.platform}</td>
               <td>{it.comment}</td>

            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Bonds;
