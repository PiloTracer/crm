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
  Theme,
  createStyles,
  makeStyles,
  styled,
} from '@mui/material';
import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from '@tanstack/react-query';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import { mkConfig, generateCsv, download } from 'export-to-csv'; //or use your library of choice here
import axios from 'axios';
import { UploadLogs } from '@/components/DbFunctions/UploadLogs'
import { useSession } from 'next-auth/react';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import React from 'react';
import { config, getWebSocketUrl } from '../../../../config/config';

const csvConfig = mkConfig({
  fieldSeparator: ',',
  decimalSeparator: '.',
  useKeysAsHeaders: true,
});

type Request = {
  username: string,
  merchant: string,
  context: string
}

const SuccessBackground = styled('div')(({ theme }) => ({
  backgroundColor: theme.palette.success.main,
  borderRadius: '8px',
  padding: '0px',
}));

const ErrorBackground = styled('div')(({ theme }) => ({
  backgroundColor: theme.palette.error.main,
  borderRadius: '8px',
  padding: '0px',
}));

const UploadResultsTable: React.FC = () => {
  const [snackbarOpen, setSnackbarOpen] = useState<boolean>(false);
  const [snackbarMessage, setSnackbarMessage] = useState<string>('');
  const { data: session } = useSession();
  const [validationErrors, setValidationErrors] = useState<
    Record<string, string | undefined>
  >({});

  const merchant = useMemo(() => {
    const res: string = session?.user ? session.user.xmerchant : "";
    return res;
  }, [session?.user]);

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
      username: id,
      merchant: merchant,
      context: "uploadresults"
    };
  }, [session?.user]);

  const { refetch } = useGetTransactions(req); // Make sure this is the correct hook from your implementation

  const handleExportRows = (rows: MRT_Row<UploadLogs>[]) => {
    const rowData = rows.map((row) => row.original);
    const csv = generateCsv(csvConfig)(rowData);
    download(csvConfig)(csv);
  };

  const handleExportData = async () => {
    var d = await fetchDataFromApi(req);
    const csv = generateCsv(csvConfig)(d);
    download(csvConfig)(csv);
  };

  const columns = useMemo<MRT_ColumnDef<UploadLogs>[]>(
    () => [
      {
        accessorFn: (originalRow) => new Date(originalRow.createds * 1000), //convert to date for sorting and filtering
        accessorKey: 'createds',
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
        accessorKey: "_id",
        header: "Id",
        enableEditing: false,
        Edit: () => null
      },
      {
        accessorKey: "message",
        header: "File",
        enableEditing: false,
        Edit: () => null
      },
      {
        accessorKey: "status",
        header: "Status",
        enableEditing: false,
        Cell: ({ cell }) => cell.getValue() ? 'Uploaded' : 'Failed',
        Edit: () => null
      },
      {
        accessorKey: "src",
        header: "Src",
        enableEditing: false,
        Edit: () => null
      },
      {
        accessorKey: "extra",
        header: "Extra",
        enableEditing: false,
        Edit: () => null,
        Cell: ({ cell }) => {
          const extra = cell.getValue() as string[];

          let backgroundColor = 'inherit';
          if (extra && Array.isArray(extra) && extra.length > 0) {
            const firstMessage = extra[0].toLowerCase();

            if (firstMessage.includes('success')) {
              return (
                <SuccessBackground>
                  <ul>
                    {extra.map((message, index) => (
                      <li key={index}>{message}</li>
                    ))}
                  </ul>
                </SuccessBackground>
              );
            } else if (firstMessage.includes('error')) {
              return (
                <ErrorBackground>
                  <ul>
                    {extra.map((message, index) => (
                      <li key={index}>{message}</li>
                    ))}
                  </ul>
                </ErrorBackground>
              );
            } else {
              return (
                <div>
                  <ul>
                    {extra.map((message, index) => (
                      <li key={index}>{message}</li>
                    ))}
                  </ul>
                </div>
              );

            }
          }

          // Return null or some default display if extra is not available
          return null;
        }
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
      density: 'compact', columnVisibility: { doc_id: false },
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

  function serializeToJson(data: any): string {
    return JSON.stringify(data, Object.keys(data).sort(), 0);
  }


  useEffect(() => {
    let ws: WebSocket | null = null;

    const connectWebSocket = (): void => {
      ws = new WebSocket(getWebSocketUrl());

      ws.onopen = async () => {
        const API_URL = '/api/fetch/fetchGetHash';
        console.log('Connected to WebSocket server');
        let msg = { salute: "hello!", token: "" };
        const customConfig = {
          headers: {
            'Content-Type': 'application/json'
          }
        };
        const response = await axios.post(
          API_URL,
          msg,
          customConfig
        );

        msg["token"] = response.data["token"];
        const strmsg = serializeToJson(msg);
        console.log(strmsg);
        ws?.send(strmsg);
      };

      ws.onmessage = (event: MessageEvent) => {
        const msg = JSON.parse(event.data);
        console.log("message received: " + msg);
        if (msg["salute"]) {
          console.log("success");
        }
        if (msg && msg.merchant && msg.merchant === merchant) {
          console.log("refetching");
          refetch(); // Refetch the data if the condition is met
        }
      };

      ws.onerror = (error: Event) => {
        console.error('WebSocket error:', error);
      };

      ws.onclose = () => {
        console.log('Disconnected from WebSocket server');
        // Optionally, attempt to reconnect
        setTimeout(connectWebSocket, 3000); // Reconnect after 3 seconds
      };
    };

    connectWebSocket();

    return () => {
      ws?.close();
      ws = null;
    };
  }, []);

  return <MaterialReactTable table={table} />;
};

const fetchDataFromApi = async (req: Request) => {
  const API_URL = '/api/fetch/fetchUploadLogs';
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
  return useQuery<UploadLogs[]>({
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
