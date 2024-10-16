/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './bank/templates/**/*.html',
    './bank/static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#001F3F',  // Navy
        secondary: '#F9D342', // Matte Yellow
        'primary-content': '#FFFFFF', // White
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'],
        serif: ['Merriweather', 'serif'],
      },
    },
  },
  daisyui: {
    themes: [
      {
        ideabank: {
          "primary": "#001F3F",
          "secondary": "#F9D342",
          "accent": "#37cdbe",
          "neutral": "#3d4451",
          "base-100": "#ffffff",
          "primary-content": "#ffffff",
          "secondary-content": "#001F3F",
        },
        lofi: {
          ...require("daisyui/src/theming/themes")["lofi"],
          "error": "red",
        }
      },
      "wire"
    ],
  },
  plugins: [require("daisyui")],
}
