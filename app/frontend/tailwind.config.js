/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}', // Adjust this path to match your project's structure
    './components/**/*.vue',
    './*.vue',
    './public/index.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
