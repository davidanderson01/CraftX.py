// CraftX.py Universal Service Worker
// Compatible with ALL browsers and devices
// Provides offline functionality, caching, and PWA features

const CACHE_NAME = 'craftxpy-universal-v1.0.0';
const STATIC_CACHE = 'craftxpy-static-v1.0.0';
const DYNAMIC_CACHE = 'craftxpy-dynamic-v1.0.0';

// Universal resource list for all platforms
const STATIC_ASSETS = [
    '/',
    '/static/manifest.json',
    '/static/icon-16x16.png',
    '/static/icon-32x32.png',
    '/static/icon-48x48.png',
    '/static/icon-72x72.png',
    '/static/icon-96x96.png',
    '/static/icon-128x128.png',
    '/static/icon-144x144.png',
    '/static/icon-152x152.png',
    '/static/icon-192x192.png',
    '/static/icon-384x384.png',
    '/static/icon-512x512.png',
    '/static/apple-touch-icon.png',
    '/static/favicon.ico'
];

// Platform detection for optimized caching
function getPlatform() {
    const userAgent = self.navigator.userAgent.toLowerCase();

    if (userAgent.includes('android')) return 'android';
    if (userAgent.includes('iphone') || userAgent.includes('ipad')) return 'ios';
    if (userAgent.includes('windows')) return 'windows';
    if (userAgent.includes('mac')) return 'macos';
    if (userAgent.includes('linux')) return 'linux';
    if (userAgent.includes('chrome')) return 'chromeos';

    return 'universal';
}

// Install event - universal caching strategy
self.addEventListener('install', event => {
    console.log('CraftX.py Universal SW: Installing...');

    event.waitUntil(
        Promise.all([
            // Cache static assets
            caches.open(STATIC_CACHE).then(cache => {
                console.log('CraftX.py Universal SW: Caching static assets');
                return cache.addAll(STATIC_ASSETS);
            }),

            // Platform-specific optimizations
            caches.open(CACHE_NAME).then(cache => {
                const platform = getPlatform();
                console.log(`CraftX.py Universal SW: Optimizing for ${platform}`);

                // Add platform-specific assets if needed
                const platformAssets = [];

                switch (platform) {
                    case 'ios':
                        platformAssets.push('/static/apple-touch-icon-180x180.png');
                        break;
                    case 'android':
                        platformAssets.push('/static/adaptive-icon.png');
                        break;
                    case 'windows':
                        platformAssets.push('/static/browserconfig.xml');
                        break;
                }

                if (platformAssets.length > 0) {
                    return cache.addAll(platformAssets);
                }
            })
        ]).then(() => {
            console.log('CraftX.py Universal SW: Installation complete');
            return self.skipWaiting();
        })
    );
});

// Activate event - cleanup old caches
self.addEventListener('activate', event => {
    console.log('CraftX.py Universal SW: Activating...');

    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME &&
                        cacheName !== STATIC_CACHE &&
                        cacheName !== DYNAMIC_CACHE) {
                        console.log('CraftX.py Universal SW: Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            console.log('CraftX.py Universal SW: Activation complete');
            return self.clients.claim();
        })
    );
});

// Fetch event - universal caching strategy
self.addEventListener('fetch', event => {
    const request = event.request;
    const url = new URL(request.url);

    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }

    // Skip chrome-extension and other special protocols
    if (!url.protocol.startsWith('http')) {
        return;
    }

    event.respondWith(
        handleFetch(request)
    );
});

async function handleFetch(request) {
    const url = new URL(request.url);

    try {
        // Strategy 1: Static assets (Cache First)
        if (STATIC_ASSETS.some(asset => url.pathname.endsWith(asset))) {
            return await cacheFirst(request, STATIC_CACHE);
        }

        // Strategy 2: API calls (Network First)
        if (url.pathname.includes('/api/') || url.pathname.includes('/_stcore/')) {
            return await networkFirst(request, DYNAMIC_CACHE);
        }

        // Strategy 3: HTML pages (Stale While Revalidate)
        if (request.headers.get('accept')?.includes('text/html')) {
            return await staleWhileRevalidate(request, DYNAMIC_CACHE);
        }

        // Strategy 4: Images and assets (Cache First with fallback)
        if (request.headers.get('accept')?.includes('image/') ||
            url.pathname.includes('/static/')) {
            return await cacheFirst(request, DYNAMIC_CACHE);
        }

        // Default: Network First
        return await networkFirst(request, DYNAMIC_CACHE);

    } catch (error) {
        console.log('CraftX.py Universal SW: Fetch error:', error);

        // Offline fallback
        if (request.headers.get('accept')?.includes('text/html')) {
            return await getOfflinePage();
        }

        // Return cached version if available
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }

        // Ultimate fallback
        return new Response(
            JSON.stringify({
                error: 'Network unavailable',
                message: 'CraftX.py is working offline'
            }),
            {
                status: 503,
                statusText: 'Service Unavailable',
                headers: { 'Content-Type': 'application/json' }
            }
        );
    }
}

// Cache First Strategy
async function cacheFirst(request, cacheName) {
    const cache = await caches.open(cacheName);
    const cachedResponse = await cache.match(request);

    if (cachedResponse) {
        return cachedResponse;
    }

    const networkResponse = await fetch(request);

    if (networkResponse.ok) {
        cache.put(request, networkResponse.clone());
    }

    return networkResponse;
}

// Network First Strategy
async function networkFirst(request, cacheName) {
    const cache = await caches.open(cacheName);

    try {
        const networkResponse = await fetch(request);

        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }

        return networkResponse;
    } catch (error) {
        const cachedResponse = await cache.match(request);

        if (cachedResponse) {
            return cachedResponse;
        }

        throw error;
    }
}

// Stale While Revalidate Strategy
async function staleWhileRevalidate(request, cacheName) {
    const cache = await caches.open(cacheName);
    const cachedResponse = await cache.match(request);

    const fetchPromise = fetch(request).then(networkResponse => {
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    });

    return cachedResponse || fetchPromise;
}

// Offline page fallback
async function getOfflinePage() {
    const offlineHTML = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CraftX.py - Offline</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                text-align: center;
                padding: 2rem;
                margin: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
            .container {
                max-width: 400px;
                background: rgba(255,255,255,0.1);
                padding: 2rem;
                border-radius: 1rem;
                backdrop-filter: blur(10px);
            }
            .icon { font-size: 4rem; margin-bottom: 1rem; }
            h1 { margin: 0 0 1rem 0; }
            p { margin: 0 0 1rem 0; opacity: 0.9; }
            .retry-btn {
                background: white;
                color: #667eea;
                border: none;
                padding: 1rem 2rem;
                border-radius: 0.5rem;
                font-weight: bold;
                cursor: pointer;
                margin-top: 1rem;
            }
            .retry-btn:hover {
                background: #f0f0f0;
            }
            .features {
                text-align: left;
                margin-top: 2rem;
                opacity: 0.8;
            }
            .features li {
                margin: 0.5rem 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="icon">🧠</div>
            <h1>CraftX.py Offline</h1>
            <p>You're currently offline, but CraftX.py is still working!</p>
            
            <div class="features">
                <h3>Available Offline:</h3>
                <ul>
                    <li>✅ Cached conversations</li>
                    <li>✅ Code examples</li>
                    <li>✅ Documentation</li>
                    <li>✅ Basic functionality</li>
                </ul>
            </div>
            
            <button class="retry-btn" onclick="window.location.reload()">
                🔄 Try Again
            </button>
            
            <p style="margin-top: 2rem; font-size: 0.9rem;">
                Universal compatibility: Works on all devices and platforms
            </p>
        </div>
        
        <script>
            // Auto-retry when connection is restored
            window.addEventListener('online', () => {
                window.location.reload();
            });
            
            // Show connection status
            function updateStatus() {
                if (navigator.onLine) {
                    document.querySelector('.retry-btn').textContent = '🔄 Reconnecting...';
                    setTimeout(() => window.location.reload(), 1000);
                }
            }
            
            setInterval(updateStatus, 5000);
        </script>
    </body>
    </html>
  `;

    return new Response(offlineHTML, {
        status: 200,
        headers: { 'Content-Type': 'text/html' }
    });
}

// Background sync for offline functionality
self.addEventListener('sync', event => {
    console.log('CraftX.py Universal SW: Background sync triggered');

    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

async function doBackgroundSync() {
    try {
        // Sync any pending data when back online
        console.log('CraftX.py Universal SW: Syncing data...');

        // Here you could sync chat messages, settings, etc.
        const clients = await self.clients.matchAll();
        clients.forEach(client => {
            client.postMessage({
                type: 'BACKGROUND_SYNC',
                data: { status: 'synced' }
            });
        });

    } catch (error) {
        console.log('CraftX.py Universal SW: Background sync failed:', error);
    }
}

// Push notifications for all platforms
self.addEventListener('push', event => {
    console.log('CraftX.py Universal SW: Push notification received');

    const options = {
        body: event.data ? event.data.text() : 'CraftX.py notification',
        icon: '/static/icon-192x192.png',
        badge: '/static/icon-72x72.png',
        image: '/static/icon-384x384.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: Math.random().toString(36).substr(2, 9)
        },
        actions: [
            {
                action: 'open',
                title: 'Open CraftX.py',
                icon: '/static/icon-96x96.png'
            },
            {
                action: 'close',
                title: 'Dismiss',
                icon: '/static/icon-96x96.png'
            }
        ],
        requireInteraction: false,
        silent: false
    };

    event.waitUntil(
        self.registration.showNotification('CraftX.py Assistant', options)
    );
});

// Notification click handling
self.addEventListener('notificationclick', event => {
    console.log('CraftX.py Universal SW: Notification clicked');

    event.notification.close();

    if (event.action === 'open') {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

// Message handling from main thread
self.addEventListener('message', event => {
    console.log('CraftX.py Universal SW: Message received:', event.data);

    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }

    if (event.data && event.data.type === 'CACHE_URLS') {
        event.waitUntil(
            caches.open(DYNAMIC_CACHE).then(cache => {
                return cache.addAll(event.data.urls);
            })
        );
    }
});

// Periodic background sync (if supported)
self.addEventListener('periodicsync', event => {
    if (event.tag === 'content-sync') {
        event.waitUntil(doPeriodicSync());
    }
});

async function doPeriodicSync() {
    try {
        console.log('CraftX.py Universal SW: Periodic sync');
        // Sync content periodically
    } catch (error) {
        console.log('CraftX.py Universal SW: Periodic sync failed:', error);
    }
}

// Clean up old caches periodically
async function cleanupCaches() {
    const cacheNames = await caches.keys();
    const oldCaches = cacheNames.filter(name =>
        name.startsWith('craftxpy-') &&
        name !== CACHE_NAME &&
        name !== STATIC_CACHE &&
        name !== DYNAMIC_CACHE
    );

    return Promise.all(
        oldCaches.map(cacheName => caches.delete(cacheName))
    );
}

// Initialize universal compatibility
console.log('CraftX.py Universal Service Worker loaded');
console.log('Platform support: ALL devices and browsers');
console.log('Features: Offline support, caching, notifications, background sync');
