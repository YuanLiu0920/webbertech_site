import { useEffect, useMemo, useState } from 'react';
import React from 'react';

import {
  MaterialReactTable,
  useMaterialReactTable,
  type MRT_ColumnDef,
} from 'material-react-table';

interface Bond {
  id: number;
  bond_name: string;
  bond_type: string;
  bond_term: number;
  amount: number;
  maturity_date: string;
  apy: number;
  platform: string;
  comment: string;
}

const Bonds: React.FC = () => {
  const [bonds, setBonds] = useState<Bond[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
      fetch('http://localhost:5000/api/bonds')
        .then((response) => response.json())
        .then((data: Bond[]) => {
          console.log("Bonds Data:", data);  // ✅ Log response to console
          setBonds(data);
          setLoading(false);
        })
        .catch((err) => {
          console.error("Error fetching bonds:", err);
          setLoading(false);
        });
    }, []);


  const columns = useMemo<MRT_ColumnDef<Bond>[]>(
    () => [
      { accessorKey: 'bond_name', header: 'Bond Name', size: 200 },
      { accessorKey: 'bond_type', header: 'Bond Type', size: 150 },
      { accessorKey: 'bond_term', header: 'Bond Term (Years)', size: 120 },
      { accessorKey: 'amount', header: 'Amount ($)', size: 150 },
      { accessorKey: 'maturity_date', header: 'Maturity Date', size: 180 },
      { accessorKey: 'apy', header: 'APY (%)', size: 120 },
      { accessorKey: 'platform', header: 'Platform', size: 150 },
      { accessorKey: 'comment', header: 'Comment', size: 250 },
    ],
    []
  );

  const table = useMaterialReactTable({
    columns,
    data: bonds,
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

export default Bonds;
