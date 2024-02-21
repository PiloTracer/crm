const rateLimit = require('express-rate-limit');
const { runMiddleware } = require('./run-middleware');

// Define the rate limiter
const limiter = rateLimit({
    windowMs: 5 * 1000, // 5 seconds
    max: 100, // limit each IP to 100 requests per windowMs
});

// Export a middleware function
module.exports = function (req, res) {
    return runMiddleware(req, res, limiter);
};
