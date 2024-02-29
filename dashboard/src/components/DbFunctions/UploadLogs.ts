import axios from "axios"

export type UploadLogs = {
  "_id": string,
  "created": number,
  "createds": number,
  "created_merchant": string | null,
  "created_by": string | null,
  "merchant": string | null,
  "message": string | null,
  "partdate": string | null,
  "doc_id": string | null,
  "parent": string | null,
  "status": boolean | false,
  "src": string | null,
  "extra": {} | null
}

export async function CreateTransactionFnc(req = null) {
  //this is just a place holder, 
  //this function is not neceesary at this time
  return []
}