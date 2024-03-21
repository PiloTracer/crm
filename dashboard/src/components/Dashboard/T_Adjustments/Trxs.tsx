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
  UseMutationResult,
  useMutation,
  useQuery,
  useQueryClient,
} from '@tanstack/react-query';
import SwapHorizontalCircleIcon from '@mui/icons-material/SwapHorizontalCircle';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import { mkConfig, generateCsv, download } from 'export-to-csv'; //or use your library of choice here
import axios from 'axios';
import { Transaction, ResponseData, RequestData, AdjustmentData, CreateTransactionFnc, ReverseAdjustmentFnc } from '@/components/DbFunctions/UpdateAdj'
import { useSession } from 'next-auth/react';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import Snackbar from '@mui/material/Snackbar';
import { sanitizeJSON, decodeHTMLEntities, isSafeStringRe } from '@/helper/Sanitize';
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

interface UserProps {
  mactive: string[]; // Replace MyDataType with the correct type for your data
}

let data: Transaction[] = [];

const WalletAdjustments: React.FC<UserProps> = ({ mactive }) => {
  const { setNeedsUpdate } = useUpdateGridContext();
  const [snackbarOpen, setSnackbarOpen] = useState<boolean>(false);
  const [snackbarMessage, setSnackbarMessage] = useState<string>('');
  const { data: session } = useSession();
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

  const merchant = useMemo(() => {
    const res: string = session?.user ? session.user.xmerchant : "";
    return res;
  }, [session?.user]);

  const merchopt: string[] = useMemo(() => {
    const res: string[] = session?.user && session.user.role === "owner" ? ["latcorp", "cliente", "*"] : [merchant];
    return res;
  }, [session?.user]);

  const roleopt: string[] = useMemo(() => {
    const res: string[] = session?.user && session.user.role === "owner" ? ["standard", "admin", "owner"] : ["standard", "admin"];
    return res;
  }, [session?.user]);

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
      username: id,
      merchant: merchant
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
        accessorKey: "status",
        header: "Status",
        enableEditing: false,
        Edit: () => null
      },
      {
        accessorFn: (originalRow) => new Date(originalRow.createds * 1000), //convert to date for sorting and filtering
        id: 'createds',
        header: 'Date',
        enableEditing: false,
        filterVariant: 'datetime-range',
        Cell: ({ cell }) =>
          `${cell.getValue<Date>().toLocaleDateString()} ${cell
            .getValue<Date>()
            .toLocaleTimeString()}`, // convert back to string for display
        Edit: () => null
      },
      {
        accessorKey: "merchant",

        header: "Merchant",
        editVariant: 'select',
        enableEditing: ["admin", "owner"].includes(role),
        /* TODO: these options must be dynamic */
        editSelectOptions: role == "owner" ? mactive : [merchant],
        muiEditTextFieldProps: {
          required: false,
          error: !!validationErrors?.merchant,
          helperText: validationErrors?.merchant,
          //remove any previous validation errors when transaction focuses on the input
          onFocus: () =>
            setValidationErrors({
              ...validationErrors,
              reson: undefined,
            }),
          //optionally add validation checking for onBlur or onChange
        }
      },
      {
        accessorKey: "amnt",
        header: "Amount",
        enableEditing: role == "owner",
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
        muiEditTextFieldProps: {
          required: false,
          error: !!validationErrors?.amnt,
          helperText: validationErrors?.amnt,
          //remove any previous validation errors when transaction focuses on the input
          onFocus: () =>
            setValidationErrors({
              ...validationErrors,
              reson: undefined,
            }),
          //optionally add validation checking for onBlur or onChange
        }
      },
      {
        accessorKey: "fee",
        header: "Fee",
        enableEditing: false,
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
        ),
        Edit: () => null
      },
      {
        accessorKey: "currency",
        header: "Curr",
        editVariant: 'select',
        enableEditing: true,
        editSelectOptions: [
          "usd"
        ],
        muiEditTextFieldProps: {
          required: false,
          error: !!validationErrors?.currency,
          helperText: validationErrors?.currency,
          //remove any previous validation errors when transaction focuses on the input
          onFocus: () =>
            setValidationErrors({
              ...validationErrors,
              reson: undefined,
            }),
          //optionally add validation checking for onBlur or onChange
        }
      },
      {
        accessorKey: "type",
        header: "Type",
        editVariant: 'select',
        enableEditing: true,
        editSelectOptions: [
          "debit",
          "credit"
        ],
        muiEditTextFieldProps: {
          required: false,
          error: !!validationErrors?.type,
          helperText: validationErrors?.type,
          //remove any previous validation errors when transaction focuses on the input
          onFocus: () =>
            setValidationErrors({
              ...validationErrors,
              reson: undefined,
            }),
          //optionally add validation checking for onBlur or onChange
        }

      },
      {
        accessorKey: "context",
        header: "Context",
        editVariant: 'select',
        enableEditing: true,
        editSelectOptions: [
          "withdrawal",
          "deposit",
          "reserve",
          "bonus",
          "other"
        ],
        muiEditTextFieldProps: {
          required: false,
          error: !!validationErrors?.context,
          helperText: validationErrors?.context,
          //remove any previous validation errors when transaction focuses on the input
          onFocus: () =>
            setValidationErrors({
              ...validationErrors,
              reson: undefined,
            }),
          //optionally add validation checking for onBlur or onChange
        }
      },
      {
        accessorKey: "trxtype",
        header: "Subtype",
        enableEditing: true,
        editVariant: 'select',
        editSelectOptions: [
          "payout",
          "inflow",
          "refund",
          "chargeback",
          "fee",
          "transfer_in",
          "transfer_out",
          "interest_credit",
          "interest_debit"
        ],
        muiEditTextFieldProps: {
          required: false,
          error: !!validationErrors?.trxtype,
          helperText: validationErrors?.trxtype,
          //remove any previous validation errors when transaction focuses on the input
          onFocus: () =>
            setValidationErrors({
              ...validationErrors,
              reson: undefined,
            }),
          //optionally add validation checking for onBlur or onChange
        }
      },
      {
        accessorKey: "method",
        header: "Method",
        editVariant: 'select',
        enableEditing: true,
        editSelectOptions: [
          "Bank Transfer",
          "Wire Transfer",
          "Cash",
          "Check",
          "Credit/Debit Card",
          "Online Payment",
          "Mobile Payment",
          "Cryptocurrency",
          "Money Order",
          "Prepaid Debit Card",
          "Peer-to-Peer (P2P)",
          "Remittance"
        ],
        muiEditTextFieldProps: {
          required: false,
          error: !!validationErrors?.method,
          helperText: validationErrors?.method,
          //remove any previous validation errors when transaction focuses on the input
          onFocus: () =>
            setValidationErrors({
              ...validationErrors,
              reson: undefined,
            }),
          //optionally add validation checking for onBlur or onChange
        }
      },
      {
        accessorKey: "description",
        header: "Description",
        enableEditing: true,
        muiTableBodyCellProps: {
          align: 'left',
        },
        Cell: ({ cell }) => <div>{decodeHTMLEntities(cell.getValue() as string)}</div>,
        muiEditTextFieldProps: {
          required: false,
          error: !!validationErrors?.description,
          helperText: validationErrors?.description,
          //remove any previous validation errors when transaction focuses on the input
          onFocus: () =>
            setValidationErrors({
              ...validationErrors,
              reson: undefined,
            }),
          //optionally add validation checking for onBlur or onChange
        }
      },
      {
        accessorKey: "target",
        header: "Target Acct",
        enableEditing: false,
        Edit: () => null
      },
      {
        accessorKey: "reference",
        header: "Reference",
        enableEditing: true,
        muiEditTextFieldProps: {
          required: false,
          error: !!validationErrors?.reference,
          helperText: validationErrors?.reference,
          //remove any previous validation errors when transaction focuses on the input
          onFocus: () =>
            setValidationErrors({
              ...validationErrors,
              reson: undefined,
            }),
          //optionally add validation checking for onBlur or onChange
        }
      },
      {
        accessorKey: "channel",
        header: "Channel",
        enableEditing: false,
        Edit: () => null
      }
    ]
    ,
    [validationErrors, role, merchant],
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
    useDeleteTransaction(merchant, id, { handleOpenSnackbar });
  //call CREATE hook
  const { mutateAsync: createTransaction, isPending: isCreatingTransaction } =
    useCreateTransaction(merchant, id, token, { handleOpenSnackbar });

  //CREATE action
  const handleCreateTransaction: MRT_TableOptions<Transaction>['onCreatingRowSave'] = async ({
    values,
    table,
  }) => {
    const newValidationErrors = validateTransaction(values);
    const errorMessages = Object.values(newValidationErrors).filter(Boolean).join('\n');
    if (errorMessages) {
      const messageLines = errorMessages.split('\n').map((line, index) => (
        <p key={index} style={{ margin: 0 }}>{line}</p>
      ));
      handleOpenSnackbar(messageLines);
      setValidationErrors(newValidationErrors);
      return;
    }
    setValidationErrors({});
    await createTransaction(values);
    table.setCreatingRow(null); //exit creating mode
    setNeedsUpdate(true);
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
    setNeedsUpdate(true);
  };

  //DELETE action
  const openDeleteConfirmModal = async (row: MRT_Row<Transaction>) => {
    if (window.confirm('Are you sure you want to reverse this transaction?')) {
      await deleteTransaction(row.original);
      setNeedsUpdate(true);
    }
  };

  const table = useMaterialReactTable({
    columns,
    enableColumnFilterModes: true,
    enableColumnPinning: true,
    enableColumnActions: ["owner"].includes(role),
    initialState: {
      density: 'compact', columnVisibility: { status: false, channel: false, _id: false, reference: false },
      columnPinning: {
        left: ['mrt-row-expand', 'mrt-row-select'],
        right: ['mrt-row-actions'],
      },
      sorting: [
        {
          id: 'createds',
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
    enableEditing: ["owner"].includes(role),
    getRowId: (row) => row._id,
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
    //    minHeight: '500px',
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
        fontWeight: row.getIsSelected() ? 'bold' : 'normal',
      },
    }),
    muiTableBodyCellProps: ({ cell }) => ({
      //conditionally style pinned columns
      sx: {
        fontSize: '12px',
        color: cell.row.original.type === 'credit' ? 'green' : cell.row.original.type === 'debit' ? 'red' : 'inherit',
      },
    }),
    onCreatingRowCancel: () => setValidationErrors({}),
    onCreatingRowSave: handleCreateTransaction,
    onEditingRowCancel: () => setValidationErrors({}),
    onEditingRowSave: handleSaveTransaction,



    //optionally customize modal content
    renderCreateRowDialogContent: ({ table, row, internalEditComponents }) => (
      <>
        {/*<DialogTitle variant="h3">New Transaction</DialogTitle>*/}
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
        {/* 
        <IconButton onClick={() => table.setEditingRow(row)}>
          <EditIcon />
        </IconButton>
        */}
        {!row.original.reversed && row.original.origen == "admin" &&
          <IconButton color="error" onClick={() => openDeleteConfirmModal(row)}>
            <SwapHorizontalCircleIcon />
          </IconButton>
        }
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
        {["owner"].includes(role) && <Button
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

type useCreateTransactionProps = {
  handleOpenSnackbar: (message: string) => void;
};

//CREATE hook (post new transaction to api)
function useCreateTransaction(
  merchant: string,
  id: string,
  token: string,
  { handleOpenSnackbar }: useCreateTransactionProps
): UseMutationResult<Transaction, unknown, Transaction> {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (transaction: Transaction) => {
      const request: AdjustmentData = {
        created: {
          id: id,
          merchant: merchant,
          createds: 0
        },
        status: {
          status: "failed",
          detail: "Manual Balance adjustment"
        },
        merchant: {
          merchant: transaction.merchant,
          id: null,
          customer: "...self",
          bank_name: null,
          branch: null
        },
        type: transaction.type,
        context: transaction.context,
        trxtype: transaction.trxtype,
        amnt: transaction.amnt,
        fee: 0,
        description: transaction.description,
        reference: transaction.reference,
        currency: transaction.currency,
        method: transaction.method,
        channel: "Dashboard",
        token: token,
        checksum: null,
        origen: "admin"
      }
      //const sanitizedObject = sanitizeJSON(request);

      let res: Transaction = await CreateTransactionFnc(request);
      return res;
    },
    //client side optimistic update
    onMutate: (newTransactionInfo: Transaction) => {
      // Store the previous transactions in case we need to roll back
      const previousTransactions = queryClient.getQueryData<Transaction[]>(['transactions']);

      // Optimistically update the transactions
      queryClient.setQueryData<Transaction[]>(
        ['transactions'],
        (prevTransactions: Transaction[] = []) =>
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
    onError: (error, variables, context) => {
      console.log("error!!!");
      context?.rollback?.();
    },
    onSuccess: (data: Transaction, variables, context) => {
      console.log("data: ", data);
      console.log("variables: ", variables);
      if (data === undefined || data?.message == undefined || data?.message != "ok") {
        //console.log("reverting... ", '-variables-', JSON.stringify(variables), '-data-', JSON.stringify(data));
        handleOpenSnackbar("Transaction failed, possible Non Sufficient Funds");
        context?.rollback?.();
      }
      else {
        handleOpenSnackbar("Transaction successful!");
      }
    },
    onSettled: () => queryClient.invalidateQueries({ queryKey: ['transactions'] }), //refetch transactions after mutation, disabled for demo
  });
}

const fetchDataFromApi = async (req: Request) => {
  const API_URL = '/api/fetch/fetchBalanceTrx';
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

//UPDATE hook (put transaction in api) NO UPDATES FOR BALANCE TRANSACTIONS/ADJUSTMENTS
function useUpdateTransaction(id: string, merchant: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (transaction: Transaction) => {
      return null;
    },
    //client side optimistic update
    onMutate: (newTransactionInfo: Transaction) => {
    },
    onSettled: () => queryClient.invalidateQueries({ queryKey: ['transactions'] }), //refetch transactions after mutation, disabled for demo
  });
}

//DELETE hook (delete transaction in api)
function useDeleteTransaction(
  merchant: string,
  id: string,
  { handleOpenSnackbar }: useCreateTransactionProps
): UseMutationResult<Transaction, unknown, Transaction> {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (transaction: Transaction) => {
      //send api update request here
      const req: RequestData = {
        username: id,
        merchant: merchant,
        message: transaction._id
      };
      const res = await ReverseAdjustmentFnc(req);
      return res as Transaction;
    },
    onMutate: (newTransactionInfo: Transaction) => {
      // Store the previous transactions in case we need to roll back
      const previousTransactions = queryClient.getQueryData<Transaction[]>(['transactions']);

      // Return the rollback function
      return { rollback: () => queryClient.setQueryData(['transactions'], previousTransactions) };
    },
    onError: (error, variables, context) => {
      context?.rollback?.();
    },
    onSuccess: (data, variables, context) => {
      if (data === undefined || (variables?.message && variables?.message === "nok")) {
        handleOpenSnackbar("Transaction failed, possible transaction non-reversible");
        context?.rollback?.();
      } else {
        handleOpenSnackbar("Transaction successful!");
        // Directly updating the cache with the new transaction data
        queryClient.setQueryData<Transaction[]>(['transactions'], (oldData = []) => {
          return [...oldData, data]; // Replace 'data' with the correct response format if necessary
        });
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
    },
  });
}

const queryClient = new QueryClient();

const AdjustmentGrid: React.FC<UserProps> = ({ mactive }) => (
  <LocalizationProvider dateAdapter={AdapterDayjs}>
    <QueryClientProvider client={queryClient}>
      <WalletAdjustments mactive={mactive} />
    </QueryClientProvider>
  </LocalizationProvider>
);

export default AdjustmentGrid;

const validateRequired = (value: string) => !!value.length;
const validateEmail = (email: string) =>
  !!email.length &&
  email
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
    );

function validateTransaction(transaction: Transaction) {
  var regexamount = /^\d+(\.\d+)?$/;
  return {
    merchant: !validateRequired(transaction.merchant)
      ? 'Merchant is Required'
      : '',
    reference: !validateRequired(transaction.reference)
      || !isSafeStringRe(String(transaction.reference))
      ? 'Reference is empty or contains forbidden characters'
      : '',
    description: !validateRequired(transaction.description)
      || !isSafeStringRe(String(transaction.description))
      ? 'Description is empty or contains forbidden characters'
      : '',
    trxtype: !validateRequired(transaction.trxtype)
      || (transaction.type == "debit" && !["payout", "chargeback", "fee", "transfer_out", "interest_debit"].includes(transaction.trxtype))
      || (transaction.type == "credit" && !["inflow", "refund", "fee", "transfer_in", "interest_credit"].includes(transaction.trxtype))
      ? 'Type and Subtype are not consistent'
      : '',
    context: !validateRequired(transaction.context)
      ? 'Please provide a valid type of adjustment'
      : '',
    method: !validateRequired(transaction.method)
      ? 'Method is Required'
      : '',
    type: !validateRequired(transaction.type)
      ? 'Type is Required'
      : '',
    currency: !validateRequired(transaction.currency)
      ? 'Currency is Required'
      : '',
    amnt: !validateRequired(String(transaction.amnt))
      || !regexamount.test(String(transaction.amnt))
      ? 'Amount is not valid'
      : '',
    //target: !validateEmail(transaction.target) ? 'Incorrect Format' : '',
  };
}