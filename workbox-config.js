module.exports = {
  globDirectory: "book",
  globPatterns: ["**/*.{html,js,css,png}"],
  swSrc: "pwa/sw-src.js",
  swDest: "book/sw.js",
  globIgnores: ["sw.js"],
  maximumFileSizeToCacheInBytes: 10 * 1024 * 1024
};
