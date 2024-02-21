import axios from "axios"

export type Transaction = {
  key: string,
  value: {
    amntsign: number,
    feesign: number,
    totsign: number
  }
}

export async function CreateTransactionFnc(req = null) {
  //this is just a place holder, 
  //this function is not neceesary at this time
  return []
}