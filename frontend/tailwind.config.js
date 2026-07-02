/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f4f8',
          100: '#dbe3ee',
          200: '#bdcbe0',
          300: '#91aacc',
          400: '#5f84b4',
          500: '#3d6397',
          600: '#2e4e7c',
          700: '#264066',
          800: '#213756',
          900: '#1d2f49',
          950: '#0f172a', // Slate-900 / Navy สีเข้มหรูหรา
        },
        gold: {
          500: '#d4af37', // Metallic Gold / Champagne
          600: '#b89229',
        }
      },
      fontFamily: {
        sans: ['Outfit', 'Inter', 'Sarabun', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
