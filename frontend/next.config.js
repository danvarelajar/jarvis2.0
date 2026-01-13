/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_BACKEND_URL: process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000',
    NEXT_PUBLIC_OPIK_ENDPOINT: process.env.NEXT_PUBLIC_OPIK_ENDPOINT || 'https://api.opik.ai',
  },
}

module.exports = nextConfig
