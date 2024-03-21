import React, { useEffect, useState } from 'react';
import Trxs from '@/components/Dashboard/Transactions';
import { useSession } from "next-auth/react";
import scss from "@/components/Layout/Layout.module.scss";
import TransactionsGrid from '@/components/Dashboard/Transactions/Trxs';
import { GetMerchantsActive } from '@/components/DbFunctions/GetMerchantsActive';

const Transactions = () => {
    const { data: session, status } = useSession()
    const [merchactive, setMerchactive] = useState<string[] | null>(null);

    useEffect(() => {
        const fetchMerchantsActive = async () => {
            const data = await GetMerchantsActive();
            const newm = [];
            if (data.length > 0) {
                for (let i = 0; i < data.length; i++) {
                    if (data[i] !== '*') {
                        newm.push(data[i]);
                    }
                }
            }
            setMerchactive(newm);
        };
        fetchMerchantsActive();
    }, []); // Empty dependency array means this runs once on mount


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
                {merchactive && <TransactionsGrid mactive={merchactive} />}
            </main>
        </>
    )
}

export default Transactions;
