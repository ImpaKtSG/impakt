import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "build",
    assetsDir: "assets",
    emptyOutDir: true,
  },

  server: {
    watch: {
      usePolling: process.env.NODE_ENV === "development",
    },
    port: 3000,
    host: "0.0.0.0",
  },
});
