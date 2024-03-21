// pages/api/sendData.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { config } from '../../../../config/config';

import axios from 'axios';
import { sanitizeJSON } from '../../../helper/Sanitize';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const data = req.body;
  const customConfig = {
    headers: {
      'Content-Type': 'application/json'
    }
  };

  try {

    //const sanitizedObject = sanitizeJSON(data);

    const response = await axios.post(
      config.API_URL_BALANCE_CREATE,
      data,
      customConfig
    );

    res.status(200).json(response.data);
  } catch (error) {
    res.status(500).json({ message: 'Error sending data' });
  }
}
