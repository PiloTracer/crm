import { CSSObject } from "@mui/system";
import * as React from "react";
import IconButton from "@mui/material/IconButton";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import ExitToAppIcon from "@mui/icons-material/ExitToApp";
import HomeIcon from "@mui/icons-material/Home";
import PaymentIcon from '@mui/icons-material/Payment';
import UploadIcon from "@mui/icons-material/Upload";
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import { Settings } from "@mui/icons-material";
import NextLink from "next/link";
import scss from "./SideMenu.module.scss";

import {
    Divider,
    Drawer,
    List,
    ListItem,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Theme,
    styled,
    useMediaQuery,
    useTheme,
} from "@mui/material";
import { signOut } from "next-auth/react";

const drawerWidth = 240;

const openedMixin = (theme: Theme): CSSObject => ({
    width: drawerWidth,
    transition: theme.transitions.create("width", {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
    }),
    overflowX: "hidden",
});

const closedMixin = (theme: Theme): CSSObject => ({
    transition: theme.transitions.create("width", {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
    overflowX: "hidden",
    width: `calc(${theme.spacing(7)} + 1px)`,
    [theme.breakpoints.up("sm")]: {
        width: `calc(${theme.spacing(8)} + 1px)`,
    },
});

const menuRouteList = ["/", "/dashboard/settings", "/dashboard/upload", "/dashboard/trxs", "/dashboard/t_adj", ""];
const menuListTranslations = ["Home", "Settings", "Upload", "Transactions", "Adjustments", "Sign Out"];
const menuListIcons = [
    <HomeIcon key="home" />,
    <Settings key="settings" />,
    <UploadIcon key="upload" />,
    <PaymentIcon key="trxs" />,
    <AccountBalanceIcon key="t_adj" />,
    <ExitToAppIcon key="signout" />,
];

const SideMenu = () => {
    const theme = useTheme();
    const [open, setOpen] = React.useState(false);
    const mobileCheck = useMediaQuery("(min-width: 600px)");

    const handleDrawerToggle = () => {
        setOpen(!open);
    };

    const handleListItemButtonClick = (text: string) => {
        text === "Sign Out" ? signOut() : null;
        setOpen(false);
    };

    const Cajon = styled(Drawer, { shouldForwardProp: (prop) => prop !== 'open' })(
        ({ theme, open }) => ({
            width: drawerWidth,
            [`& .MuiDrawer-paper`]: {
                left: 0,
                top: mobileCheck ? 64 : 57,
                flexShrink: 0,
                whiteSpace: "nowrap",
                boxSizing: "border-box",
                ...(open && {
                    ...openedMixin(theme),
                    "& .MuiDrawer-paper": openedMixin(theme),
                }),
                ...(!open && {
                    ...closedMixin(theme),
                    "& .MuiDrawer-paper": closedMixin(theme),
                }),
            },
        }),
    );

    return (
        <Cajon
            variant="permanent"
            anchor="left"
            open={open}
            className={scss.sideMenu}
        >
            <div className={scss.drawerHeader}>
                <IconButton onClick={handleDrawerToggle}>
                    {theme.direction === "rtl" ? (
                        <ChevronRightIcon />
                    ) : (
                        <ChevronLeftIcon />
                    )}
                </IconButton>
            </div>
            <Divider />
            <Divider />
            <List>
                {menuListTranslations.map((text, index) => (
                    <ListItem key={text} disablePadding sx={{ display: "block" }}>
                        <NextLink
                            className={scss.link}
                            href={`${menuRouteList[index]}`}
                        >
                            <ListItemButton
                                onClick={() => handleListItemButtonClick(text)}
                                title={text}
                                aria-label={text}
                                sx={{
                                    minHeight: 48,
                                    justifyContent: open ? "initial" : "center",
                                    px: 2.5,
                                }}
                            >
                                <ListItemIcon
                                    sx={{
                                        minWidth: 0,
                                        mr: open ? 3 : "auto",
                                        justifyContent: "center",
                                    }}
                                >
                                    {menuListIcons[index]}
                                </ListItemIcon>
                                <ListItemText
                                    primary={text}
                                    sx={{
                                        color: theme.palette.text.primary,
                                        opacity: open ? 1 : 0,
                                    }}
                                />{" "}
                            </ListItemButton>
                        </NextLink>
                    </ListItem>
                ))}
            </List>
        </Cajon>
    );
};

export default SideMenu;