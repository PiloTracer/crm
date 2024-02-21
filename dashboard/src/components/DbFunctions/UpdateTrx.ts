import axios from "axios"

export type RequestDataExtra = {
  type: string,
  context: string,
  trxtype: string,
  amnt: number,
  fees: number,
  description: string,
  target: string,
  currency: string,
  method: string,
  channel: string,
  token: string | null,
  checksum: string | null
}

export type RequestData = {
  username: string,
  merchant: string,
  by_merchant: string,
  id: string,
  status: string,
  reference?: string,
  descriptor?: string,
  reason?: string,
  transaction: RequestDataExtra
}

export class TrxPromise<T> extends Promise<T>{
  _id: string = "";
  customeraccount: string = "";
  amount: number = 0;
  fees: number = 0;
  cxname: string = "";
  routing: string = "";
  bankaccount: string = "";
  accounttype: string = "";
  email: string = "";
  address: string = "";
  parent: string = "";
  type: string = "";
  method: string = "";
  created: string = "";
  createdf: string = "";
  modified: string = "";
  merchant: string = "";
  status: string = "";
  descriptor: string = "";
  reference: string = "";
  reason: string = "";
  message: string = "";
}

export type Transaction = {
  "_id": string,
  "customeraccount": string,
  "amount": number,
  "fees": number,
  "cxname": string,
  "routing": string,
  "bankaccount": string,
  "accounttype": string,
  "email": string,
  "address": string,
  "trxtype": string,
  "parent": string,
  "type": string,
  "method": string,
  "created": string,
  "createdf": string,
  "modified": string,
  "merchant": string,
  "status": string,
  "descriptor": string,
  "reference": string,
  "reason": string,
  "message": string
}

export type ResponseData = {
  message: string,
  msg: string
}

export async function UpdateTransactionFnc<Transaction>(requestdata: RequestData) {
  console.log(requestdata);
  const API_URL = '/api/fetch/fetchTransactionUpdate';
  const customConfig = {
    headers: {
      'Content-Type': 'application/json'
    }
  };
  var r: any;
  try {
    const response = await axios.post(
          API_URL,
          requestdata,
          customConfig
    );

    const data = await response.data;
    r = data;
    if (data.message === "nok") {
      throw Error("failed! " + JSON.stringify(data));
    }

  } catch (error) {
    throw error;
  } finally {
    return r;
  }
}


export class ValidationError extends Error {
  details: any;

  constructor(message: string, details: any = null) {
    super(message);
    this.name = 'ValidationError';
    this.details = details;
  }
}
