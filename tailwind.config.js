/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/**/*.js',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'],
      },
    },
  },
  daisyui: {
    themes: [
      "light", "dark", "cupcake", "luxury", "business",
      {
        luxury: {
          ...require("daisyui/src/theming/themes")["luxury"],
          "primary-content": "#FFFFFF",
        },
      }
    ],
  },
  plugins: [require("daisyui")],
}

