let deferredPrompt;

// 1. Helper: Check if already installed/standalone
const isStandalone = () => {
  return (window.matchMedia('(display-mode: standalone)').matches) || (window.navigator.standalone);
};

// 2. Helper: Detect iOS
const isIOS = () => {
  return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
};

// 3. Capture the "Install" prompt event (Android/Chrome)
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  
  const lastDismissed = localStorage.getItem('pwa_install_dismissed');
  const now = Date.now();
  if (!lastDismissed || now - parseInt(lastDismissed) > 86400000) {
    showInstallButton('✨ Install deepDive App', () => {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((choiceResult) => {
          if (choiceResult.outcome === 'accepted') {
            console.log('User accepted the install prompt');
          }
          const btn = document.getElementById('pwa-install-btn');
          if (btn) btn.remove();
          deferredPrompt = null;
        });
      }
    });
  }
});

// 4. Handle iOS Hint (Safari)
window.addEventListener('load', () => {
  if (isIOS() && !isStandalone()) {
    const lastDismissed = localStorage.getItem('pwa_ios_dismissed');
    const now = Date.now();
    if (!lastDismissed || now - parseInt(lastDismissed) > 86400000) {
      showInstallButton('✨ Add to iPhone/iPad', () => {
        alert("To install the deepDive app on your iPhone/iPad:\n\n1. Tap the 'Share' icon (square with arrow) at the bottom of Safari.\n2. Scroll down and tap 'Add to Home Screen'.");
        const btn = document.getElementById('pwa-install-btn');
        if (btn) {
            btn.remove();
            localStorage.setItem('pwa_ios_dismissed', Date.now().toString());
        }
      });
    }
  }
});

function showInstallButton(text, onClickAction) {
  if (document.getElementById('pwa-install-btn')) return;

  const btn = document.createElement('button');
  btn.id = 'pwa-install-btn';
  btn.innerHTML = text;
  
  Object.assign(btn.style, {
    position: 'fixed',
    bottom: '20px',
    left: '50%',
    transform: 'translateX(-50%)',
    padding: '12px 24px',
    backgroundColor: '#2e2e2e',
    color: '#f0d78c',
    border: '2px solid #f0d78c',
    borderRadius: '50px',
    cursor: 'pointer',
    zIndex: '10000',
    boxShadow: '0 8px 16px rgba(0,0,0,0.4)',
    fontSize: '14px',
    fontWeight: 'bold',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    transition: 'all 0.3s ease'
  });

  const close = document.createElement('span');
  close.innerHTML = '&times;';
  close.style.fontSize = '20px';
  close.style.marginLeft = '8px';
  close.style.opacity = '0.7';
  close.onclick = (e) => {
    e.stopPropagation();
    btn.style.opacity = '0';
    setTimeout(() => btn.remove(), 300);
    const storageKey = isIOS() ? 'pwa_ios_dismissed' : 'pwa_install_dismissed';
    localStorage.setItem(storageKey, Date.now().toString());
  };
  btn.appendChild(close);

  btn.addEventListener('click', onClickAction);
  document.body.appendChild(btn);
}

// 5. Cleanup when app is installed
window.addEventListener('appinstalled', (evt) => {
  const btn = document.getElementById('pwa-install-btn');
  if (btn) btn.remove();
});

// 6. Service Worker Registration and Update Detection
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
