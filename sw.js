self.addEventListener('install', event => {
  console.log('Service worker installed');
  self.skipWaiting();
});

self.addEventListener('fetch', () => {
  // You can cache assets here later
});
