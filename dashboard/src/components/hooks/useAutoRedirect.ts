// hooks/useAutoRedirect.ts
import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { getSession } from 'next-auth/react';

const useAutoRedirect = () => {
  const router = useRouter();

  useEffect(() => {
    const checkSession = async () => {
      const session = await getSession();
      if (!session) {
        // Session has expired, redirect to the login page
        router.push('/auth/signin');
      }
    };

    checkSession();
  }, [router]);
};

export default useAutoRedirect;
