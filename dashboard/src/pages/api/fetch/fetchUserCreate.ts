// pages/api/sendData.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { config } from '../../../../config/config';
import { authOptions } from "../auth/[...nextauth]"

import axios from 'axios';
import { getSession } from 'next-auth/react';
import { getServerSession } from "next-auth"

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  //const session = await getSession({ req });
  const session = await getServerSession(req, res, authOptions)
  const data = req.body;
  var customConfig;
  customConfig = {
    headers: {
      Authorization: `Bearer ${session?.user?.xtoken}`,
      'Content-Type': 'application/json'
    },
  };

  try {
    const response = await axios.post(
      config.API_URL_USERCREATE,
      data,
      customConfig
    );

    res.status(200).json(response.data);
  } catch (error) {
    res.status(500).json({ message: 'Error sending data' });
  }
}
