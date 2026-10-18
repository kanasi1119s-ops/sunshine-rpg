import { defineConfig } from "vite";

export default defineConfig({
  base: "./",
  test: {
    environment: "node",
    include: ["src/**/*.test.ts"],
    // 重い音楽テスト（曲の書き出し）が遅い環境でも時間切れにならないよう余裕を持たせる
    testTimeout: 30000,
  },
});
