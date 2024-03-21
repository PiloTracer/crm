// pages/api/fetch/fetchGetHash.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { consts } from '../../../../config/config';
import crypto from 'crypto';
import { SHA256 } from 'crypto-js';

function hashStringWithSalt(inputString: string): string {
  const hash = crypto.createHash('sha1');
  const salt: string = consts.SALT;
  hash.update(inputString + salt);
  return hash.digest('hex');
}

function serializeToJson(data: any): string {
  return JSON.stringify(data, Object.keys(data).sort(), 0);
}

function generateHashFromJson(data: any): string {
  const jsonString = JSON.stringify(data, Object.keys(data).sort(), 0);
  return SHA256(jsonString).toString();
}

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
    return;
  }

  const msg = req.body;

  if (!msg) {
    res.status(400).send('Salute parameter is required');
    return;
  }

  try {
    const output = generateHashFromJson(msg);
    res.status(200).json({ token: output });
  } catch (error) {
    res.status(500).send('Error processing request');
  }
}
