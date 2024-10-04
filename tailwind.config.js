/** @type {import('tailwindcss').Config} */
import colors from "tailwindcss/colors";

module.exports = {
  content: ["./templates/**/*.html", "./core/templates/**/*.html", "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {},
    container: {
      center: true,
      padding: {
        DEFAULT: "1rem",
        sm: "2rem",
        lg: "2rem",
        // xl: "5rem",
        // "2xl": "6rem",
      },
      screens: {
        sm: '600px',
        md: '728px',
        lg: '984px',
        xl: '1240px',
        '2xl': '1496px',
      },
    },
    colors: {
      primary: "#6A9C89",
      primaryHover: "#16423C",
      secondary: "#4F4557",
      tertiary: "#6D5D6E",
      light: "#FAF0E6",
      publisherPrimary: "#f5f411",
      publisherPrimaryHover: "#352F44",
      black: colors.black,
      white: colors.white,
      amber: colors.amber,
      emerald: colors.emerald,
      indigo: colors.indigo,
      yellow: colors.yellow,
      stone: colors.stone,
      sky: colors.sky,
      neutral: colors.neutral,
      gray: colors.gray,
      slate: colors.slate,
      red: colors.red,
      lime: colors.lime,
      teal: colors.teal,
      cyan: colors.cyan
    },
  },
  plugins: [require("flowbite/plugin")],
  important: true,
};
