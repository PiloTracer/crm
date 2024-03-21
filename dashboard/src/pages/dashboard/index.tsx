import { NextPage } from "next";
import { useSession } from "next-auth/react";
import Router, { useRouter } from "next/router";
import { useEffect } from "react";
import Home from "./Home";

const Protected: NextPage = (): JSX.Element => {
    const { status, data } = useSession();
    const router = useRouter();
    const mypath = `/auth/signin?callbackUrl=${encodeURIComponent(router.asPath)}`;

    useEffect(() => {
        if (status === "unauthenticated") Router.replace(mypath);
    }, [mypath, status]);

    if (status === "authenticated") {
        return (
            <Home />
        );
    } else {
        return <div>loading</div>;
    }
};

export default Protected;
