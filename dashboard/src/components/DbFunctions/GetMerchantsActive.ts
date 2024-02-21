import axios from "axios"

export async function GetMerchantsActive() {
  console.log("getting Merchants Active");
  const API_URL = '/api/fetch/fetchMerchantsActive';
  const response = await axios.get(API_URL);

  const data = await response.data;

  if (data === undefined) {
    throw Error("failed!" + JSON.stringify(data));
  }

  return data;
}