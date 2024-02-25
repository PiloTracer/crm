import { config } from '../../../../../config/config';
import NodeCache from 'node-cache';
import axios from 'axios';
import crypto from 'crypto';
import { isvalidJSON, lowercaseObject } from '../../../../helper/Sanitize';
import { validateData } from '../../../../helper/Validate';

const myCache = new NodeCache({ stdTTL: 300, checkperiod: 30 });

export async function POST(
    req, res
) {

    let err = {};

    try {
        let j = await req.json();

        const questionMarkIndex = req.url.indexOf("?");

        const substringBeforeQuestionMark = questionMarkIndex !== -1
            ? req.url.substring(0, questionMarkIndex)
            : req.url;

        const { searchParams } = new URL(req.url);
        const fields = substringBeforeQuestionMark.split("/");
        const method = searchParams.get('m');
        const version = fields[5];
        const apikey = fields[6];
        const cacheKey = apikey; // Unique key for this particular cache
        const cachedData = myCache.get(cacheKey);

        //1....................
        //cached data

        //throw Error(JSON.stringify(j));

        if (!isvalidJSON(j)) {
            throw Error("Request contains invalid characters");
        };

        const customConfig = {
            headers: {
                'Content-Type': 'application/json'
            }
        };

        let apiauth = {};

        // Initialize from cache or db
        if (cachedData) {
            apiauth = cachedData;
        } else {
            const response = await axios.post(
                config.API_URL_GET_API_AUTH,
                { email: j.authentication.email.toLowerCase(), apitoken: apikey },
                customConfig
            );

            // Save new data to cache
            myCache.set(cacheKey, response.data);
            apiauth = response.data;
        }

        // Validate checksum
        if (
            apiauth?.message
            && apiauth.message == "ok"
            && apikey == apiauth.apitoken
        ) {
            let hashraw = j.transaction.customeraccount +
                j.transaction.amount +
                j.transaction.currency +
                j.transaction.routing +
                j.transaction.email +
                j.transaction.trxtype +
                j.transaction.merchant +
                apiauth.apisecret

            let hash = crypto.createHash('sha1').update(hashraw).digest('hex');
            if (hash != j.authentication.checksum) {
                throw Error("Error sending data: Validation failed");
            }
        } else {
            throw Error("Wrong request " + apiauth.apitoken + "  " + apikey + "  " + apiauth.message);
        }

        j.transaction = lowercaseObject(j.transaction);

        const data = {
            id: apiauth.merchant + "_" + j.transaction.id,
            authchecksum: j.authentication.checksum,
            authemail: j.authentication.email,
            customeraccount: j.transaction.customeraccount,
            amount: j.transaction.amount,
            currency: j.transaction.currency,
            cxname: j.transaction.cxname,
            routing: j.transaction.routing,
            bankaccount: j.transaction.bankaccount,
            accounttype: j.transaction.accounttype,
            email: j.transaction.email,
            address: j.transaction.address,
            trxtype: j.transaction.trxtype,
            parent: j.transaction.parent,
            merchant: j.transaction.merchant,
            comment: j.transaction.comment,
            method: method,
            version: version,
            apikey: apikey,
            origen: "customer"
        }

        // Validate data
        const { isValid, errors } = validateData(data);
        err = errors;
        if (!isValid) {
            throw Error("Wrong format of data");
        }

        const response = await axios.post(
            config.API_URL_TRANSACTION_ADD,
            data,
            customConfig
        );

        response.data.ext = errors;

        return Response.json(response.data, { headers: { "Content-Type": "application/json" }, status: 200 });
    } catch (error) {
        return Response.json({ status: "nok", message: "failed", reference: null, error: error.message, ext: err }, { headers: { "Content-Type": "application/json" }, status: 500 });
    }
}