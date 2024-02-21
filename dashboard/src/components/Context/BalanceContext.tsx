import React, { createContext, useContext, useState, Dispatch, SetStateAction, ReactNode } from 'react';

interface UpdateGridContextType {
    needsUpdate: boolean;
    setNeedsUpdate: Dispatch<SetStateAction<boolean>>;
}

const UpdateGridContext = createContext<UpdateGridContextType>({
    needsUpdate: false,
    setNeedsUpdate: () => { }
});

export const useUpdateGridContext = () => useContext(UpdateGridContext);

interface UpdateGridProviderProps {
    children: ReactNode;
}

export const UpdateGridProvider: React.FC<UpdateGridProviderProps> = ({ children }) => {
    const [needsUpdate, setNeedsUpdate] = useState<boolean>(false);

    return (
        <UpdateGridContext.Provider value={{ needsUpdate, setNeedsUpdate }}>
            {children}
        </UpdateGridContext.Provider>
    );
};
