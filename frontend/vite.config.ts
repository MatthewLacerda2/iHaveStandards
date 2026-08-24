/// <reference types="vitest/config" />
import { defineConfig } from "vite";
import react, { reactCompilerPreset } from "@vitejs/plugin-react";
import babel from "@rolldown/plugin-babel";
import tailwindcss from "@tailwindcss/vite";
import { tanstackRouter } from "@tanstack/router-plugin/vite";

export default defineConfig({
  plugins: [
    tanstackRouter({ target: "react", autoCodeSplitting: true }),
    react(),
    // plugin-react 6 dropped its own babel option: Vite 8 does React Refresh
    // natively, so the compiler is the only thing still needing Babel.
    babel({ presets: [reactCompilerPreset()] }),
    tailwindcss(),
  ],
  // Vite 8 reads the "@/*" mapping straight from tsconfig.json, so the
  // vite-tsconfig-paths plugin is no longer needed.
  resolve: { tsconfigPaths: true },
  server: {
    // Dev-only: forward API calls to the local backend so the relative
    // `/api/v1` default in lib/api/client.ts works with no extra config.
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
  test: {
    globals: true,
    environment: "jsdom",
    include: ["src/**/*.test.{ts,tsx}", "eslint-rules/**/*.test.ts"],
  },
});
