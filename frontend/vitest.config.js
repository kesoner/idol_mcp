import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/setupTests.js'],
    exclude: [
      '**/node_modules/**',
      '**/dist/**',
      '**/cypress/**',
      '**/.{idea,git,cache,output,temp}/**',
      '**/Live2DModel.test.jsx'
    ],
    alias: {
      '@testing-library/jest-dom': '@testing-library/jest-dom/vitest'
    },
    deps: {
      inline: [/@testing-library\/jest-dom/]
    }
  },
}); 