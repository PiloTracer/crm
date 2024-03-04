import React, { useState, useEffect, useMemo } from 'react';
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
  UseMutationResult,
  useQuery,
  useQueryClient,
} from '@tanstack/react-query';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import { mkConfig, generateCsv, download } from 'export-to-csv'; //or use your library of choice here
import axios from 'axios';
import { GetMerchantsActive } from '@/components/DbFunctions/GetMerchantsActive'
import { User, RequestData, ResponseData, CreateUserFnc, DeleteUserFnc, UpdateUserFnc } from '@/components/DbFunctions/UpdateUser'
import { useSession } from 'next-auth/react';
import { Session } from 'inspector';
import { getMaxListeners } from 'events';
import { idID } from '@mui/material/locale';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { useTheme } from "@mui/system";
import { log } from 'console';
import TransactionBottomRow from '../TransactionBottomRow';
import Snackbar from '@mui/material/Snackbar';
import { ToggleOff, ToggleOn } from '@mui/icons-material';

const csvConfig = mkConfig({
  fieldSeparator: ',',
  decimalSeparator: '.',
  useKeysAsHeaders: true,
});

//import { getServerSession } from "next-auth";


type Request = {
  username: string,
  merchant: string
}


interface UserProps {
  mactive: string[]; // Replace MyDataType with the correct type for your data
}


const Users: React.FC<UserProps> = ({ mactive }) => {
  const [snackbarOpen, setSnackbarOpen] = useState<boolean>(false);
  const [snackbarMessage, setSnackbarMessage] = useState<string>('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
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

  const id = useMemo(() => {
    // Your constant initialization logic
    const res: string = session?.user ? session.user.xid : "";
    return res;
  }, [session?.user]);

  const merchant = useMemo(() => {
    // Your constant initialization logic
    const res: string = session?.user ? session.user.xmerchant : "";
    return res;
  }, [session?.user]);

  const role = useMemo(() => {
    // Your constant initialization logic
    const res: string = session?.user ? session?.user?.xrole : undefined;
    return res;
  }, [session?.user]);

  const roleopt: string[] = useMemo(() => {
    const res: string[] = role == "owner" ? ["standard", "admin", "owner"] : ["standard", "admin"];
    return res;
  }, [session?.user]);

  const token = useMemo(() => {
    const res: string = session?.user ? session.user.xtoken : "";
    return res;
  }, [session?.user]);

  const req: Request = useMemo(() => {
    // Your constant initialization logic
    return {
      username: id,
      merchant: merchant
    };
  }, [session?.user]);


  const handleExportRows = (rows: MRT_Row<User>[]) => {
    const rowData = rows.map((row) => row.original);
    const csv = generateCsv(csvConfig)(rowData);
    download(csvConfig)(csv);
  };

  const handleExportData = async () => {
    var d = await fetchDataFromApi(req);
    const csv = generateCsv(csvConfig)(d);
    download(csvConfig)(csv);
  };

  const columns = useMemo<MRT_ColumnDef<User>[]>(
    () => [
      {
        accessorKey: "username",
        header: "User",
        enableEditing: true
      },
      {
        accessorKey: "password",
        header: "Password"
      },
      {
        accessorKey: "_id",
        header: "Id",
        enableEditing: false,
        Edit: () => null
      },
      {
        accessorKey: "active",
        header: "Active",
        Cell: ({ cell }) => cell.getValue() ? 'true' : 'false',
        enableEditing: ["admin", "owner"].includes(role),
        editVariant: 'select',
        editSelectOptions: [
          { value: true, label: 'true' },
          { value: false, label: 'false' }
        ]
      },
      {
        accessorKey: "role",
        header: "Role",
        enableEditing: ["admin", "owner"].includes(role),
        editVariant: 'select',
        editSelectOptions: roleopt
      },
      {
        accessorKey: "fullname",
        header: "Name",
        enableEditing: true
      },
      {
        accessorKey: "merchant",
        header: "Merchant",
        editVariant: 'select',
        enableEditing: ["admin", "owner"].includes(role),
        /* TODO: these options must be dynamic */
        editSelectOptions: role == "owner" ? mactive : [merchant]
      },
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
    useUpdateUser(id, merchant, role, token, { handleOpenSnackbar });
  //call DELETE hook
  const { mutateAsync: deleteTransaction, isPending: isDeletingTransaction } =
    useDeleteTransaction(id, merchant, { handleOpenSnackbar });
  //call CREATE hook
  const { mutateAsync: createTransaction, isPending: isCreatingTransaction } =
    useCreateTransaction(merchant, id, { handleOpenSnackbar });

  //CREATE action
  const handleCreateTransaction: MRT_TableOptions<User>['onCreatingRowSave'] = async ({
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
    await createTransaction(values);
    table.setCreatingRow(null); //exit creating mode
  };

  //UPDATE action
  const handleSaveTransaction: MRT_TableOptions<User>['onEditingRowSave'] = async ({
    values,
    table,
  }) => {
    const newValidationErrors = validateTransaction(values);
    const errorMessages = Object.values(newValidationErrors).filter(Boolean).join('\n');
    if (errorMessages) {
      handleOpenSnackbar(errorMessages);
      setValidationErrors(newValidationErrors);
      return;
    }
    setValidationErrors({});
    await updateTransaction(values);
    table.setEditingRow(null); //exit editing mode
  };

  //DELETE action
  const openDeleteConfirmModal = (row: MRT_Row<User>) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      deleteTransaction(row.original._id);
    }
  };
  //DELETE action
  const openUpdateConfirmModal = (row: MRT_Row<User>) => {
    if (window.confirm('Are you sure you want to modify this user?')) {
      //deleteTransaction(row.original._id);
      updateTransaction(row.original);
    }
  };

  const table = useMaterialReactTable({
    columns,
    enableColumnFilterModes: true,
    enableColumnPinning: true,
    enableColumnActions: ["admin", "owner"].includes(role),
    initialState: {
      density: 'compact', columnVisibility: { active: false, _id: false, channel: false, password: false },
      columnPinning: {
        left: ['mrt-row-expand', 'mrt-row-select'],
        right: ['mrt-row-actions'],
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
    getRowId: (row) => row._id,
    muiSearchTextFieldProps: {
      size: 'small',
      variant: 'outlined',
    },
    muiPaginationProps: {
      color: 'secondary',
      rowsPerPageOptions: [5, 10, 20],
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
        <DialogTitle variant="h3">Create New User</DialogTitle>
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
        <DialogTitle variant="h3">Edit User</DialogTitle>
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
        {id != row.id && (
          <IconButton color="error" onClick={() => openDeleteConfirmModal(row)}>
            <DeleteIcon />
          </IconButton>
        )}
        {id != row.id && row.original.active == true && (
          <IconButton color="success" onClick={() => openUpdateConfirmModal(row)}>
            <ToggleOn />
          </IconButton>
        )}
        {id != row.id && row.original.active == false && (
          <IconButton color="error" onClick={() => openUpdateConfirmModal(row)}>
            <ToggleOff />
          </IconButton>
        )}
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
        {["admin", "owner"].includes(role) && <Button
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
          Create New User
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

type UseUpdateUserProps = {
  handleOpenSnackbar: (message: string) => void;
};



const fetchDataFromApi = async (req: Request) => {
  const API_URL = '/api/fetch/fetchUsers';
  const customConfig = {
    headers: {
      'Content-Type': 'application/json'
    }
  };
  //if (request.merchant === undefined || request.merchant === null) {
  //  return;
  //}
  console.log("get users request", req);
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
  return useQuery<User[]>({
    queryKey: ['transactions'],
    queryFn: async () => {
      var d = await fetchDataFromApi(req);
      return d;
      //send api request here
      //await new Promise((resolve) => setTimeout(resolve, 1000)); //fake api call
      //return Promise.resolve(fakeData);
    },
    refetchOnWindowFocus: false,
  });
}

//UPDATE hook (put User in api)
function useUpdateUser(
  id: string,
  merchant: string,
  role: string,
  token: string,
  { handleOpenSnackbar }: UseUpdateUserProps
): UseMutationResult<User, unknown, User> {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (user: User) => {
      //send api update request here
      const request: RequestData = {
        username: id,
        merchant: user.merchant,
        message: user._id
      }

      console.log("User deactivate Request: ", request);
      const res = await UpdateUserFnc(request);
      console.log("Users update response: ", res);
      return res;
    },
    //client side optimistic update
    onMutate: (newUserInfo: User) => {
      // Store the previous transactions in case we need to roll back
      const previousTransactions = queryClient.getQueryData<User[]>(['transactions']);

      // Return the rollback function
      return { rollback: () => queryClient.setQueryData(['transactions'], previousTransactions) };
    },
    onError: (error, newUserInfo, context) => {
      console.log("error!!!");
      context?.rollback?.();
    },
    onSuccess: (data, variables, context) => {
      if (data === undefined || (variables?.message && variables?.message === "nok")) {
        console.error("reverting...");
        handleOpenSnackbar("Transaction failed, possible Non Sufficient Funds");
        context?.rollback?.();
      } else {
        handleOpenSnackbar("Transaction successful!");

        // Update the specific row in the cache
        queryClient.setQueryData<User[]>(['transactions'], (oldData = []) => {
          const updatedData = oldData.map(transaction => {
            // Assuming 'data' contains the updated transaction and has a unique identifier '_id'
            if (transaction._id === data._id) {
              return data; // Update the specific row with the new data
            }
            return transaction; // Return the unmodified row
          });
          return updatedData;
        });
      }
    },
    onSettled: () => queryClient.invalidateQueries({ queryKey: ['transactions'] })
  });
}


//CREATE hook (post new transaction to api)
function useCreateTransaction(
  merchant: string,
  id: string,
  { handleOpenSnackbar }: useCreateTransactionProps
): UseMutationResult<User, unknown, User> {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (transaction: User) => {
      const request: User = {
        _id: "",
        type: null,
        role: transaction.role,
        fullname: transaction.fullname,
        username: transaction.username,
        password: transaction.password,
        merchant: transaction.merchant,
        active: transaction.active,
        message: null,
        createds: 0,
        created_by: id,
        created_merchant: merchant,
        err: null
      }
      console.log("1", request);
      let res = await CreateUserFnc(request);
      console.log("2", res);
      return res;
    },
    //client side optimistic update
    onMutate: (newTransactionInfo: User) => {
      // Store the previous transactions in case we need to roll back
      const previousTransactions = queryClient.getQueryData<User[]>(['transactions']);

      // Return the rollback function
      return { rollback: () => queryClient.setQueryData(['transactions'], previousTransactions) };
    },
    onError: (error, variables, context) => {
      console.log("error!!!", error);
      context?.rollback?.();
    },
    onSuccess: (data, variables, context) => {
      if (data === undefined || (variables?.message && variables?.message === "nok")) {
        console.error("reverting...");
        handleOpenSnackbar("Transaction failed, possible Non Sufficient Funds");
        context?.rollback?.();
      } else {
        handleOpenSnackbar("Transaction successful!");
        // Directly updating the cache with the new transaction data
        queryClient.setQueryData<User[]>(['transactions'], (oldData = []) => {
          return [...oldData, data]; // Replace 'data' with the correct response format if necessary
        });
      }
    },
    onSettled: () => queryClient.invalidateQueries({ queryKey: ['transactions'] })
  });
}

//DELETE hook (delete transaction in api)
function useDeleteTransaction(
  id: string,
  merchant: string,
  { handleOpenSnackbar }: useCreateTransactionProps
) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (transactionId: string | null) => {
      //send api update request here
      if (transactionId != id) {
        const req: RequestData = {
          username: id,
          merchant: merchant,
          message: transactionId
        };
        const res = await DeleteUserFnc(req);
        return res;
      } else {
        return undefined;
      }

      //await new Promise((resolve) => setTimeout(resolve, 1000)); //fake api call
      //return Promise.resolve();
    },
    //client side optimistic update
    //onMutate: (transactionId: string) => {
    //  queryClient.setQueryData(['transactions'], (prevTransactions: any) =>
    //    prevTransactions?.filter((transaction: User) => transaction._id !== transactionId),
    //  );
    //  return { rollback: () => queryClient.setQueryData(['transactions'], previousTransactions) };
    //},
    onMutate: (transactionId: string) => {
      // Store the previous transactions in case we need to roll back
      const previousTransactions = queryClient.getQueryData<User[]>(['transactions']);

      // Return the rollback function
      return { rollback: () => queryClient.setQueryData(['transactions'], previousTransactions) };
    },
    onError: (error, variables, context) => {
      console.log("error!!!");
      context?.rollback?.();
    },
    onSuccess: (data, variables, context) => {
      console.log("data: ", data);
      console.log("variables: ", variables);
      if (data === undefined) {
        console.log("reverting...");
        handleOpenSnackbar("Transaction failed, possible Non Sufficient Funds");
        context?.rollback?.();
      }
      else {
        handleOpenSnackbar("Transaction successful!");
      }
      //queryClient.setQueryData(['transactions'], (old: Transaction[]) => {
      //  return old.map((transaction) => {
      //    if (transaction._id === variables._id) {
      //      return data;
      //    } else {
      //      return transaction;
      //    }
      //  });
      //});
    },
    onSettled: () => queryClient.invalidateQueries({ queryKey: ['transactions'] }), //refetch transactions after mutation, disabled for demo
  });
}

const queryClient = new QueryClient();

const ExampleWithProviders: React.FC<UserProps> = ({ mactive }) => (
  <LocalizationProvider dateAdapter={AdapterDayjs}>
    <QueryClientProvider client={queryClient}>
      <Users mactive={mactive} />
    </QueryClientProvider>
  </LocalizationProvider>
);

export default ExampleWithProviders;

const validateRequired = (value: string) => !!value.length;

const validateEmail = (email: string) =>
  !!email.length &&
  email
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
    );

function validateTransaction(transaction: User) {
  return {
    active: !validateRequired(String(transaction.active))
      ? 'Active status is Required'
      : '',
    merchant: !validateRequired(transaction.merchant)
      ? 'Merchant is Required'
      : '',
    role: !validateRequired(transaction.role)
      ? 'Role is Required'
      : '',
    password: validatePassword(transaction.password),
    name: !validateRequired(transaction.fullname) ? 'Name is Required' : '',
    username: !validateEmail(transaction.username) ? 'Invalid User name (email)' : '',
  };
}

function setIsLoading(arg0: boolean) {
  throw new Error('Function not implemented.');
}

function validatePassword(password: string | null): string {
  if (!password || password == undefined || password == null || password == "") {
    return 'Password is required';
  }
  if (password.length < 8) {
    return 'Password must be at least 8 characters long';
  }
  if (!/[A-Z]/.test(password)) {
    return 'Password must contain at least one uppercase letter';
  }
  if (!/[a-z]/.test(password)) {
    return 'Password must contain at least one lowercase letter';
  }
  if (!/[0-9]/.test(password)) {
    return 'Password must contain at least one number';
  }
  if (!/[^A-Za-z0-9]/.test(password)) {
    return 'Password must contain at least one special character';
  }
  return '';
}
