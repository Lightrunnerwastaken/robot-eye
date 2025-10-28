import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#6d28d9",
          light: "#a855f7"
        },
        accent: "#22d3ee"
      }
    }
  },
  plugins: []
};

export default config;
