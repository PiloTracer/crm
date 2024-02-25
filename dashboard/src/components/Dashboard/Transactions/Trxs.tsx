import { useMemo, useState } from 'react';
import {
  MRT_EditActionButtons,
  MaterialReactTable,
  // createRow,
  type MRT_ColumnDef,
  type MRT_Row,
  type MRT_TableOptions,
  useMaterialReactTable,
  MRT_Cell,
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
//import DeleteIcon from '@mui/icons-material/Delete';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import { mkConfig, generateCsv, download } from 'export-to-csv'; //or use your library of choice here
import axios from 'axios';
import { Transaction, UpdateTransactionFnc, RequestData } from '@/components/DbFunctions/UpdateTrx'
import { useSession } from 'next-auth/react';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import Snackbar from '@mui/material/Snackbar';
import { red } from '@mui/material/colors';
import { isSafeStringRe } from '@/helper/Sanitize';

const csvConfig = mkConfig({
  fieldSeparator: ',',
  decimalSeparator: '.',
  useKeysAsHeaders: true,
});

type Request = {
  username: string,
  type: string,
  method: string,
  merchant: string
}


const Example: React.FC = () => {
  const [snackbarOpen, setSnackbarOpen] = useState<boolean>(false);
  const [snackbarMessage, setSnackbarMessage] = useState<string>('');
  const { data: session } = useSession();
  const merchant: string = session?.user?.xmerchant;
  const [validationErrors, setValidationErrors] = useState<
    Record<string, string | undefined>
  >({});


  const handleOpenSnackbar = (message: any) => {
    setSnackbarMessage(message);
    setSnackbarOpen(true);
  };
  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };

  const id = useMemo(() => {
    // Your constant initialization logic
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
      type: "row",
      method: "netcashach",
      merchant: session?.user.xmerchant
    };
  }, [session?.user]);


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
        accessorKey: "_id",
        header: "Id",
        enableEditing: false,
        Edit: () => null
      },
      {
        accessorFn: (originalRow) => new Date(originalRow?.createdf), //convert to date for sorting and filtering
        id: 'createdf',
        header: 'Created',
        enableColumnFilter: true,
        enableEditing: false,
        filterVariant: 'datetime-range',
        Cell: ({ cell }) =>
          `${cell.getValue<Date>().toLocaleDateString()} ${cell
            .getValue<Date>()
            .toLocaleTimeString()}`, // convert back to string for display,
        Edit: () => null
      },
      {
        accessorKey: "merchant",
        header: "Merchant",
        enableEditing: false,
        Edit: () => null
      },
      {
        accessorKey: "trxtype",
        header: "Subtype",
        enableEditing: false,
        enableColumnFilter: false,
        Edit: () => null
      },
      {
        accessorKey: "customeraccount",
        header: "Customer",
        enableEditing: false
      },
      {
        accessorKey: "parent",
        header: "File id",
        enableEditing: false,
        enableHiding: true,
        enableColumnFilter: false,
        visibleInShowHideMenu: false,
        Edit: () => null
      },
      {
        accessorKey: "amount",
        header: "Amount",
        enableEditing: false,
        muiTableBodyCellProps: {
          align: 'right',
        },
        enableColumnFilter: true,
        filterVariant: 'range',
        Cell: ({ cell }) => (
          <>
            {cell.getValue<number>()?.toLocaleString?.('en-US', {
              style: 'currency',
              currency: 'usd',
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </>
        ),
        /*filterFn: (row, columnId, filterValue, addMeta) => {
         // Assuming the filterValue is a string like "<2000"
         const filterNumber = parseFloat(filterValue.replace(/[^\d.-]/g, ''));
 
         const rowValue = row.original[columnId as keyof Transaction] as number;
 
         if (!filterValue || isNaN(filterNumber) || isNaN(rowValue)) {
           return true; // no filter applied
         }
 
         if (filterValue.startsWith('<')) {
           return rowValue < filterNumber;
         } else if (filterValue.startsWith('>')) {
           return rowValue > filterNumber;
         } else if (filterValue.startsWith('=')) {
           return rowValue === filterNumber;
         }
         // Add more conditions as needed
 
         return true; // default to true if no condition is met
       },
       filterValue: (row: any) => parseFloat(row.amount), */
      },
      {
        accessorKey: "fees",
        header: "Fees",
        enableEditing: false,
        enableColumnFilter: false,
        muiTableBodyCellProps: {
          align: 'right',
        },
        Cell: ({ cell }) => (
          <>
            {cell.getValue<number>()?.toLocaleString?.('en-US', {
              style: 'currency',
              currency: 'usd',
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </>
        )
      },
      {
        accessorKey: "cxname",
        header: "Name",
        enableEditing: false,
        enableColumnFilter: false,
        Edit: () => null
      },
      {
        accessorKey: "routing",
        header: "Routing",
        enableEditing: false,
        enableColumnFilter: false,
        Edit: () => null
      },
      {
        accessorKey: "bankaccount",
        header: "Bank Acct",
        enableEditing: false,
        enableColumnFilter: false,
        Edit: () => null
      },
      {
        accessorKey: "accounttype",
        header: "T",
        editVariant: 'select',
        enableEditing: false,
        enableColumnFilter: false,
        editSelectOptions: [
          "c",
          "s",
          "m",
          "d"
        ],
        Edit: () => null
      },
      {
        accessorKey: "email",
        header: "Email",
        enableEditing: false,
        enableColumnFilter: false,
        Edit: () => null
      },
      {
        accessorKey: "address",
        header: "Address",
        enableColumnFilter: false,
        Edit: () => null
      },
      {
        accessorKey: "method",
        header: "Method",
        enableEditing: false
      },
      {
        accessorKey: "status",
        header: "Status",
        editVariant: "select",
        editSelectOptions: ({ row }) => {
          // Determine the options based on the current row
          if (row.original.status === 'approved') {
            return [
              { label: 'approved', value: 'approved' },
              { label: 'reversed', value: 'reversed' },
            ];
          } else if (row.original.status === 'reversed') {
            return [
              { label: 'reversed', value: 'reversed' }
            ];
          } else if (row.original.status === 'rejected') {
            return [
              { label: 'pending', value: 'pending' }
            ];
          } else {
            return [
              { label: 'approved', value: 'approved' },
              { label: 'rejected', value: 'rejected' },
              { label: 'pending', value: 'pending' },
              { label: 'review', value: 'review' }
            ];
          }
        },
        enableEditing: ["admin", "owner"].includes(role),
        muiEditTextFieldProps: {
          select: true,
          error: !!validationErrors?.status,
          helperText: validationErrors?.status,
        }
      },
      {
        accessorKey: "reference",
        header: "Reference",
        enableEditing: ["admin", "owner"].includes(role),
        enableColumnFilter: false,
        muiEditTextFieldProps: {
          required: false,
          error: !!validationErrors?.reference,
          helperText: validationErrors?.reference,
          //remove any previous validation errors when transaction focuses on the input
          onFocus: () =>
            setValidationErrors({
              ...validationErrors,
              reference: undefined,
            }),
          //optionally add validation checking for onBlur or onChange
        },
      },
      {
        accessorKey: "descriptor",
        header: "Descriptor",
        /*size: 200,*/
        enableEditing: ["admin", "owner"].includes(role),
        enableColumnFilter: false,
        muiEditTextFieldProps: {
          required: false,
          error: !!validationErrors?.descriptor,
          helperText: validationErrors?.descriptor,
          //remove any previous validation errors when transaction focuses on the input
          onFocus: () =>
            setValidationErrors({
              ...validationErrors,
              descriptor: undefined,
            }),
          //optionally add validation checking for onBlur or onChange
        },
      },
      {
        accessorKey: "reason",
        header: "Reason",
        enableEditing: ["admin", "owner"].includes(role),
        enableColumnFilter: false,
        muiEditTextFieldProps: {
          required: false,
          error: !!validationErrors?.reason,
          helperText: validationErrors?.reason,
          //remove any previous validation errors when transaction focuses on the input
          onFocus: () =>
            setValidationErrors({
              ...validationErrors,
              reson: undefined,
            }),
          //optionally add validation checking for onBlur or onChange
        }
      }
    ]
    ,
    [validationErrors, role],
  );

  //call CREATE hook
  const { mutateAsync: createTransaction, isPending: isCreatingTransaction } =
    useCreateTransaction();
  //call READ hook
  const {
    data: fetchedTransactions = [],
    isError: isLoadingTransactionsError,
    isFetching: isFetchingTransactions,
    isLoading: isLoadingTransactions,
  } = useGetTransactions(req);
  //call UPDATE hook
  const { mutateAsync: updateTransaction, isPending: isUpdatingTransaction } =
    useUpdateTransaction(id, merchant, role, token, { handleOpenSnackbar });
  //call DELETE hook
  const { mutateAsync: deleteTransaction, isPending: isDeletingTransaction } =
    useDeleteTransaction();

  //CREATE action
  const handleCreateTransaction: MRT_TableOptions<Transaction>['onCreatingRowSave'] = async ({
    values,
    table,
  }) => {
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
    const newValidationErrors = validateTransaction(values);
    const errorMessages = Object.values(newValidationErrors).filter(Boolean).join('\n');
    if (errorMessages) {
      const messageLines = errorMessages.split('\n').map((line, index) => (
        <p key={index} style={{ margin: 0 }}>{line}</p>
      ));
      console.log(JSON.stringify(messageLines));
      handleOpenSnackbar(messageLines);
      setValidationErrors(newValidationErrors);
      return;
    }
    setValidationErrors({});
    await updateTransaction(values);
    table.setEditingRow(null); //exit creating mode
  };

  //DELETE action
  const openDeleteConfirmModal = (row: MRT_Row<Transaction>) => {
    if (window.confirm('Are you sure you want to delete this transaction?')) {
      deleteTransaction(row.original._id);
    }
  };

  const table = useMaterialReactTable({
    columns,
    enableColumnFilterModes: true,
    enableColumnPinning: true,
    enableColumnActions: true,
    initialState: {
      density: 'compact', columnVisibility: { parent: false, _id: false, type: false },
      columnPinning: {
        left: ['mrt-row-expand', 'mrt-row-select'],
        right: role == "owner" ? ['mrt-row-actions'] : [],
      },
      sorting: [
        {
          id: 'created',
          desc: true
        }
      ],
      pagination: {
        pageSize: 50, // Set your default number of rows per page here
        pageIndex: 0, // This sets the initial page index (0 for the first page)
      },
    },
    paginationDisplayMode: 'pages',
    data: fetchedTransactions,
    positionToolbarAlertBanner: 'bottom',
    enableRowSelection: true,
    defaultColumn: { minSize: 20, maxSize: 50 },
    layoutMode: 'semantic',
    createDisplayMode: 'modal', //default ('row', and 'custom' are also available)
    editDisplayMode: 'modal', //default ('row', 'cell', 'table', and 'custom' are also available)
    enableEditing: ["admin", "owner"].includes(role),
    getRowId: (row) => row?._id,
    muiSearchTextFieldProps: {
      size: 'small',
      variant: 'outlined',
    },
    muiPaginationProps: {
      color: 'secondary',
      rowsPerPageOptions: [50, 250, 500],
      shape: 'rounded',
      variant: 'outlined',
    },
    muiToolbarAlertBannerProps: isLoadingTransactionsError
      ? {
        color: 'error',
        children: 'Error loading data',
      }
      : undefined,
    //muiTableContainerProps: {
    //  sx: {
    //    minHeight: 'auto',
    //  },
    //},
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
        fontWeight: row.getIsSelected() ? 'bold' : 'normal'
      },
    }),
    muiTableBodyCellProps: ({ cell }) => ({
      //conditionally style pinned columns
      sx: {
        fontSize: '12px',
        color: cell.row.original.status === 'approved' ? 'green' : cell.row.original.status === 'reversed' ? 'red' : 'inherit',
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
        {/*<DialogTitle variant="h3">Edit Transaction</DialogTitle>*/}
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
      role == "owner" && <Box sx={{ display: 'flex', gap: '1rem' }}>
        <Tooltip title="Edit">
          <IconButton color="success" onClick={() => table.setEditingRow(row)}>
            <EditIcon />
          </IconButton>
        </Tooltip>
        {/* <Tooltip title="Delete">
          <IconButton color="error" onClick={() => openDeleteConfirmModal(row)}>
            <DeleteIcon />
          </IconButton>
        </Tooltip> */}
      </Box>
    ),
    renderTopToolbarCustomActions: ({ table }) => (
      <Box
        sx={{
          display: 'flex',
          gap: '16px',
          padding: '8px',
          flexWrap: 'wrap',
        }}
      >

        {false && <Button
          variant="contained"
          onClick={() => {
            table.setCreatingRow(true); //simplest way to open the create row modal with no default values
            //or you can pass in a row object to set default values with the `createRow` helper function
            // table.setCreatingRow(
            //   createRow(table, {
            //     //optionally pass in default values for the new row, useful for nested data or other complex scenarios
            //   }),
            // );
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

  return (
    <><div>
      {/* Other components */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        message={snackbarMessage}
      />
    </div><MaterialReactTable table={table} /></>
  );
};

//CREATE hook (post new transaction to api)
function useCreateTransaction() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (transaction: Transaction) => {
      //send api update request here
      await new Promise((resolve) => setTimeout(resolve, 1000)); //fake api call
      return Promise.resolve();
    },
    //client side optimistic update
    onMutate: (newTransactionInfo: Transaction) => {
      queryClient.setQueryData(
        ['transactions'],
        (prevTransactions: any) =>
          [
            ...prevTransactions,
            {
              ...newTransactionInfo,
              id: (Math.random() + 1).toString(36).substring(7),
            },
          ] as Transaction[],
      );
    },
    onSettled: () => queryClient.invalidateQueries({ queryKey: ['transactions'] }), //refetch transactions after mutation, disabled for demo
  });
}

const fetchDataFromApi = async (req: Request) => {
  const API_URL = '/api/fetch/fetchTransactions';
  const customConfig = {
    headers: {
      'Content-Type': 'application/json'
    }
  };
  try {
    console.log("request: ", req);
    const response = await axios.post(
      API_URL,
      req,
      customConfig
    );
    if (process.env.NODE_ENV === 'production') {
      console.log('Running in production mode');
    } else {
      console.log('Running in development mode');
    }
    var result = await response.data;
    return result;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
  return [];
};

//READ hook (get transactions from api)
function useGetTransactions(req: Request) {
  return useQuery<Transaction[]>({
    queryKey: ['transactions'],
    queryFn: async () => {
      var d = await fetchDataFromApi(req);
      return d;
    },
    refetchOnWindowFocus: false,
  });
}

type UseUpdateTransactionProps = {
  handleOpenSnackbar: (message: string) => void;
};

//UPDATE hook (put transaction in api)
function useUpdateTransaction(
  id: string,
  merchant: string,
  role: string,
  token: string,
  { handleOpenSnackbar }: UseUpdateTransactionProps
) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (transaction
      : Transaction) => {
      //send api update request here
      let res: Transaction;
      try {
        const request: RequestData = {
          username: id,
          merchant: ["owner"].includes(role) ? transaction.merchant : merchant,
          by_merchant: merchant,
          id: transaction?._id,
          status: transaction?.status,
          descriptor: transaction?.descriptor,
          reference: transaction?.reference,
          reason: transaction?.reason,
          transaction: {
            type: transaction?.status == "approved" ? "debit" :
              transaction?.status == "reversed" ? "credit" : "debit",
            context: "withdrawal",
            trxtype: transaction?.status == "approved" ? "payout" :
              transaction?.status == "reversed" ? "refund" : "payout",
            amnt: transaction?.amount,
            fees: transaction?.fees,
            description: "customer requested withdraw",
            target: transaction?.customeraccount,
            currency: "usd",
            method: transaction?.method,
            channel: transaction?.parent,
            token: token,
            checksum: null
          }
        }
        res = await UpdateTransactionFnc(request);
        //if (res && res.message && res.message === "nok") {
        //  throw Error("failed! " + JSON.stringify(data));
        //}
        console.log("transactions update response: ", res);
        return res;

      } catch (error) {
        console.log(error);
        //alert("Failed!");
        //throw new Error("failed! ");
      }

    },
    //client side optimistic update
    onMutate: (newTransactionInfo: Transaction) => {
      // Store the previous transactions in case we need to roll back
      const previousTransactions = queryClient.getQueryData<Transaction[]>(['transactions']);

      queryClient.setQueryData<Transaction[]>(
        ['transactions'],
        (prevTransactions: Transaction[] = []) => {
          return prevTransactions.map((transaction: Transaction) =>
            transaction._id === newTransactionInfo._id ?
              { ...transaction, ...newTransactionInfo } : transaction
          );
        });

      // Return the rollback function
      return { rollback: () => queryClient.setQueryData(['transactions'], previousTransactions) };
    },
    onError: (error, newTransactionInfo, context) => {
      console.log("error!!!");
      context?.rollback?.();
    },
    onSuccess: (data, newTransactionInfo, context) => {
      if (!data?.message || data?.message != "ok") {
        console.log("reverting...");
        handleOpenSnackbar("Transaction failed, possible Non Sufficient Funds");
        context?.rollback?.();
      }
      else {
        handleOpenSnackbar("Transaction Completed");
      }
    },

    onSettled: () => queryClient.invalidateQueries({ queryKey: ['transactions'] }), //refetch transactions after mutation, disabled for demo
  });
}

//DELETE hook (delete transaction in api)
function useDeleteTransaction() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (transactionId: string) => {
      //send api update request here
      await new Promise((resolve) => setTimeout(resolve, 1000)); //fake api call
      return Promise.resolve();
    },
    //client side optimistic update
    onMutate: (transactionId: string) => {
      queryClient.setQueryData(['transactions'], (prevTransactions: any) =>
        prevTransactions?.filter((transaction: Transaction) => transaction._id !== transactionId),
      );
    },
    onSettled: () => queryClient.invalidateQueries({ queryKey: ['transactions'] }), //refetch transactions after mutation, disabled for demo
  });
}

const queryClient = new QueryClient();

const ExampleWithProviders = () => (
  //Put this with your other react-query providers near root of your app
  <LocalizationProvider dateAdapter={AdapterDayjs}>
    <QueryClientProvider client={queryClient}>
      <Example />
    </QueryClientProvider>
  </LocalizationProvider>
);

export default ExampleWithProviders;

const validateRequired = (value: string) => !!value.length;

function validateTransaction(transaction: Transaction) {
  return {
    descriptor: transaction.status === "approved"
      && (!validateRequired(transaction.descriptor)
        || !isSafeStringRe(String(transaction.descriptor)))
      ? 'Descriptor is empty or contains forbidden characters'
      : '',
    reference: transaction.status === "approved"
      && (!validateRequired(transaction.reference)
        || !isSafeStringRe(String(transaction.reference)))
      ? 'Reference is empty or contains forbidden characters'
      : '',
    reason: !validateRequired(transaction.reason)
      || !isSafeStringRe(String(transaction.reason))
      ? 'Reason is empty or contains forbidden characters'
      : '',
  };
}