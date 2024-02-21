import NextAuth, { NextAuthOptions } from "next-auth";
//import AppleProvider from 'next-auth/providers/apple'
//import FacebookProvider from 'next-auth/providers/facebook'
//import GoogleProvider from 'next-auth/providers/google'
//import EmailProvider from 'next-auth/providers/email'
import CredentialsProvider from "next-auth/providers/credentials";
import Router, { useRouter } from "next/router";
import { error } from 'console';
import React, { useState, useEffect } from 'react';
import { MyLoginRequest, User, RequestData } from '@/components/DbFunctions/UpdateUser'

import axios from 'axios';
import { config } from "../../../../config/config";



export const authOptions: NextAuthOptions = {
  secret: process.env.NEXTAUTH_SECRET,

  providers: [
    CredentialsProvider({
      name: "credentials",
      credentials: {},
      async authorize(credentials, req) {
        //const API_URL = '/api/fetch/fetchAuth';
        const API_URL = config.API_URL_USER_AUTH;
        const customConfig = {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        };
        const { username, password } = credentials as {
          username: string;
          password: string;
        };

        const requestdata: MyLoginRequest = {
          username: username,
          password: password
        };

        //const data: any = await Authenticate(request)
        const response = await axios.post(
          API_URL,
          requestdata,
          customConfig
        );
        const data = response.data;

        if (
          data === undefined
          || data === null
          || data.token === undefined
          || data.token === null
          || data.token === ""
        ) {
          throw Error("failed!" + JSON.stringify(data));
        }

        // if everything is fine
        const parsed = {
          name: data.fullname,
          email: data.username,
          //xrole: data.roles,
          xid: data._id,
          xmsg: data.message,
          xmerchant: data.merchant,
          xrole: data.role,
          xtype: data.type,
          xtoken: data.token
        }

        return parsed as any;
      },
    }),

  ],
  session: {
    maxAge: 1 * 60 * 60,
    strategy: "jwt"
  },
  pages: {
    signIn: "/auth/signin",
    error: '/error',
    signOut: '/'
  },

  jwt: {
    maxAge: 1 * 60 * 60
  },

  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.xmsg = user.xmsg;
        token.xmerchant = user.xmerchant;
        token.xtype = user.xtype;
        token.xid = user.xid;
        token.xrole = user.xrole;
        token.xtoken = user.xtoken;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.xmsg = String(token.xmsg);
        session.user.xmerchant = String(token.xmerchant);
        session.user.xtype = String(token.xtype);
        session.user.xid = String(token.xid);
        session.user.xrole = token.xrole as string[];
        session.user.xtoken = String(token.xtoken);
      }
      return session;
    },
  },

  //  callbacks: {
  //    jwt(params) {
  //      // update token
  //      if (params.user?.xmsg) {
  //        params.token.xmsg = params.user.xmsg;
  //      }
  //      // return final_token
  //      return params.token;
  //    },
  //    session({ session, token, user }) {
  //      return session
  //    },
  //
  //    //session(params) {
  //    //  if (params.session.user) {
  //    //    params.session.user.xid = String(params.token.xid?? "");
  //    //    params.session.user.xmsg = String(params.token.xmsg?? "");
  //    //    //session.user.xrole = Array<string>(user.xid?? new Array());
  //    //  }
  //    //  return params.session;
  //    //}
  //
  //  }
};

export default NextAuth(authOptions);
