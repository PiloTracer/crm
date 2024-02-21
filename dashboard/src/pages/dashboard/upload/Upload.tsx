import React from 'react';
import DropBox from '@/components/Dashboard/DropBox';
import { useSession } from "next-auth/react";
import scss from "@/components/Layout/Layout.module.scss";

const Upload = () => {
    const { data: session } = useSession();

    return (
        <>
            <main className={scss.main}>
                <DropBox>
                </DropBox>
            </main>
        </>
    )
}

export default Upload;


