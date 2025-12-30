/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'messenger-blue': '#0084ff',
        'messenger-blue-dark': '#0066cc',
        'messenger-gray': '#f0f2f5',
        'messenger-text': '#1c1e21',
        'messenger-secondary': '#65676b'
      },
      fontFamily: {
        'poppins': ['Poppins', 'sans-serif'],
        'sf-pro': ['SF Pro Display', 'system-ui', 'sans-serif']
      }
    },
  },
  plugins: [],
}
