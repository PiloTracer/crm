import axios from "axios"

export type TransactionDoc = {
  message: string,
  id: string,
  rev: string,
  error: string,
  doc: Transaction
}

export type Transaction = {
  _id: string | "",
  merchant: string | "",
  customer: string | "",
  amnt: number | 0,
  currency: string | "",
  type: string | "",
  context: string | "",
  trxtype: string | "",
  method: string | "",
  description: string | "",
  reference: string | "",
  amntsign: number | 0,
  feesign: number | 0,
  totsign: number | 0,
  created: number | 0,
  status: string | "",
  channel: string | "",
  message: string | "",
  checksum: string | "",
  reversed: boolean | false,
  origen: string | ""
}

export type RequestData = {
  username: string,
  merchant: string,
  message: string | null
}

export type ResponseData = {
  message: string,
  msg: string
}

export type ResponseCreate = {
  message: string,
  id: string,
  rev: string
}

export type AdjustmentData = {
  created: {
    id: string,
    merchant: string,
    created: number | null
  },
  status: { 
    status : string,
    detail : string
  },
  merchant: {
    merchant: string,
    id : string | null,
    customer: string | null,
    bank_name: string | null,
    branch: string | null
  },
  type: string,
  context: string,
  trxtype: string,
  amnt: number,
  fee: number | null,
  method: string,
  description: string,
  reference: string,
  currency: string,
  channel: string,
  token: string,
  checksum: string | null,
  origen: string | null
}

export async function CreateTransactionFnc<Transaction>(requestdata: AdjustmentData) {
  console.log(requestdata);
  let data: any;
  const API_URL = '/api/fetch/fetchBalanceCreate';
  const customConfig = {
    headers: {
      'Content-Type': 'application/json'
    }
  };
  try {
    const response = await axios.post(
          API_URL,
          requestdata,
          customConfig
    );

    data = await response.data as TransactionDoc;

    //if (data === undefined || data?.message === "nok") {
    //  throw Error("creation failed!" + JSON.stringify(data));
    //}

  } catch(error) {
    throw error;

  } finally {
    console.log("received data: ", data);
    return data?.doc as Transaction;
  }
}

export async function ReverseAdjustmentFnc<Transaction>(requestdata: RequestData) {
  const API_URL = '/api/fetch/fetchBalanceReverse';
  const customConfig = {
    headers: {
      'Content-Type': 'application/json'
    }
  };
  const response = await axios.post(
        API_URL,
        requestdata,
        customConfig
  );

  const data = await response.data;

  if (data === undefined || data.error !== null) {
    throw Error("failed!" + JSON.stringify(data));
  }

  console.log(data);
  return data?.doc as Transaction;
}