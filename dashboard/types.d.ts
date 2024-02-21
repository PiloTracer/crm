import { User as NextAuthUser } from 'next-auth'

declare module 'next-auth' {
  interface User extends NextAuthUser {
    xtype: string;
    xmsg: string;
    xmerchant: string;
    xid: string;
    xrole: string;
    xtoken: string;
  };
  interface Session {
      user: {
          xtype: string;
          xmsg: string;
          xmerchant: string;
          xid: string;
          xrole: string;
          xtoken: string;
      } & DefaultSession['user'];
  }
}


