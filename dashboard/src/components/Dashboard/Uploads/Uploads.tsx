import React, { useCallback, useMemo } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { useTheme } from "@mui/system";
import { Typography } from '@mui/material';
import scss from "./Uploads.module.scss";
import { Card, Grid, Paper, Box } from "@mui/material";
import { useSession } from 'next-auth/react';
import { error } from 'console';
import { config } from '../../../../config/config';

const Uploads = () => {
  type Response = {
    id: string,
    access_token: string
  }

  const theme = useTheme();
  const API_METHOD = 'POST'
  const STATUS_IDLE = 0
  const STATUS_UPLOADING = 1

  const minSize = 0;
  const maxSize = 100000;
  const accept = "";
  const [myfiles, setFiles] = React.useState([])
  const [status, setStatus] = React.useState(STATUS_IDLE)

  const { data: session } = useSession();

  const role = useMemo(() => {
    const res: string = session?.user ? session?.user?.xrole : undefined;
    return res;
  }, [session?.user]);

  const merchant = useMemo(() => {
    const res: string = session?.user ? session?.user?.xmerchant : undefined;
    return res;
  }, [session?.user]);


  const onDrop = useCallback((acceptedFiles: any) => {
    const API_URL = '/api/fetch/fetchFilesUpload'
    const fdata = new FormData();
    const conf = {
      headers: {
        'content-type': 'multipart/form-data'
      }
    }
    if (merchant == (undefined || "")) {
      throw Error("failed! Missing Merchant name");
    }
    fdata.set("merchant", merchant);
    console.log("about to submit files...");
    const uploadFiles = (req: any) => {
      setStatus(STATUS_UPLOADING);
      axios.post(
        API_URL,
        req,
        conf)
        .then((res: { data: Response; }) => console.log(res.data))
    }
    [...acceptedFiles].forEach((file, i) => {
      fdata.append("files", file, merchant + "_" + file.name);
    })
    uploadFiles(fdata);
  }, [merchant])

  const { isDragActive, getRootProps, getInputProps, isDragReject, acceptedFiles } = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': ['.jpeg', '.jpg'],
      'image/png': ['.png'],
      'text/*': ['.txt', '.csv'],
      'application/ms-excel': [".xls", ".xlsx"],
      'application/msexcel': [".xls", ".xlsx"],
      'application/json': [".json"],
    }
  });


  const files = acceptedFiles.map((file: any) => (
    <li key={file.path}>
      {file.path} - {file.size} bytes
    </li>
  ));

  // The base template for the alert
  if (merchant != "*" && ["standard", "admin"].includes(role)) {
    return (
      <>
        <Paper className={scss.transactions}>
          <Grid style={{ width: '100vw' }}>
            <Card className={scss.card} variant={"outlined"} style={{ padding: '0rem', borderStyle: 'dashed', borderWidth: '5px' }}>
              <div {...getRootProps()}>
                <input {...getInputProps()} />
                {
                  isDragActive ?
                    <>
                      <Typography color={theme.palette.success.main} fontSize={14} padding={5}>
                        Dropping files
                      </Typography>
                    </>
                    :
                    <>
                      <Typography color={theme.palette.success.main} fontSize={14} padding={5}>
                        Drag and drop some files here, or click to select files
                      </Typography>
                    </>
                }
              </div>
            </Card>
            <Box>
              <aside>
                <h4 style={{ paddingTop: "1rem" }}>Files</h4>
                <ul style={{ paddingLeft: "2rem" }}>{files}</ul>
              </aside>
            </Box>

          </Grid>
        </Paper >
      </>
    );

  }
  else {
    return (
      <>
        <Paper className={scss.transactions}>
          <Grid style={{ width: '100vw' }}>
            <Card className={scss.card} variant={"outlined"} style={{ padding: '0rem', borderStyle: 'dashed', borderWidth: '5px' }}>
              <Typography color={theme.palette.error.main} fontSize={14} padding={5}>
                Owners or Users with Global Merchant definitions cannot upload files at this time.
              </Typography>
            </Card>
          </Grid>
        </Paper >
      </>
    );

  }
  //return uploadTemplate();

}

export default Uploads;
