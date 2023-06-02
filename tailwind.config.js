/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/frontend/**/*.vue"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: "#C8BCF6",
        "light-gray": {
          1: "#F5F5F5",
          2: "#EFEFEF",
          3: "#C0BFBD",
        },
        "dark-shade": "#1F1F22",
        "dark-gray": "#09090A",
      },
    },
  },
};
