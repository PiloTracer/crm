import { useEffect, useMemo, useState } from 'react';

import {
  MRT_EditActionButtons,
  MaterialReactTable,
  // createRow,
  type MRT_ColumnDef,
  type MRT_Row,
  useMaterialReactTable,
} from 'material-react-table';
import {
  Box,
  Button,
  DialogActions,
  DialogContent,
  DialogTitle,
} from '@mui/material';
import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from '@tanstack/react-query';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import { mkConfig, generateCsv, download } from 'export-to-csv'; //or use your library of choice here
import axios from 'axios';
import { Transaction } from '@/components/DbFunctions/Balances'
import { useSession } from 'next-auth/react';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import React from 'react';
import { config } from '../../../../config/config';

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

const UploadResultsTable = () => {
  const { data: session } = useSession();
  const [validationErrors, setValidationErrors] = useState<
    Record<string, string | undefined>
  >({});

  const id = useMemo(() => {
    const res: string = session?.user ? session.user.xid : "";
    return res;
  }, [session?.user]);

  const merchant = useMemo(() => {
    const res: string = session?.user ? session.user.xmerchant : "";
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

  const { refetch } = useGetTransactions(req); // Make sure this is the correct hook from your implementation

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
      rowsPerPageOptions: [10, 50, 100],
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
      showAlertBanner: isLoadingTransactionsError,
      showProgressBars: isFetchingTransactions,
    },
  });

  // WebSocket setup
  useEffect(() => {
    const ws = new WebSocket(config.API_URL_WEBSOCKETS);

    ws.onopen = () => {
      console.log('Connected to WebSocket server');

      // Send authentication token right after connection is established
      const authToken = "somethingextrahere2024$$!!!!I6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"; // Replace with your actual token
      ws.send(JSON.stringify({ token: authToken }));
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      // Check if the message contains a specific value
      if (message.merchant === merchant) {
        refetch(); // Refetch the data if the condition is met
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('Disconnected from WebSocket server');
    };

    return () => {
      ws.close();
    };
  }, [refetch, session, merchant]); // Add merchant to the dependency array

  return <MaterialReactTable table={table} />;
};

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
    console.error('Error fetching data:', req);
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

const queryClient = new QueryClient();

const UploadResultsGrid = () => (
  //Put this with your other react-query providers near root of your app
  <LocalizationProvider dateAdapter={AdapterDayjs}>
    <QueryClientProvider client={queryClient}>
      <UploadResultsTable />
    </QueryClientProvider>
  </LocalizationProvider>
);

export default UploadResultsGrid;
