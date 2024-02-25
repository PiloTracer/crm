import React from 'react';
import Uploads from '@/components/Dashboard/Uploads';
import { useSession } from "next-auth/react";
import scss from "@/components/Layout/Layout.module.scss";
import UploadResultsGrid from '@/components/Dashboard/UploadResults/UploadResults';

const Upload = () => {
    const { data: session } = useSession();

    return (
        <>
            <main className={scss.main}>
                <Uploads />
                <UploadResultsGrid />
            </main>
        </>
    )
}

export default Upload;

