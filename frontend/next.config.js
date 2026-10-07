/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  webpack: (config, { isServer }) => {
    config.experiments = {
      ...config.experiments,
      asyncIteration: true,
    };
    return config;
  },
};

module.exports = nextConfig;
