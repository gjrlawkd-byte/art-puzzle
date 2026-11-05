import { defineConfig } from '@apps-in-toss/web-framework/config';

export default defineConfig({
  // 앱인토스 콘솔에 등록한 앱 이름과 반드시 같아야 업로드된다
  appName: 'art-puzzle',
  brand: {
    primaryColor: '#D9A441',
  },
  webView: {},
  permissions: [],
  webBundleDir: 'dist',
});
