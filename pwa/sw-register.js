let deferredPrompt;

// 1. Capture the "Install" prompt event (Android/Chrome)
// We are disabling the automatic popup bubble as per user request.
// The browser will still show the install icon in the address bar for desktop.
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  // Automatic popup removed.
});

// 2. Cleanup when app is installed
window.addEventListener('appinstalled', (evt) => {
  const btn = document.getElementById('pwa-install-btn');
  if (btn) btn.remove();
});

// 3. Service Worker Registration and Update Detection
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    const swPath = (window.rootPath || '') + 'sw.js';
    let refreshing = false;

    // Detect when the new service worker has taken control
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      if (!refreshing) {
        refreshing = true;
        window.location.reload();
      }
    });

    navigator.serviceWorker.register(swPath).then(registration => {
      console.log('SW registered: ', registration);

      // Function to handle the update
      const onUpdateFound = () => {
        const installingWorker = registration.installing;
        if (installingWorker) {
          installingWorker.addEventListener('statechange', () => {
            if (installingWorker.state === 'installed' && navigator.serviceWorker.controller) {
              showUpdateAvailable(registration.waiting);
            }
          });
        }
      };

      // Check if there is already a waiting service worker
      if (registration.waiting) {
        showUpdateAvailable(registration.waiting);
      }

      // Listen for future updates
      registration.addEventListener('updatefound', onUpdateFound);
    }).catch(registrationError => {
      console.log('SW registration failed: ', registrationError);
    });
  });
}

function showUpdateAvailable(waitingWorker) {
  if (document.getElementById('pwa-update-btn')) return;

  const btn = document.createElement('button');
  btn.id = 'pwa-update-btn';
  btn.innerHTML = '✨ New Content Available! <u>Update Now</u>';
  
  Object.assign(btn.style, {
    position: 'fixed',
    top: '20px',
    left: '50%',
    transform: 'translateX(-50%)',
    padding: '12px 24px',
    backgroundColor: '#f0d78c',
    color: '#2e2e2e',
    border: 'none',
    borderRadius: '50px',
    cursor: 'pointer',
    zIndex: '10001',
    boxShadow: '0 8px 16px rgba(0,0,0,0.4)',
    fontSize: '14px',
    fontWeight: 'bold',
    transition: 'all 0.3s ease',
    animation: 'pwa-slide-down 0.5s ease-out'
  });

  // Add simple animation
  const styleSheet = document.createElement("style");
  styleSheet.innerText = `
    @keyframes pwa-slide-down {
      from { top: -100px; opacity: 0; }
      to { top: 20px; opacity: 1; }
    }
  `;
  document.head.appendChild(styleSheet);

  btn.addEventListener('click', () => {
    if (waitingWorker) {
      waitingWorker.postMessage({ type: 'SKIP_WAITING' });
    }
    btn.remove();
  });

  document.body.appendChild(btn);
}
