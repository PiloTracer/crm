import { useEffect, useMemo, useState } from 'react';

import {
  MRT_EditActionButtons,
  MaterialReactTable,
  // createRow,
  type MRT_ColumnDef,
  type MRT_Row,
  type MRT_TableOptions,
  useMaterialReactTable,
} from 'material-react-table';
import {
  Box,
  Button,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  QueryClient,
  QueryClientProvider,
  useMutation,
  useQuery,
  useQueryClient,
} from '@tanstack/react-query';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import { mkConfig, generateCsv, download } from 'export-to-csv'; //or use your library of choice here
import axios from 'axios';
import { Transaction, CreateTransactionFnc } from '@/components/DbFunctions/Balances'
import { useSession } from 'next-auth/react';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import React from 'react';
import { useUpdateGridContext } from '@/components/Context/BalanceContext';

const csvConfig = mkConfig({
  fieldSeparator: ',',
  decimalSeparator: '.',
  useKeysAsHeaders: true,
});

type Request = {
  username: string,
  merchant: string
}

let data: Transaction[] = [];

const Example = () => {
  const { needsUpdate, setNeedsUpdate } = useUpdateGridContext();
  const { data: session } = useSession();
  const merchant: string = session?.user?.xmerchant;
  const [validationErrors, setValidationErrors] = useState<
    Record<string, string | undefined>
  >({});

  const id = useMemo(() => {
    const res: string = session?.user ? session.user.xid : "";
    return res;
  }, [session?.user]);

  const role = useMemo(() => {
    const res: string = session?.user ? session?.user?.xrole : undefined;
    return res;
  }, [session?.user]);

  const token = useMemo(() => {
    const res: string = session?.user ? session.user.xtoken : "";
    return res;
  }, [session?.user]);

  const req: Request = useMemo(() => {
    return {
      username: session?.user.xid,
      merchant: session?.user.xmerchant
    };
  }, [session?.user]);

  const { refetch } = useGetTransactions(req); // Make sure this is the correct hook from your implementation
  useEffect(() => {
    if (needsUpdate) {
      refetch(); // This refetches the data for BalanceGrid
      setNeedsUpdate(false); // Reset the update flag
    }
  }, [needsUpdate, refetch, setNeedsUpdate]);


  const handleExportRows = (rows: MRT_Row<Transaction>[]) => {
    const rowData = rows.map((row) => row.original);
    const csv = generateCsv(csvConfig)(rowData);
    download(csvConfig)(csv);
  };

  const handleExportData = async () => {
    var d = await fetchDataFromApi(req);
    const csv = generateCsv(csvConfig)(d);
    download(csvConfig)(csv);
  };

  const columns = useMemo<MRT_ColumnDef<Transaction>[]>(
    () => [
      {
        accessorKey: "key",
        header: "Merchant",
        enableEditing: false,
        Edit: () => null
      },
      {
        accessorKey: "value.amntsign",
        header: "Amount",
        enableEditing: false,
        Edit: () => null
      },
      {
        accessorKey: "value.feesign",
        header: "Fees",
        enableEditing: false,
        Edit: () => null
      },
      {
        accessorKey: "value.totsign",
        header: "Total",
        enableEditing: false,
        Edit: () => null
      }
    ]
    ,
    [validationErrors, role],
  );

  //call READ hook
  const {
    data: fetchedTransactions = [],
    isError: isLoadingTransactionsError,
    isFetching: isFetchingTransactions,
    isLoading: isLoadingTransactions,
  } = useGetTransactions(req);
  //call UPDATE hook
  const { mutateAsync: updateTransaction, isPending: isUpdatingTransaction } =
    useUpdateTransaction(id, merchant);
  //call DELETE hook
  const { mutateAsync: deleteTransaction, isPending: isDeletingTransaction } =
    useDeleteTransaction();
  //call CREATE hook
  const { mutateAsync: createTransaction, isPending: isCreatingTransaction } =
    useCreateTransaction(merchant, id);

  //CREATE action
  const handleCreateTransaction: MRT_TableOptions<Transaction>['onCreatingRowSave'] = async ({
    values,
    table,
  }) => {
    //console.log("handleCreateTransaction");
    const newValidationErrors = validateTransaction(values);
    if (Object.values(newValidationErrors).some((error) => error)) {
      setValidationErrors(newValidationErrors);
      return;
    }
    setValidationErrors({});
    await createTransaction(values);
    table.setCreatingRow(null); //exit creating mode
  };

  //UPDATE action
  const handleSaveTransaction: MRT_TableOptions<Transaction>['onEditingRowSave'] = async ({
    values,
    table,
  }) => {
    //console.log("handleSaveTransaction");
    const newValidationErrors = validateTransaction(values);
    if (Object.values(newValidationErrors).some((error) => error)) {
      setValidationErrors(newValidationErrors);
      return;
    }
    setValidationErrors({});
    await updateTransaction(values);
    table.setEditingRow(null); //exit editing mode
  };

  //DELETE action
  const openDeleteConfirmModal = (row: MRT_Row<Transaction>) => {
    if (window.confirm('Are you sure you want to delete this transaction?')) {
      deleteTransaction(0);
    }
  };

  const table = useMaterialReactTable({
    columns,
    enableColumnFilterModes: false,
    enableColumnPinning: false,
    enableColumnActions: false,
    initialState: {
      density: 'compact', columnVisibility: { channel: false },
      columnPinning: {
        left: ['mrt-row-expand', 'mrt-row-select'],
        right: ['mrt-row-actions'],
      },
    },
    paginationDisplayMode: 'pages',
    data: fetchedTransactions,
    positionToolbarAlertBanner: 'bottom',
    enableRowSelection: false,
    defaultColumn: { minSize: 20, maxSize: 50 },
    layoutMode: 'semantic',
    createDisplayMode: 'modal', //default ('row', and 'custom' are also available)
    editDisplayMode: 'modal', //default ('row', 'cell', 'table', and 'custom' are also available)
    enableEditing: false,
    //getRowId: (row) => row._id,   // there is no need forn an _id and _id is not available
    muiSearchTextFieldProps: {
      size: 'small',
      variant: 'outlined',
    },
    muiPaginationProps: {
      color: 'secondary',
      rowsPerPageOptions: [10, 20, 30],
      shape: 'rounded',
      variant: 'outlined',
    },
    muiToolbarAlertBannerProps: isLoadingTransactionsError
      ? {
        color: 'error',
        children: 'Error loading data',
      }
      : undefined,
    muiTableContainerProps: {
      sx: {
        minHeight: '150px',
      },
    },
    muiTableHeadCellProps: {
      //simple styling with the `sx` prop, works just like a style prop in this example
      sx: {
        fontWeight: 'normal',
        fontSize: '12px',
      },
    },
    muiTableBodyRowProps: ({ row }) => ({
      //conditionally style selected rows
      sx: {
        fontWeight: row.getIsSelected() ? 'bold' : 'normal',
      },
    }),
    muiTableBodyCellProps: ({ column }) => ({
      //conditionally style pinned columns
      sx: {
        fontWeight: column.getIsPinned() ? 'bold' : 'normal',
        fontSize: '12px'
      },
    }),
    onCreatingRowCancel: () => setValidationErrors({}),
    onCreatingRowSave: handleCreateTransaction,
    onEditingRowCancel: () => setValidationErrors({}),
    onEditingRowSave: handleSaveTransaction,



    //optionally customize modal content
    renderCreateRowDialogContent: ({ table, row, internalEditComponents }) => (
      <>
        <DialogTitle variant="h3">Create New Transaction</DialogTitle>
        <DialogContent
          sx={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}
        >
          {internalEditComponents} {/* or render custom edit components here */}
        </DialogContent>
        <DialogActions>
          <MRT_EditActionButtons variant="text" table={table} row={row} />
        </DialogActions>
      </>
    ),
    //optionally customize modal content
    renderEditRowDialogContent: ({ table, row, internalEditComponents }) => (
      <>
        <DialogTitle variant="h3">Edit Transaction</DialogTitle>
        <DialogContent
          sx={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}
        >
          {internalEditComponents} {/* or render custom edit components here */}
        </DialogContent>
        <DialogActions>
          <MRT_EditActionButtons variant="text" table={table} row={row} />
        </DialogActions>
      </>
    ),
    renderRowActions: ({ row, table }) => (
      <Box sx={{ display: 'flex', gap: '1rem' }}>
        <Tooltip title="Edit">
          <IconButton onClick={() => table.setEditingRow(row)}>
            <EditIcon />
          </IconButton>
        </Tooltip>
        <Tooltip title="Delete">
          <IconButton color="error" onClick={() => openDeleteConfirmModal(row)}>
            <DeleteIcon />
          </IconButton>
        </Tooltip>
      </Box>
    ),
    renderTopToolbarCustomActions: ({ table }) => (
      false && <Box
        sx={{
          display: 'flex',
          gap: '16px',
          padding: '8px',
          flexWrap: 'wrap',
        }}
      >
        {["admin", "owner"].includes(role) && <Button
          variant="contained"
          onClick={() => {
            table.setCreatingRow(true); //simplest way to open the create row modal with no default values
          }}
        >
          Create New Transaction
        </Button>}
        <Button
          //export all data that is currently in the table (ignore pagination, sorting, filtering, etc.)
          onClick={handleExportData}
          startIcon={<FileDownloadIcon />}
        >
          Export All Data
        </Button>
        <Button
          disabled={table.getPrePaginationRowModel().rows.length === 0}
          //export all rows, including from the next page, (still respects filtering and sorting)
          onClick={() =>
            handleExportRows(table.getPrePaginationRowModel().rows)
          }
          startIcon={<FileDownloadIcon />}
        >
          Export All Rows
        </Button>
        <Button
          disabled={table.getRowModel().rows.length === 0}
          //export all rows as seen on the screen (respects pagination, sorting, filtering, etc.)
          onClick={() => handleExportRows(table.getRowModel().rows)}
          startIcon={<FileDownloadIcon />}
        >
          Export Page Rows
        </Button>
        <Button
          disabled={
            !table.getIsSomeRowsSelected() && !table.getIsAllRowsSelected()
          }
          //only export selected rows
          onClick={() => handleExportRows(table.getSelectedRowModel().rows)}
          startIcon={<FileDownloadIcon />}
        >
          Export Selected Rows
        </Button>
      </Box>
    ),
    state: {
      isLoading: isLoadingTransactions,
      isSaving: isCreatingTransaction || isUpdatingTransaction || isDeletingTransaction,
      showAlertBanner: isLoadingTransactionsError,
      showProgressBars: isFetchingTransactions,
    },
  });

  return <MaterialReactTable table={table} />;
};

//CREATE hook (post new transaction to api)
function useCreateTransaction(merchant: string, id: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (transaction: Transaction) => {
      const request: any = {
        status: {
          status: "p",
          detail: "Manual Balance adjustment"
        }
      }
      console.log("about to call CreateTransactionFnc");
      let res = await CreateTransactionFnc(request);
      console.log(res);
      return res;

      //await new Promise((resolve) => setTimeout(resolve, 1000)); //fake api call
      //return Promise.resolve();
    },
    //client side optimistic update
    onMutate: (newTransactionInfo: Transaction) => {
      // Store the previous transactions in case we need to roll back
      const previousTransactions = queryClient.getQueryData<Transaction[]>(['transactions']);

      // Optimistically update the transactions
      queryClient.setQueryData(
        ['transactions'],
        (prevTransactions: Transaction[]) =>
          [
            ...prevTransactions,
            {
              ...newTransactionInfo,
              id: (Math.random() + 1).toString(36).substring(7),
            },
          ] as Transaction[],
      );

      // Return the rollback function
      return { rollback: () => queryClient.setQueryData(['transactions'], previousTransactions) };
    },
    onError: (error, variables, context) => context?.rollback(),
    onSuccess: (data, variables, context) => {
      queryClient.setQueryData(['transactions'], (old: Transaction[]) => {
        return old.map((transaction) => {
          if (transaction.value.amntsign === variables.value.amntsign) { //this used to be _id instead of amntsign
            return data;
          } else {
            return transaction;
          }
        });
      });
    },
    // onSettled: () => queryClient.invalidateQueries({ queryKey: ['transactions'] }), //refetch transactions after mutation, disabled for demo
  });
}

const fetchDataFromApi = async (req: Request) => {
  const API_URL = '/api/fetch/fetchBalanceBalances';
  const customConfig = {
    headers: {
      'Content-Type': 'application/json'
    }
  };
  try {
    const response = await axios.post(
      API_URL,
      req,
      customConfig
    );
    var result = await response.data;
    return result;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
  return [];
};

//READ hook (get transactions from api)
function useGetTransactions(req: Request) { //instead of any used to be Request
  return useQuery<Transaction[]>({
    queryKey: ['transactions'],
    queryFn: async () => {
      var dat = await fetchDataFromApi(req);
      return dat;
    },
    refetchOnWindowFocus: false,
  });
}

//UPDATE hook (put transaction in api) NO UPDATES FOR BALANCE TRANSACTIONS/ADJUSTMENTS
function useUpdateTransaction(id: string, merchant: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (transaction: Transaction) => {
      return null;
    },
    //client side optimistic update
    onMutate: (newTransactionInfo: Transaction) => {
      //console.log("did this stupid thing");
      queryClient.setQueryData(
        ['transactions'],
        (prevTransactions: any) =>
          prevTransactions?.map((prevTransaction: Transaction) =>
            prevTransaction.value.amntsign === newTransactionInfo.value.amntsign ? newTransactionInfo : prevTransaction, // _id instead of amntsign
          ),
      );
    },
    onSettled: () => queryClient.invalidateQueries({ queryKey: ['transactions'] }),
  });
}

//DELETE hook (delete transaction in api)
function useDeleteTransaction(amountsign: number = 0) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (amountsign: number) => { //amountsign instead of transactionId
      //send api update request here
      await new Promise((resolve) => setTimeout(resolve, 1000)); //fake api call
      return Promise.resolve();
    },
    //client side optimistic update
    onMutate: (amountsign: number) => { //amountsign instead of transactionId
      queryClient.setQueryData(['transactions'], (prevTransactions: any) =>
        prevTransactions?.filter((transaction: Transaction) => transaction.value.amntsign !== amountsign), //_id instead of amntsign,  //amountsign instead of transactionId
      );
    },
    onSettled: () => queryClient.invalidateQueries({ queryKey: ['transactions'] }),
  });
}

const queryClient = new QueryClient();

const BalanceGrid = () => (
  //Put this with your other react-query providers near root of your app
  <LocalizationProvider dateAdapter={AdapterDayjs}>
    <QueryClientProvider client={queryClient}>
      <Example />
    </QueryClientProvider>
  </LocalizationProvider>
);

export default BalanceGrid;

const validateRequired = (value: string) => !!value.length;
const validateEmail = (email: string) =>
  !!email.length &&
  email
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
    );

function validateTransaction(transaction: Transaction) {
  return {}; //no validations
}