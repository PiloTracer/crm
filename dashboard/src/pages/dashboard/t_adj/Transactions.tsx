import React, { useEffect, useState } from 'react';
import { useSession } from "next-auth/react";
import scss from "@/components/Layout/Layout.module.scss";
import { GetMerchantsActive } from '@/components/DbFunctions/GetMerchantsActive';
import AdjustmentGrid from '@/components/Dashboard/T_Adjustments';
import BalanceGrid from '@/components/Dashboard/T_Balances';
import { UpdateGridProvider } from '@/components/Context/BalanceContext';

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
            <UpdateGridProvider>
                <main className={scss.main}>
                    <BalanceGrid>
                    </BalanceGrid>
                    {merchactive && <AdjustmentGrid mactive={merchactive} />}
                </main>
            </UpdateGridProvider>
        </>
    )
}

export default Transactions;
