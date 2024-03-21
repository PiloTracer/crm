// pages/api/sendData.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { config } from '../../../../config/config';

import axios from 'axios';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const response = await axios.get(
      config.API_URL_MERCHANTS_ACTIVE
    );

    res.status(200).json(response.data);
  } catch (error) {
    res.status(500).json({ message: 'Error sending data' });
  }
}
