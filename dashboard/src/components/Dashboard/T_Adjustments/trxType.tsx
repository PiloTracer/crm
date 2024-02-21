import React from 'react';
import { MenuItem, Select, SelectChangeEvent } from '@mui/material';
import { MRT_Cell, MRT_ColumnDef } from 'material-react-table';
import { Transaction } from '@/components/DbFunctions/UpdateAdj';

interface CustomSelectProps {
  cell: MRT_Cell<Transaction>;
  column: MRT_ColumnDef<Transaction>[];
  row: Transaction;
  value: string;
  updateCell: (value: any) => void;
}

export const TrxTypeEditComponent: React.FC<CustomSelectProps> = ({
  cell,
  column,
  row,
  value,
  updateCell,
}) => {
  const handleSelectChange = (event: SelectChangeEvent<string>) => {
    updateCell(event.target.value as string);
  };

  const getOptions = () => {
    if (row.type === 'debit') {
      return ['withdrawal', 'error'];
    } else if (row.type === 'credit') {
      return ['deposit', 'error', 'other'];
    }
    return [];
  };

  return (
    <Select value={value} onChange={handleSelectChange}>
      {getOptions().map((option) => (
        <MenuItem key={option} value={option}>{option}</MenuItem>
      ))}
    </Select>
  );
};

//export default TrxTypeEditComponent;
