import React from 'react';
import Trxs from '@/components/Dashboard/Transactions';
import { useSession } from "next-auth/react";
import scss from "@/components/Layout/Layout.module.scss";

const Transactions = () => {
    const { data: session, status } = useSession()
    if (status === 'loading') {
        return (
            <>
                <main className={scss.main}>
                    <div>Loading...</div>
                </main>
            </>
        )
    }
    return (
        <>
            <main className={scss.main}>
                <Trxs>
                </Trxs>
            </main>
        </>
    )
}

export default Transactions;
