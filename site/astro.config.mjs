// @ts-check
import { defineConfig } from "astro/config";
import vercel from "@astrojs/vercel";
import tailwindcss from "@tailwindcss/vite";
import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
  site: "https://loveoverexile.com",
  adapter: vercel(),
  vite: {
    plugins: [tailwindcss()],
  },
  integrations: [sitemap()],
});
