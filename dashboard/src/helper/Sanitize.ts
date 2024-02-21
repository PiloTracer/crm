function sanitizeString(str: string): string {
    // Replace special characters with HTML entities or remove them
    return str.replace(/[&<>"']/g, (match) => {
        switch (match) {
            case '&': return '&amp;';
            case '<': return '&lt;';
            case '>': return '&gt;';
            case '"': return '&quot;';
            case "'": return '&#39;';
            default: return match;
        }
    }).toLowerCase();
}

export function isSafeString(inputString: string): boolean {
    const disallowedChars = ['(', ')', '[', ']', '<', '>', '@', '/', '\\', '|', '_', '"', "!", "~", "%", '^'];

    for (const char of disallowedChars) {
        if (inputString.includes(char)) return false;
    }

    return true;
}

export function isSafeStringRe(inputString: string): boolean {
    const sanitized = sanitizeChars(inputString);
    return sanitized.length === inputString.length;
}


export function sanitizeChars(inputString: string): string {
    return inputString.replace(/[\[\(\)\]<>\\/\"@\/\|_!~%\^]/g, '');
}

export function lowercaseObject(obj: { [key: string]: any }): { [key: string]: string } {
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      obj[key] = obj[key].toLowerCase();
    }
  }
  return obj;
}

export function isvalidJSON<T extends Record<string, any>>(obj: T): boolean {
    var result = true;
    for (const key in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, key)) {
            const value = obj[key];
            // Check if the value is a string and sanitize it
            if (typeof value === 'string') {
                result = isSafeStringRe(value);
            } else if (typeof value === 'object' && value !== null) {
                // If the value is an object (but not null), sanitize it recursively
                result = isvalidJSON(value);
            }
        }
        if (result === false) return false;
    }
    return result;
}

export function sanitizeJSON<T extends Record<string, any>>(obj: T): T {
    const sanitizedObj = {} as Record<string, any>;
    for (const key in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, key)
        && !key.toLowerCase().includes("type")
        && key.toLowerCase() != "token" ) {
            const value = obj[key];
            // Check if the value is a string and sanitize it
            if (typeof value === 'string') {
                sanitizedObj[key] = sanitizeString(value);
            } else if (typeof value === 'object' && value !== null) {
                // If the value is an object (but not null), sanitize it recursively
                sanitizedObj[key] = sanitizeJSON(value);
            } else {
                // For other types, copy as is
                sanitizedObj[key] = value;
            }
        } else {
            sanitizedObj[key] = obj[key];
        }
    }
    return sanitizedObj as T;
}

// Function to decode HTML entities
export const decodeHTMLEntities = (text: string): string => {
  const textArea = document.createElement('textarea');
  textArea.innerHTML = text;
  return textArea.value;
};

// Example usage
//const myObject = {
//    name: "<script>alert('xss')</script>",
//    age: 30,
//    details: {
//        address: "123 Main St & Co.",
//        notes: "Check for < and > symbols"
//    }
//};
//
//const sanitizedObject = sanitizeJSON(myObject);
//console.log(sanitizedObject);
