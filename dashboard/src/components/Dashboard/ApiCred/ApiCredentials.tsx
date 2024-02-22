// Import necessary dependencies
import React, { useMemo, useState } from 'react';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import Box from '@mui/material/Box';
import { useSession } from 'next-auth/react';
import axios from 'axios';

// Define the response type
type ApiResponse = {
  id: string;
  merchant: string;
  apitoken: string | null;
  apisecret: string | null;
};

const PostRequestComponent: React.FC = () => {
  const { data: session } = useSession();
  const [response, setResponse] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      // Handle successful copy (e.g., show a toast notification)
    }, (err) => {
      // Handle errors here
      console.error('Could not copy text: ', err);
    });
  };

  const role = useMemo(() => {
    const res: string = session?.user ? session?.user?.xrole : undefined;
    return res;
  }, [session?.user]);

  const merchant = useMemo(() => {
    const res: string = session?.user ? session?.user?.xmerchant : undefined;
    return res;
  }, [session?.user]);

  const id = useMemo(() => {
    const res: string = session?.user ? session.user.xid : "";
    return res;
  }, [session?.user]);

  const token = useMemo(() => {
    const res: string = session?.user ? session.user.xtoken : "";
    return res;
  }, [session?.user]);

  const sendPostRequest = async () => {

    try {
      // Replace with your API endpoint
      const url = 'http://localhost:8000/messages/user/createapi';

      const header = {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
      }

      // Replace with the data you need to send
      const data = {
        "id": id,
        "merchant": merchant
      };

      const result = await axios.post<ApiResponse>(url, data, header);
      setResponse(result.data);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'An error occurred');
    }
  };

  return (
    <Box sx={{ padding: 2 }}>
      {["admin"].includes(role) &&
        <>
          <Button variant="contained" color="primary" onClick={sendPostRequest}>
            Generate API credentials
          </Button>
          <Typography variant="h6">NOTE: This action cannot be undone.<br />Once you click, you will need to update your integration with the new credentials.</Typography>
        </>
      }
      {response && (
        <Box sx={{ marginTop: 2 }}>
          <Typography variant="h6">Write down the following data in a secure location:</Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography>
              Secret Word: <span style={{ color: 'green' }}>{response.apisecret}</span>
            </Typography>
            <IconButton size="small" onClick={() => copyToClipboard(response?.apisecret ? response.apisecret : "")}>
              <ContentCopyIcon fontSize="inherit" />
            </IconButton>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography>
              Api Token: <span style={{ color: 'green' }}>{response.apitoken}</span>
            </Typography>
            <IconButton size="small" onClick={() => copyToClipboard(response?.apitoken ? response.apitoken : "")}>
              <ContentCopyIcon fontSize="inherit" />
            </IconButton>
          </Box>
          <Typography variant="h6" color="error">(The information above will only be available at this time)</Typography>
        </Box>
      )}
      {error && (
        <Typography color="error" sx={{ marginTop: 2 }}>
          Error: {error}
        </Typography>
      )}
    </Box>
  );
};

export default PostRequestComponent;
