import React, { useState, useEffect } from 'react';
import ExampleWithProviders from '@/components/Dashboard/Users';
import { useSession } from "next-auth/react";
import scss from "@/components/Layout/Layout.module.scss";
import { GetMerchantsActive } from '@/components/DbFunctions/GetMerchantsActive';
import ApiCred from '@/components/Dashboard/ApiCred';


const Settings = () => {
    const { data: session, status } = useSession();
    const [merchactive, setMerchactive] = useState<string[] | null>(null);

    useEffect(() => {
        const fetchMerchantsActive = async () => {
            const data = await GetMerchantsActive();
            setMerchactive(data);
        };
        fetchMerchantsActive();
    }, []); // Empty dependency array means this runs once on mount

    if (status === 'loading') {
        return (
            <main className={scss.main}>
                <div>Loading...</div>
            </main>
        );
    }

    return (
        <main className={scss.main}>
            <ApiCred />
            {merchactive && <ExampleWithProviders mactive={merchactive} />}
        </main>
    );
}

export default Settings;
