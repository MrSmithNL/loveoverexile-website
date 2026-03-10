import eslint from "@eslint/js";
import tseslint from "@typescript-eslint/eslint-plugin";
import tsparser from "@typescript-eslint/parser";
import eslintPluginAstro from "eslint-plugin-astro";

export default [
  // Global ignores
  {
    ignores: ["dist/", ".astro/", "node_modules/", ".vercel/"],
  },

  // Base ESLint recommended rules
  eslint.configs.recommended,

  // TypeScript files (.ts / .tsx)
  {
    files: ["**/*.ts", "**/*.tsx"],
    languageOptions: {
      parser: tsparser,
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
      },
      globals: {
        Response: "readonly",
        Request: "readonly",
        fetch: "readonly",
        URL: "readonly",
        console: "readonly",
        JSON: "readonly",
        Headers: "readonly",
        FormData: "readonly",
        URLSearchParams: "readonly",
      },
    },
    plugins: {
      "@typescript-eslint": tseslint,
    },
    rules: {
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
      ],
      "@typescript-eslint/consistent-type-imports": "error",
      "@typescript-eslint/no-non-null-assertion": "error",

      "no-unused-vars": "off",

      "no-console": "warn",
      eqeqeq: ["error", "always"],
      "no-var": "error",
      "prefer-const": "error",
    },
  },

  // Astro files — plugin recommended config
  ...eslintPluginAstro.configs.recommended,

  // Astro overrides — globals for inline scripts and relaxed rules
  {
    files: ["**/*.astro"],
    languageOptions: {
      globals: {
        dataLayer: "readonly",
        window: "readonly",
        document: "readonly",
        console: "readonly",
      },
    },
    rules: {
      "no-console": "warn",
    },
  },
];
