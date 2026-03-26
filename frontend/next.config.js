/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Allow CORS for API calls to agent
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
