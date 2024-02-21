import { NextPage } from "next";
import { useSession } from "next-auth/react";
import Router, { useRouter } from "next/router";
import { useEffect } from "react";
import Dashboard from "./Dashboard";

const Protected: NextPage = (): JSX.Element => {
    const { status, data } = useSession();
    const router = useRouter();
    const mypath = `/auth/signin?callbackUrl=${encodeURIComponent(router.asPath)}`;

    useEffect(() => {
        if (status === "unauthenticated") Router.replace(mypath);
    }, [mypath, status]);

    if (status === "authenticated") {
        return (
            <Dashboard />
        );
    } else {
        return <div>loading</div>;
    }
};

export default Protected;
