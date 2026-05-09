importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.4.1/workbox-sw.js');

if (workbox) {
  const { precacheAndRoute } = workbox.precaching;
  const { registerRoute, NavigationRoute } = workbox.routing;
  const { createHandlerBoundToURL } = workbox.precaching;
  const { CacheFirst } = workbox.strategies;
  const { CacheableResponsePlugin } = workbox.cacheableResponse;
  const { RangeRequestsPlugin } = workbox.rangeRequests;
  const { ExpirationPlugin } = workbox.expiration;

  // Workbox will inject the manifest here
  precacheAndRoute(self.__WB_MANIFEST || []);

  // Runtime caching for videos (Cache-First)
  registerRoute(
    ({ request }) => request.destination === 'video',
    new CacheFirst({
      cacheName: 'deep-dive-videos',
      plugins: [
        new CacheableResponsePlugin({ statuses: [200] }),
        new RangeRequestsPlugin(),
        new ExpirationPlugin({
          maxEntries: 10,
          maxAgeSeconds: 30 * 24 * 60 * 60, // 30 Days
        }),
      ],
    })
  );

  // Navigation fallback to index.html for offline support
  const handler = createHandlerBoundToURL('./index.html');
  const navigationRoute = new NavigationRoute(handler);
  registerRoute(navigationRoute);

  self.addEventListener('install', (event) => {
    self.skipWaiting();
  });

  self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
      self.skipWaiting();
    }
  });
}
