import crypto from 'crypto';
import { consts } from '../../config/config';

const MONTHS = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

export const months = (config: any) => {
  const cfg = config || {};
  const count = cfg.count || 12;
  const section = cfg.section;
  const values = [];
  let i, value;

  for (i = 0; i < count; ++i) {
    value = MONTHS[Math.ceil(i) % 12];
    values.push(value.substring(0, section));
  }

  return values;
};

export function isEmptyObject(obj: Object): boolean {
    return Object.keys(obj).length === 0;
}


export function hashStringWithSalt(inputString: string): string {
    const salt = consts.SALT;
    const hash = crypto.createHash('sha1');
    hash.update(inputString + salt);
    return hash.digest('hex');
}

