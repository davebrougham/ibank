/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/**/*.js',
  ],
  theme: {
    extend: {},
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

