/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    webpack: (config, context) => {
        // Enable polling based on env variable being set
        if (process.env.NEXT_WEBPACK_USEPOLLING === 'true') {
            config.watchOptions = {
                poll: 1000,
                aggregateTimeout: 300
            }
        }
        return config
    },
};

export default nextConfig;
