import Dashboard from "@/pages/dashboard";
import { useSession } from "next-auth/react";
import scss from "../components/Layout/Layout.module.scss";
import React from "react";
import SignIn from "./auth/signin";

const Home: React.FC = () => {
    const { data: session } = useSession();

    return (
        <main className={scss.main}>
            {session && <Dashboard />}
            {!session && <SignIn />}
        </main>
    );
};

export default Home;