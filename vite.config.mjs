import { defineConfig } from 'vite';

// 앱인토스 번들용 빌드. art/, data/ 는 scripts/copy-assets.mjs 가 dist 로 복사한다.
export default defineConfig({
  base: './',
  publicDir: false,
  define: { __TOSS__: 'true' }, // index.html 이 이 값으로 앱인토스 SDK 사용 여부를 정함
  build: { outDir: 'dist', emptyOutDir: true },
});
