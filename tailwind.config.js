/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./index.html",
      "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
      extend: {
        colors: {
          marine: {
            50: '#eff9ff',
            100: '#dff2ff',
            200: '#b8e7ff',
            300: '#78d5ff',
            400: '#2fc0ff',
            500: '#03a4f4',
            600: '#0084d1',
            700: '#0069a8',
            800: '#025889',
            900: '#084a72',
          },
          ocean: {
            50: '#f0f9ff',
            100: '#e0f2fe',
            200: '#b9e6fe',
            300: '#7cd4fd',
            400: '#36bffa',
            500: '#0ca5eb',
            600: '#0084c9',
            700: '#0168a3',
            800: '#065786',
            900: '#0b476f',
          }
        },
        animation: {
          'wave': 'wave 2s ease-in-out infinite',
          'pulse-slow': 'pulse 3s ease-in-out infinite',
          'float': 'float 3s ease-in-out infinite',
        },
        keyframes: {
          wave: {
            '0%, 100%': { transform: 'translateY(0)' },
            '50%': { transform: 'translateY(-10px)' },
          },
          float: {
            '0%, 100%': { transform: 'translateY(0)' },
            '50%': { transform: 'translateY(-20px)' },
          }
        },
        fontFamily: {
          'sans': ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        },
        boxShadow: {
          'soft': '0 2px 15px 0 rgba(0, 0, 0, 0.08)',
          'hard': '0 10px 40px 0 rgba(0, 0, 0, 0.15)',
        }
      },
    },
    plugins: [],
  }