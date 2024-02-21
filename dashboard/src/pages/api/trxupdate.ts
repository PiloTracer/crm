import type { NextApiRequest, NextApiResponse } from 'next'

type RequestData = {
  _id: string,
  status: string,
  reference?: string,
  descriptor?: string,
  reason?: string
}

type ResponseData = {
  _id: string,
  status: string
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  //'use server'

  if (req.method === 'POST') {
    // Process a POST request
  } else {
    res.status(200).json({ message: 'Hello from Next.js!' })
  }
}
