// pages/api/fetchData.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { config } from '../../../../config/config';
import axios from 'axios';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { merchant } = req.query;
  //const { merchant, postid } = req.query;

  try {
    const response = await axios.get(`${config.API_URL_MERCHANT_ACTIVE}?merchant=${merchant}`);
    res.status(200).json(response.data);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching data' });
  }
}
