import { SessionProvider } from "next-auth/react";
import { CssBaseline } from "@mui/material";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import React, { useEffect } from "react";
import darkTheme from "@/theme/darkTheme";
import lightTheme from "@/theme/lightTheme";
import Header from "@/components/Header";
import Layout from "@/components/Layout";
import { AppProps } from "next/app";
import { Session } from "next-auth";

const ColorModeContext = React.createContext({
  toggleColorMode: () => { },
});

const App = ({ Component, pageProps }: AppProps<{ session: Session; }>) => {

  const [mode, setMode] = React.useState<"light" | "dark">("dark");
  const colorMode = React.useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => (prevMode === "light" ? "dark" : "light"));
      },
    }),
    []
  );

  const darkThemeChosen = React.useMemo(
    () =>
      createTheme({
        ...darkTheme,
      }),
    []
  );
  const lightThemeChosen = React.useMemo(
    () =>
      createTheme({
        ...lightTheme,
      }),
    []
  );
  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider
        theme={mode === "dark" ? darkThemeChosen : lightThemeChosen}
      >
        <SessionProvider session={pageProps.session}>
          <CssBaseline />
          <Header ColorModeContext={ColorModeContext} />
          <Layout>
            <Component {...pageProps} />
          </Layout>
        </SessionProvider>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
};
export default App;