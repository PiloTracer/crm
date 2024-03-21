// pages/api/sendData.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { config } from '../../../../config/config';

import axios from 'axios';


export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const data = req.body;
  const authHeader: string = req.headers.authorization as string;
  
  const customConfig = {
    headers: {
          Authorization: authHeader,
          'Content-Type': 'application/json'
    },
  };

  try {
    const response = await axios.post(
      config.API_URL_API_CREATE,
      data,
      customConfig
    );

    res.status(200).json(response.data);
  } catch (error) {
    res.status(500).json({ message: 'Error sending data' });
  }
}
