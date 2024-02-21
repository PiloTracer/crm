import axios from "axios"

export type User = {
  _id: string,
  type: string | null,
  role: string,
  fullname: string,
  username: string,
  password: string | null,
  message: string | null,
  err: string | null,
  merchant: string,
  active: boolean,
  created: number | null,
  created_by: string | null,
  created_merchant: string | null
}

export type MyLoginRequest = {
  username: string;
  password: string
};

export type RequestData = {
  username: string,
  merchant: string,
  message: string | null
}

export type ResponseData = {
  message: string,
  error: string
}

//this is not working for Next.Auth
//
//export async function Authenticate(requestdata: MyLoginRequest) {
//  const API_URL = '/api/fetch/fetchAuth';
//  const customConfig = {
//    headers: {
//      'Content-Type': 'application/x-www-form-urlencoded'
//    }
//  };
//
//  const response = await axios.post(
//        API_URL,
//        requestdata,
//        customConfig
//  );
//
//  //throw Error("auth: " + JSON.stringify(response));
//
//  const data = response.data;
//  if (data === undefined 
//    || data?.token === undefined 
//    || data?.token === "")
//  {
//    throw Error("failed!" + JSON.stringify(data));
//  }
//
//  return data;
//}

export async function CreateUserFnc<ResponseData>(requestdata: User) {
  console.log(requestdata);
  const API_URL = '/api/fetch/fetchUserCreate';
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

  if (data === undefined || data.err !== null) {
    throw Error("failed!" + JSON.stringify(data));
  }

  console.log(data);
  return data;
}

export async function UpdateUserFnc<User>(requestdata: RequestData) {
  const API_URL = '/api/fetch/fetchUserActDeact';
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

  if (data === undefined
  || data.message === undefined
  || data.message !== "ok") {
    throw Error("update error!" + JSON.stringify(data));
  }

  return data;
}

export async function DeleteUserFnc<ResponseData>(requestdata: RequestData) {
  const API_URL = '/api/fetch/fetchUserDelete';
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
  return data;
}