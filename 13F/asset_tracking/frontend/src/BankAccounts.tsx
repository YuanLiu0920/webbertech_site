import { useEffect, useMemo, useState } from 'react';
import React from 'react';

import {
  MaterialReactTable,
  useMaterialReactTable,
  type MRT_ColumnDef,
} from 'material-react-table';

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

    useEffect(() => {
      fetch('http://localhost:5000/api/bank_accounts')
        .then((response) => response.json())
        .then((data: BankAccount[]) => {
          console.log("Bank Accounts Data:", data);  // ✅ Log response to console
          setAccounts(data);
          setLoading(false);
        })
        .catch((err) => {
          console.error("Error fetching bank accounts:", err);
          setLoading(false);
        });
    }, []);


  const columns = useMemo<MRT_ColumnDef<BankAccount>[]>(
    () => [
      { accessorKey: 'bank_name', header: 'Bank Name', size: 200 },
      { accessorKey: 'account_name', header: 'Account Name', size: 200 },
      { accessorKey: 'account_number', header: 'Account Number', size: 180 },
      { accessorKey: 'routing_number', header: 'Routing Number', size: 180 },
      { accessorKey: 'deposit_amount', header: 'Deposit Amount ($)', size: 150 },
      { accessorKey: 'current_amount', header: 'Current Amount ($)', size: 150 },
      { accessorKey: 'maturity_date', header: 'Maturity Date', size: 180 },
      { accessorKey: 'current_rate', header: 'Current Rate (%)', size: 120 },
      { accessorKey: 'comments', header: 'Comments', size: 250 },
    ],
    []
  );

  const table = useMaterialReactTable({
    columns,
    data: accounts,
    state: { isLoading: loading },
    enablePagination: true,
    enableSorting: true,
    enableColumnResizing: true,
    enableColumnVirtualization: true,
    enableRowNumbers: true,
    muiTableContainerProps: { sx: { maxHeight: '600px' } },
  });

  return <MaterialReactTable table={table} />;
};

export default BankAccounts;
