/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: [],
  },
  serverExternalPackages: [
    'three',
    '@react-three/fiber',
    '@react-three/drei',
  ],
}

export default nextConfig;
