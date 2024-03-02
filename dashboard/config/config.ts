// config.ts
export const config = {
  API_URL_MERCHANT_ACTIVE: 'http://10.5.0.6:8000/merchant/merchantactive',
  API_URL_BALANCE_ADJUSTMENTS: 'http://10.5.0.6:8000/pull/adjustments',
  API_URL_BALANCE_BALANCES: 'http://10.5.0.6:8000/balance/balances',
  API_URL_UPLOAD_LOGS: 'http://10.5.0.6:8000/pull/latestuploads',
  API_URL_BALANCE_REVERSE: 'http://10.5.0.6:8000/balance/reverse',
  API_URL_TRANSACTIONS: 'http://10.5.0.6:8000/pull/transactions',
  API_URL_BALANCE_CREATE: 'http://10.5.0.6:8000/balance/create',
  API_URL_PROCESSOR_TRANSACTION_CREATE: 'http://10.5.0.6:8000/pull/transaction/create',
  API_URL_TRANSACTION_UPDATE: 'http://10.5.0.6:8000/pull/updatetrx',
  API_URL_FILES_UPLOAD: 'http://10.5.0.6:8000/pull/filesupload',
  API_URL_API_CREATE: 'http://10.5.0.6:8000/messages/user/createapi',
  API_URL_USERS: 'http://10.5.0.6:8000/messages/users',
  API_URL_USER_AUTH: 'http://10.5.0.6:8000/messages/user/token',
  API_URL_USERCREATE: 'http://10.5.0.6:8000/messages/user/signup',
  API_URL_USERDELETE: 'http://10.5.0.6:8000/messages/user/delete',
  API_URL_USERACTDEACT: 'http://10.5.0.6:8000/messages/user/activate_deactivate',
  API_URL_MERCHANTS_ACTIVE: 'http://10.5.0.6:8000/merchant/listactive',
  API_URL_RABBIT_UPLOAD: 'http://10.5.0.8:5672',
};

export const consts = {
  SALT: 'AKksl0Fsdk200fGjK100$',
};

export function getWebSocketUrl(): string {
  const hostname = typeof window !== 'undefined' ? window.location.hostname : 'localhost';
  const port = '4500'; // Define the port if it's different from the hostname's port
  const protocol = hostname === 'localhost' ? 'ws' : 'wss'; // Use wss for secure WebSocket if not localhost

  return `${protocol}://${hostname}:${port}/ws`;
}
