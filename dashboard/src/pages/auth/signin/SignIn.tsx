import { NextPage } from "next";
import { signIn, useSession } from "next-auth/react";
import { useRouter } from "next/router";
import React, { useEffect } from "react";
import { FormEventHandler, useState } from "react";


import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, makeStyles, ThemeProvider } from '@mui/material/styles';
import scss from './Signin.module.scss';

function Copyright(props: any) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <Link color="inherit" href="https://mui.com/">
        W-Financial
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const defaultTheme = createTheme();

interface Props { }

const SignIn: React.FC = () => {
  //const SignIn: NextPage = (props): JSX.Element => {
  const { status } = useSession();
  useEffect(() => {
  }, [status]);


  const [userInfo, setUserInfo] = useState({ username: "", password: "" });
  const router = useRouter();
  const handleSubmit: FormEventHandler<HTMLFormElement> = async (e) => {
    // validate your userinfo
    e.preventDefault();

    const res = await signIn("credentials", {
      username: userInfo.username,
      password: userInfo.password,
      redirect: false,
    });

    console.log(res);

    //router.push(`/auth/signin/callbackUrl=${router.query.callbackUrl ?? "/dashboard"}`);
    router.push(router.query.callbackUrl ? decodeURIComponent(router.query.callbackUrl as string) : '/');
  };

  if (status === "authenticated") {
    return (<div>loading</div>)
  }
  else {
    return (
      <>
        <main className={scss.main}>
          <CssBaseline />
          <Box
            sx={{
              marginTop: 8,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Sign in
            </Typography>
            <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
              <TextField
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                autoFocus
                value={userInfo.username}
                onChange={({ target }) =>
                  setUserInfo({ ...userInfo, username: target.value })
                }
                type="email"
                placeholder="john@email.com"
                InputLabelProps={{
                  shrink: true,
                }}
                variant="filled"
              />
              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                id="password"
                autoComplete="current-password"
                value={userInfo.password}
                onChange={({ target }) =>
                  setUserInfo({ ...userInfo, password: target.value })
                }
                type="password"
                placeholder="********"
                InputLabelProps={{
                  shrink: true,
                }}
                variant="filled"
              />
              <FormControlLabel
                control={<Checkbox value="remember" color="primary" />}
                label="Remember me"
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Sign In
              </Button>
              <Grid container>
                <Grid item xs>
                  <Link href="#" variant="body2">
                    Forgot password?
                  </Link>
                </Grid>
                <Grid item>
                  <Link href="#" variant="body2">
                    {"Don't have an account? Sign Up"}
                  </Link>
                </Grid>
              </Grid>
            </Box>
          </Box>
          <Copyright sx={{ mt: 8, mb: 4 }} />
        </main>
      </>
    );
  }

};

export default SignIn;