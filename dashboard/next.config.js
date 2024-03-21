// If you're using JSDoc for type checking, keep this line
/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    webpack: (config) => {
        // Enable polling based on env variable being set
        if (process.env.NEXT_WEBPACK_USEPOLLING === 'true') {
            config.watchOptions = {
                poll: 1000,
                aggregateTimeout: 300
            }
        }
        return config;
    },
};

module.exports = nextConfig;
