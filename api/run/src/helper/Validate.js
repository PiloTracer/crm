export function validateData(data) {
    const errors = {};
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // Check "authchecksum" for a maximum of 50 characters
    if (typeof data.authchecksum !== 'string' || data.authchecksum.length > 50) {
        errors.authchecksum = 'Authchecksum must be a string with a maximum of 50 characters.';
    }

    // Check "authemail" for valid format and length
    if (typeof data.authemail !== 'string' || !emailRegex.test(data.authemail) || data.authemail.length > 100) {
        errors.authemail = 'Authemail must be a valid email address and no longer than 100 characters.';
    }

    // Check "id" for a maximum of 32 characters
    if (typeof data._id !== 'string' || data._id.length > 32) {
        errors._id = 'ID must be a string with a maximum of 32 characters.';
    }

    // Check "customeraccount" for a maximum of 20 characters
    if (typeof data.customeraccount !== 'string' || data.customeraccount.length > 20) {
        errors.customeraccount = 'Customeraccount must be a string with a maximum of 20 characters.';
    }

    // Check "amount" for numbers and "." as decimal separator
    const amountRegex = /^\d+(\.\d+)?$/;
    if (typeof data.amount !== 'string' || !amountRegex.test(data.amount)) {
        errors.amount = 'Amount must be a number and can only contain digits and a decimal point.';
    }

    // Check "currency" for a size of 3 characters
    if (typeof data.currency !== 'string' || data.currency.length != 3) {
        errors.currency = 'Currency must have 3 characters exactly.';
    }

    // Check "trxtype" for a maximum of 20 characters
    if (typeof data.trxtype !== 'string' || data.trxtype.length > 20) {
        errors.trxtype = 'Trxtype must be a string with a maximum of 20 characters.';
    }

    // Check "cxname" for a maximum of 80 characters
    if (typeof data.cxname !== 'string' || data.cxname.length > 80) {
        errors.cxname = 'Cxname must be a string with a maximum of 80 characters.';
    }

    // Check "routing" for a maximum of 20 characters
    if (typeof data.routing !== 'string' || data.routing.length > 20) {
        errors.routing = 'Routing must be a string with a maximum of 20 characters.';
    }

    // Check "bankaccount" for a maximum of 20 characters
    if (typeof data.bankaccount !== 'string' || data.bankaccount.length > 20) {
        errors.bankaccount = 'Bankaccount must be a string with a maximum of 20 characters.';
    }

    // Check "accounttype" for 1 character
    if (typeof data.accounttype !== 'string' || data.accounttype.length != 1) {
        errors.accounttype = 'Accounttype must be a string with 1 character.';
    }

    // Check "email" for valid format and length
    if (typeof data.email !== 'string' || !emailRegex.test(data.email) || data.email.length > 100) {
        errors.email = 'Email must be a valid email address and no longer than 100 characters.';
    }

    // Check "address" length
    if (typeof data.address !== 'string' || data.address.length > 200) {
        errors.address = 'Address must be a string with a maximum of 200 characters.';
    }

    // Check "parent" length
    if (typeof data.parent !== 'string' || data.parent.length > 20) {
        errors.parent = 'Parent must be a string with a maximum of 20 characters.';
    }

    // Check "merchant" length
    if (typeof data.merchant !== 'string' || data.merchant.length > 20) {
        errors.merchant = 'Merchant must be a string with a maximum of 20 characters.';
    }

    // Check "comment" length
    if (typeof data.comment !== 'string' || data.comment.length > 20) {
        errors.comment = 'Comment must be a string with a maximum of 20 characters.';
    }

    // Check "apikey" length
    if (typeof data.apikey !== 'string' || data.apikey.length > 50) {
        errors.apikey = 'Apikey must be a string with a maximum of 50 characters.';
    }

    // Check "version" for numbers or "."
    const versionRegex = /^\d+(\.\d+)*$/;
    if (typeof data.version !== 'string' || !versionRegex.test(data.version) || data.version.length > 20) {
        errors.version = 'Version must only contain numbers and dots.';
    }

    // Check "method" length
    if (typeof data.method !== 'string' || data.method.length > 20) {
        errors.method = 'Method must be a string with a maximum of 20 characters.';
    }

    return {
        isValid: Object.keys(errors).length === 0,
        errors,
    };
}
