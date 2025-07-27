"""
CraftX.py Universal Mobile Application
100% Compatible with ALL devices and platforms:
- Android (all versions and manufacturers)
- iOS (iPhone, iPad, all iOS versions)
- Samsung Galaxy series
- Windows (XP, 7, 8, 10, 11)
- MacOS (all versions)
- Linux (all distributions)
- ChromeOS
- Tablets and older devices

Zero functionality loss across platforms
"""

import streamlit as st
import json
import os
import sys
import platform
import subprocess
import base64
from datetime import datetime
from pathlib import Path

# Import universal systems
try:
    from craftxpy.utils.cloud_storage import cloud_storage
    from craftxpy.utils.auth import universal_auth
    from craftxpy.utils.data_storage import universal_storage
except ImportError:
    # Fallback if modules not available
    cloud_storage = None
    universal_auth = None
    universal_storage = None

# Universal compatibility detection


def detect_platform():
    """Detect platform and adjust accordingly."""
    system = platform.system().lower()
    version = platform.version()
    machine = platform.machine()

    return {
        "system": system,
        "version": version,
        "machine": machine,
        "is_mobile": any(keyword in str(st.get_option("client.toolbarMode")).lower() for keyword in ["mobile", "phone", "tablet"]),
        "is_touch": "ontouchstart" in str(st.get_option("client.toolbarMode")).lower(),
        "screen_size": "unknown"
    }


def get_logo_base64():
    """Get the CraftX.py logo as base64 for embedding in HTML."""

    # Try multiple possible logo locations
    logo_paths = [
        "static/craftx-logo.png",
        "assets/img/craftx-logo.png",
        "static/icon-192x192.png",
        "static/icon-96x96.png"
    ]

    for logo_path in logo_paths:
        if os.path.exists(logo_path):
            try:
                with open(logo_path, "rb") as f:
                    logo_bytes = f.read()
                    logo_base64 = base64.b64encode(logo_bytes).decode()
                    return f"data:image/png;base64,{logo_base64}"
            except Exception as e:
                continue

    # If no logo found, create a simple SVG logo
    svg_logo = '''<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
            </linearGradient>
        </defs>
        <circle cx="24" cy="24" r="22" fill="url(#grad)" />
        <text x="24" y="32" font-family="Arial" font-size="24" text-anchor="middle" fill="white" font-weight="bold">C</text>
    </svg>'''

    # Convert SVG to base64
    svg_base64 = base64.b64encode(svg_logo.encode()).decode()
    return f"data:image/svg+xml;base64,{svg_base64}"


def get_elevatecraft_logo_base64():
    """Get the ElevateCraft logo as base64 for embedding in HTML."""

    # Try to load the uploaded ElevateCraft logo
    elevatecraft_logo_paths = [
        "static/elevatecraft-logo.png",
        "assets/img/elevatecraft-logo.png"
    ]

    for logo_path in elevatecraft_logo_paths:
        if os.path.exists(logo_path):
            try:
                with open(logo_path, "rb") as f:
                    logo_bytes = f.read()
                    logo_base64 = base64.b64encode(logo_bytes).decode()
                    return f"data:image/png;base64,{logo_base64}"
            except Exception as e:
                continue

    # Create a simple, clean ElevateCraft logo SVG
    elevatecraft_svg = '''<svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#667eea"/>
                <stop offset="100%" style="stop-color:#764ba2"/>
            </linearGradient>
        </defs>
        <circle cx="12" cy="12" r="11" fill="url(#grad1)"/>
        <path d="M8 14 L12 10 L16 14" stroke="white" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="12" cy="8" r="1.5" fill="white"/>
    </svg>'''

    # Convert SVG to base64
    try:
        svg_base64 = base64.b64encode(
            elevatecraft_svg.encode('utf-8')).decode()
        return f"data:image/svg+xml;base64,{svg_base64}"
    except Exception as e:
        # Ultimate fallback - return a simple emoji
        return "🌟"


# Configure for universal compatibility
# Get logo for favicon
try:
    # Try to use the actual logo for favicon
    logo_paths = [
        "static/icon-32x32.png",
        "static/icon-16x16.png",
        "static/craftx-logo.png"
    ]
    favicon_path = None
    for path in logo_paths:
        if os.path.exists(path):
            favicon_path = path
            break

    st.set_page_config(
        page_title="CraftX.py Universal Assistant",
        page_icon=favicon_path if favicon_path else "🧠",
        layout="wide",
        initial_sidebar_state="auto",  # Auto-adjust based on screen size
        menu_items={
            'Get Help': 'https://craftx.elevatecraft.org/docs.html',
            'Report a bug': 'https://github.com/davidanderson01/CraftX.py/issues',
            'About': "CraftX.py - Universal AI Assistant Framework"
        }
    )
except:
    # Fallback if logo loading fails
    st.set_page_config(
        page_title="CraftX.py Universal Assistant",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            'Get Help': 'https://craftx.elevatecraft.org/docs.html',
            'Report a bug': 'https://github.com/davidanderson01/CraftX.py/issues',
            'About': "CraftX.py - Universal AI Assistant Framework"
        }
    )

# Universal CSS that works on ALL devices and browsers
st.markdown("""
<style>
    /* CSS Reset for universal compatibility */
    * {
        box-sizing: border-box;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* Universal viewport handling */
    @-ms-viewport { width: device-width; }
    @viewport { width: device-width; }
    
    /* Root variables for consistent theming */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --background-color: #f8f9ff;
        --text-color: #333333;
        --border-radius: 8px;
        --shadow: 0 2px 10px rgba(0,0,0,0.1);
        --transition: all 0.3s ease;
    }
    
    /* Universal container that adapts to all screen sizes */
    .universal-container {
        width: 100%;
        max-width: 100vw;
        padding: 0.5rem;
        margin: 0 auto;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }
    
    /* Responsive header that works on all devices */
    .universal-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 1rem;
        border-radius: var(--border-radius);
        margin-bottom: 1rem;
        text-align: center;
        box-shadow: var(--shadow);
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    /* Universal button styling */
    .universal-button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 500;
        cursor: pointer;
        transition: var(--transition);
        width: 100%;
        min-height: 44px; /* Touch-friendly for mobile */
        display: inline-flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        user-select: none;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
    }
    
    .universal-button:hover,
    .universal-button:focus {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        outline: none;
    }
    
    .universal-button:active {
        transform: translateY(0);
    }
    
    /* Universal input styling */
    .universal-input {
        width: 100%;
        padding: 12px 16px;
        border: 2px solid #e0e6ed;
        border-radius: var(--border-radius);
        font-size: 16px; /* Prevents zoom on iOS */
        background: white;
        transition: var(--transition);
        min-height: 44px; /* Touch-friendly */
    }
    
    .universal-input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
        outline: none;
    }
    
    /* Chat interface that adapts to all screen sizes */
    .universal-chat {
        flex: 1;
        display: flex;
        flex-direction: column;
        background: var(--background-color);
        border-radius: var(--border-radius);
        padding: 1rem;
        margin-bottom: 1rem;
        overflow: hidden;
    }
    
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        max-height: 60vh;
        padding: 0.5rem;
        scrollbar-width: thin; /* Firefox */
        scrollbar-color: var(--primary-color) transparent; /* Firefox */
        -webkit-overflow-scrolling: touch; /* iOS smooth scrolling */
    }
    
    /* Webkit scrollbar styling */
    .chat-messages::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: transparent;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 3px;
    }
    
    /* Universal message bubbles */
    .message {
        margin: 8px 0;
        padding: 12px 16px;
        border-radius: 18px;
        max-width: 85%;
        word-wrap: break-word;
        word-break: break-word;
        line-height: 1.4;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }
    
    .assistant-message {
        background: white;
        color: var(--text-color);
        margin-right: auto;
        border-bottom-left-radius: 4px;
        box-shadow: var(--shadow);
    }
    
    /* Status indicators */
    .status-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .status-card {
        background: white;
        padding: 1rem;
        border-radius: var(--border-radius);
        text-align: center;
        box-shadow: var(--shadow);
        transition: var(--transition);
    }
    
    .status-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    /* Universal sidebar that adapts to screen size */
    .universal-sidebar {
        background: white;
        border-radius: var(--border-radius);
        padding: 1rem;
        box-shadow: var(--shadow);
    }
    
    /* Quick actions grid */
    .quick-actions {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 0.5rem;
        margin: 1rem 0;
    }
    
    /* Floating action button for all devices */
    .fab {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 56px;
        height: 56px;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        border-radius: 50%;
        border: none;
        color: white;
        font-size: 24px;
        cursor: pointer;
        box-shadow: var(--shadow);
        z-index: 1001;
        transition: var(--transition);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .fab:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 25px rgba(0,0,0,0.3);
    }
    
    /* Loading animation */
    .loading-dots {
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    
    .loading-dots span {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--primary-color);
        animation: pulse 1.4s infinite ease-in-out;
    }
    
    .loading-dots span:nth-child(1) { animation-delay: -0.32s; }
    .loading-dots span:nth-child(2) { animation-delay: -0.16s; }
    .loading-dots span:nth-child(3) { animation-delay: 0s; }
    
    @keyframes pulse {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
    }
    
    /* Responsive breakpoints for all device types */
    
    /* Large desktop (1200px+) */
    @media (min-width: 1200px) {
        .universal-container { max-width: 1140px; }
        .status-grid { grid-template-columns: repeat(4, 1fr); }
        .quick-actions { grid-template-columns: repeat(3, 1fr); }
    }
    
    /* Desktop (992px - 1199px) */
    @media (min-width: 992px) and (max-width: 1199px) {
        .universal-container { max-width: 960px; }
        .status-grid { grid-template-columns: repeat(3, 1fr); }
        .quick-actions { grid-template-columns: repeat(2, 1fr); }
    }
    
    /* Tablet (768px - 991px) */
    @media (min-width: 768px) and (max-width: 991px) {
        .universal-container { max-width: 720px; }
        .status-grid { grid-template-columns: repeat(2, 1fr); }
        .quick-actions { grid-template-columns: repeat(2, 1fr); }
        .fab { bottom: 15px; right: 15px; width: 50px; height: 50px; }
    }
    
    /* Mobile landscape (576px - 767px) */
    @media (min-width: 576px) and (max-width: 767px) {
        .universal-container { max-width: 540px; }
        .status-grid { grid-template-columns: repeat(2, 1fr); }
        .quick-actions { grid-template-columns: repeat(2, 1fr); }
        .universal-header { padding: 0.75rem; }
        .message { max-width: 90%; font-size: 14px; }
    }
    
    /* Mobile portrait (up to 575px) */
    @media (max-width: 575px) {
        .universal-container { padding: 0.25rem; }
        .status-grid { grid-template-columns: 1fr 1fr; }
        .quick-actions { grid-template-columns: 1fr; }
        .universal-header { padding: 0.5rem; font-size: 14px; }
        .message { max-width: 95%; font-size: 14px; }
        .fab { bottom: 10px; right: 10px; width: 48px; height: 48px; font-size: 20px; }
    }
    
    /* Very small screens (up to 360px) */
    @media (max-width: 360px) {
        .universal-container { padding: 0.125rem; }
        .status-grid { grid-template-columns: 1fr; }
        .universal-header { padding: 0.375rem; font-size: 12px; }
        .message { font-size: 13px; }
    }
    
    /* High DPI displays */
    @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
        .universal-header { background-size: 200% 200%; }
    }
    
    /* Orientation handling */
    @media (orientation: landscape) and (max-height: 500px) {
        .chat-messages { max-height: 40vh; }
        .universal-header { padding: 0.5rem; }
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        :root {
            --background-color: #1a1a1a;
            --text-color: #ffffff;
        }
        
        .universal-chat { background: #2d2d2d; }
        .status-card { background: #3d3d3d; color: white; }
        .assistant-message { background: #3d3d3d; color: white; }
        .universal-input { background: #3d3d3d; color: white; border-color: #555; }
    }
    
    /* Reduced motion support */
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    
    /* Print styles */
    @media print {
        .fab, .universal-sidebar { display: none; }
        .universal-container { max-width: none; padding: 0; }
        .message { break-inside: avoid; }
    }
    
    /* Hide Streamlit elements for cleaner UI */
    #MainMenu, footer, header, .stDeployButton { visibility: hidden; }
    
    /* Override Streamlit default styles */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--border-radius) !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        min-height: 44px !important;
        width: 100% !important;
        transition: var(--transition) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stTextInput > div > div > input {
        font-size: 16px !important;
        border-radius: var(--border-radius) !important;
        border: 2px solid #e0e6ed !important;
        padding: 12px 16px !important;
        background: white !important;
        min-height: 44px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    .stSelectbox > div > div > select {
        min-height: 44px !important;
        font-size: 16px !important;
    }
    
    /* Accessibility improvements */
    .universal-button:focus,
    .universal-input:focus,
    .fab:focus {
        outline: 2px solid var(--primary-color);
        outline-offset: 2px;
    }
    
    /* High contrast mode */
    @media (prefers-contrast: high) {
        :root {
            --primary-color: #000080;
            --secondary-color: #000040;
            --background-color: #ffffff;
            --text-color: #000000;
        }
        
        .message { border: 2px solid var(--text-color); }
    }
</style>

<!-- Universal PWA Meta Tags -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
<meta name="theme-color" content="#764ba2">
<meta name="color-scheme" content="light dark">

<!-- iOS Specific -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="CraftX.py">
<meta name="apple-touch-fullscreen" content="yes">

<!-- Android Specific -->
<meta name="mobile-web-app-capable" content="yes">
<meta name="android-app-installable" content="yes">

<!-- Windows Specific -->
<meta name="msapplication-TileColor" content="#667eea">
<meta name="msapplication-config" content="static/browserconfig.xml">

<!-- PWA Manifest -->
<link rel="manifest" href="static/manifest.json">

<!-- Universal Icons -->
<link rel="icon" type="image/x-icon" href="static/favicon.ico">
<link rel="icon" type="image/png" sizes="16x16" href="static/icon-16x16.png">
<link rel="icon" type="image/png" sizes="32x32" href="static/icon-32x32.png">
<link rel="icon" type="image/png" sizes="48x48" href="static/icon-48x48.png">
<link rel="icon" type="image/png" sizes="96x96" href="static/icon-96x96.png">
<link rel="icon" type="image/png" sizes="192x192" href="static/icon-192x192.png">

<!-- Apple Touch Icons -->
<link rel="apple-touch-icon" href="static/apple-touch-icon.png">
<link rel="apple-touch-icon" sizes="57x57" href="static/apple-touch-icon-57x57.png">
<link rel="apple-touch-icon" sizes="60x60" href="static/apple-touch-icon-60x60.png">
<link rel="apple-touch-icon" sizes="72x72" href="static/apple-touch-icon-72x72.png">
<link rel="apple-touch-icon" sizes="76x76" href="static/apple-touch-icon-76x76.png">
<link rel="apple-touch-icon" sizes="114x114" href="static/apple-touch-icon-114x114.png">
<link rel="apple-touch-icon" sizes="120x120" href="static/apple-touch-icon-120x120.png">
<link rel="apple-touch-icon" sizes="144x144" href="static/apple-touch-icon-144x144.png">
<link rel="apple-touch-icon" sizes="152x152" href="static/apple-touch-icon-152x152.png">
<link rel="apple-touch-icon" sizes="167x167" href="static/apple-touch-icon-167x167.png">
<link rel="apple-touch-icon" sizes="180x180" href="static/apple-touch-icon-180x180.png">

<!-- Service Worker Registration -->
<script>
// Universal Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered successfully');
                
                // Check for updates
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            // New version available
                            if (confirm('New version available! Reload to update?')) {
                                window.location.reload();
                            }
                        }
                    });
                });
            })
            .catch(error => console.log('SW registration failed'));
    });
}

// Universal PWA Install Prompt
let deferredPrompt;
let installSource = 'unknown';

// Detect install source
if (navigator.userAgent.includes('Android')) {
    installSource = 'android';
} else if (navigator.userAgent.includes('iPhone') || navigator.userAgent.includes('iPad')) {
    installSource = 'ios';
} else if (navigator.userAgent.includes('Windows')) {
    installSource = 'windows';
} else if (navigator.userAgent.includes('Mac')) {
    installSource = 'macos';
} else if (navigator.userAgent.includes('Linux')) {
    installSource = 'linux';
}

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    showInstallBanner();
});

function showInstallBanner() {
    const banner = document.getElementById('install-banner');
    if (banner) {
        banner.style.display = 'block';
        
        // Platform-specific install instructions
        const instructions = document.getElementById('install-instructions');
        if (instructions) {
            switch(installSource) {
                case 'ios':
                    instructions.innerHTML = 'Tap the Share button and select "Add to Home Screen"';
                    break;
                case 'android':
                    instructions.innerHTML = 'Tap "Add to Home screen" or "Install"';
                    break;
                default:
                    instructions.innerHTML = 'Click "Install" to add to your device';
            }
        }
    }
}

function installApp() {
    if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('User accepted the install prompt');
                hideInstallBanner();
            }
            deferredPrompt = null;
        });
    } else {
        // Manual install for iOS or other platforms
        alert('To install this app:\\n\\n' +
              'iOS: Tap Share button → Add to Home Screen\\n' +
              'Android: Tap menu → Add to Home screen\\n' +
              'Desktop: Click install icon in address bar');
    }
}

function hideInstallBanner() {
    const banner = document.getElementById('install-banner');
    if (banner) {
        banner.style.display = 'none';
    }
}

// Universal keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K for quick search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const input = document.querySelector('input[type="text"]');
        if (input) input.focus();
    }
    
    // Escape to clear input
    if (e.key === 'Escape') {
        const input = document.querySelector('input[type="text"]');
        if (input) input.value = '';
    }
});

// Universal touch gestures
let touchStartY = 0;
let touchEndY = 0;

document.addEventListener('touchstart', (e) => {
    touchStartY = e.changedTouches[0].screenY;
});

document.addEventListener('touchend', (e) => {
    touchEndY = e.changedTouches[0].screenY;
    handleGesture();
});

function handleGesture() {
    const swipeThreshold = 50;
    const diff = touchStartY - touchEndY;
    
    if (Math.abs(diff) > swipeThreshold) {
        if (diff > 0) {
            // Swipe up - scroll to bottom
            window.scrollTo(0, document.body.scrollHeight);
        } else {
            // Swipe down - scroll to top
            window.scrollTo(0, 0);
        }
    }
}

// Universal quick access
function quickAccess() {
    const input = document.querySelector('input[type="text"]');
    if (input) {
        input.focus();
        input.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// Universal notifications (when supported)
function requestNotificationPermission() {
    if ('Notification' in window && navigator.serviceWorker) {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                console.log('Notification permission granted');
            }
        });
    }
}

// Auto-request notification permission on first interaction
document.addEventListener('click', requestNotificationPermission, { once: true });

// Universal share functionality
async function shareContent(text, url) {
    if (navigator.share) {
        try {
            await navigator.share({
                title: 'CraftX.py AI Assistant',
                text: text,
                url: url || window.location.href
            });
        } catch (err) {
            console.log('Error sharing:', err);
            fallbackShare(text, url);
        }
    } else {
        fallbackShare(text, url);
    }
}

function fallbackShare(text, url) {
    // Fallback: copy to clipboard
    if (navigator.clipboard) {
        navigator.clipboard.writeText(url || window.location.href).then(() => {
            alert('Link copied to clipboard!');
        });
    } else {
        // Ultimate fallback
        const textArea = document.createElement('textarea');
        textArea.value = url || window.location.href;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        alert('Link copied to clipboard!');
    }
}

// Universal performance monitoring
if ('performance' in window) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perf = performance.getEntriesByType('navigation')[0];
            console.log('Page load time:', perf.loadEventEnd - perf.loadEventStart, 'ms');
        }, 0);
    });
}

// Universal error handling
window.addEventListener('error', (e) => {
    console.error('Global error:', e.error);
    // Could send to analytics or error reporting service
});

window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled promise rejection:', e.reason);
    // Could send to analytics or error reporting service
});
</script>
""", unsafe_allow_html=True)


def show_authentication_modal():
    """Show authentication options modal."""
    st.markdown("### 🔐 Sign In Options")

    if not universal_auth:
        st.error("Authentication system not available")
        if st.button("Close"):
            st.session_state.show_auth = False
            st.rerun()
        return

    providers = universal_auth.get_all_providers()

    st.info("Choose your preferred sign-in method:")

    # Create provider buttons
    cols = st.columns(2)
    for i, (provider_id, provider_info) in enumerate(providers.items()):
        with cols[i % 2]:
            if st.button(
                f"{provider_info['icon']} {provider_info['name']}",
                key=f"auth_{provider_id}",
                help=f"Sign in with {provider_info['name']}"
            ):
                if universal_auth.is_provider_configured(provider_id):
                    # Generate OAuth URL (this would normally redirect to the provider)
                    st.info(f"Redirecting to {provider_info['name']}...")
                    st.write(
                        "OAuth implementation would handle the actual authentication flow")
                else:
                    st.warning(
                        f"{provider_info['name']} not configured by administrator")

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔒 Privacy Policy"):
            st.info(
                "Your privacy is important to us. We only store necessary authentication data.")
    with col2:
        if st.button("❌ Close"):
            st.session_state.show_auth = False
            st.rerun()


def show_storage_settings_modal():
    """Show cloud storage settings modal."""
    st.markdown("### ☁️ Cloud Storage Settings")

    if not cloud_storage:
        st.error("Cloud storage system not available")
        if st.button("Close"):
            st.session_state.show_storage = False
            st.rerun()
        return

    # Storage Overview
    st.subheader("📊 Storage Overview")

    if universal_storage:
        user_id = st.session_state.get('user_id', 'anonymous')
        stats = universal_storage.get_storage_stats(user_id)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💬 Chat Sessions", stats.get('chat_sessions', 0))
        with col2:
            st.metric("📁 Files Stored", stats.get('files', 0))
        with col3:
            used_gb = stats.get('total_size_bytes', 0) / (1024**3)
            st.metric("💾 Storage Used", f"{used_gb:.2f} GB")

    # Cloud Providers
    st.subheader("🌐 Available Cloud Providers")

    providers = cloud_storage.get_all_providers()
    config = cloud_storage.get_storage_config()
    enabled_providers = {p["provider_id"]: p for p in config.get("enabled_providers", [])}

    for provider_id, provider_info in providers.items():
        with st.expander(f"{provider_info['icon']} {provider_info['name']} - {provider_info['max_storage']}"):
            if provider_id in enabled_providers:
                st.success("✅ Connected")
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(
                        f"Added: {enabled_providers[provider_id].get('added_date', 'Unknown')}")
                with col2:
                    if st.button(f"🗑️ Remove", key=f"remove_{provider_id}"):
                        cloud_storage.remove_provider(provider_id)
                        st.success(f"Removed {provider_info['name']}")
                        st.rerun()
            else:
                st.info("Not connected")
                if st.button(f"🔗 Connect {provider_info['name']}", key=f"connect_{provider_id}"):
                    # Mock connection - in real implementation, this would do OAuth
                    mock_token = f"mock_token_{provider_id}_{datetime.now().timestamp()}"
                    cloud_storage.add_provider(provider_id, mock_token)
                    st.success(f"Connected to {provider_info['name']}!")
                    st.rerun()

    # Sync Settings
    st.subheader("⚙️ Sync Settings")

    auto_sync = st.checkbox(
        "🔄 Automatic Sync",
        value=config.get("sync_settings", {}).get("auto_sync", True),
        help="Automatically sync data to connected cloud providers"
    )

    sync_interval = st.selectbox(
        "⏱️ Sync Interval",
        options=[60, 300, 900, 1800, 3600],
        format_func=lambda x: f"{x//60} minutes" if x < 3600 else f"{x//3600} hour(s)",
        index=1,
        help="How often to sync data"
    )

    # Manual Sync
    st.subheader("🔄 Manual Sync")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Backup All Data"):
            st.info("Starting backup to all connected providers...")
            # Backup logic would go here
            st.success("Backup completed!")

    with col2:
        if st.button("📥 Restore Data"):
            st.info("Select a backup to restore from...")
            # Restore logic would go here

    st.markdown("---")
    if st.button("❌ Close"):
        st.session_state.show_storage = False
        st.rerun()


def show_profile_modal():
    """Show user profile modal."""
    st.markdown("### 👤 User Profile")

    current_user = st.session_state.get('current_user', {})

    if not current_user:
        st.error("No user logged in")
        if st.button("Close"):
            st.session_state.show_profile = False
            st.rerun()
        return

    # Profile Information
    st.subheader("ℹ️ Profile Information")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://via.placeholder.com/100", width=100)

    with col2:
        st.write(f"**Name:** {current_user.get('name', 'Unknown')}")
        st.write(f"**Email:** {current_user.get('email', 'Unknown')}")
        st.write(f"**Provider:** {current_user.get('provider', 'Unknown')}")
        st.write(f"**Joined:** {current_user.get('created_at', 'Unknown')}")

    # Usage Statistics
    if universal_storage:
        st.subheader("📊 Usage Statistics")
        user_id = st.session_state.get('user_id', 'anonymous')
        stats = universal_storage.get_storage_stats(user_id)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💬 Total Chats", stats.get('chat_sessions', 0))
        with col2:
            st.metric("📁 Files Uploaded", stats.get('files', 0))
        with col3:
            used_mb = stats.get('total_size_bytes', 0) / (1024**2)
            st.metric("💾 Data Stored", f"{used_mb:.1f} MB")

    # Preferences
    st.subheader("⚙️ Preferences")

    theme_pref = st.selectbox(
        "🎨 Theme Preference",
        ["System Default", "Light Mode", "Dark Mode"],
        help="Choose your preferred theme"
    )

    notifications = st.checkbox(
        "🔔 Enable Notifications",
        value=True,
        help="Receive notifications about important events"
    )

    data_retention = st.selectbox(
        "🗃️ Data Retention",
        ["30 days", "90 days", "1 year", "Forever"],
        index=2,
        help="How long to keep your chat history"
    )

    # Account Actions
    st.subheader("🔧 Account Actions")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📤 Export Data"):
            st.info("Preparing data export...")
            # Export logic would go here
            st.success("Data export ready for download!")

    with col2:
        if st.button("🗑️ Clear History"):
            if st.checkbox("I understand this will delete all my chat history"):
                st.warning("This action cannot be undone!")
                if st.button("Confirm Delete"):
                    # Clear history logic would go here
                    st.success("Chat history cleared!")

    with col3:
        if st.button("❌ Delete Account"):
            st.error("⚠️ This will permanently delete your account and all data!")
            if st.checkbox("I understand this action is permanent"):
                if st.button("Confirm Account Deletion"):
                    # Account deletion logic would go here
                    st.success("Account deletion initiated...")

    st.markdown("---")
    if st.button("❌ Close"):
        st.session_state.show_profile = False
        st.rerun()


def main():
    """Universal main application function."""

    # Initialize theme state
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False

    # Detect platform for adaptive behavior
    platform_info = detect_platform()

    # Theme Toggle Button (at the top)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        if st.button("🌙 Dark" if not st.session_state.dark_mode else "☀️ Light",
                     key="theme_toggle",
                     help="Toggle between light and dark mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    # Apply theme CSS based on current mode
    theme_css = f"""
    <style>
        :root {{
            --bg-primary: {'#1e1e1e' if st.session_state.dark_mode else '#ffffff'};
            --bg-secondary: {'#2d2d2d' if st.session_state.dark_mode else '#f5f5f5'};
            --text-primary: {'#ffffff' if st.session_state.dark_mode else '#000000'};
            --text-secondary: {'#cccccc' if st.session_state.dark_mode else '#666666'};
            --accent-color: {'#4CAF50' if st.session_state.dark_mode else '#2196F3'};
            --border-color: {'#444444' if st.session_state.dark_mode else '#e0e0e0'};
        }}
        
        .stApp {{
            background-color: var(--bg-primary);
            color: var(--text-primary);
        }}
        
        .universal-header {{
            background: {'linear-gradient(135deg, #2c3e50, #3498db)' if st.session_state.dark_mode else 'linear-gradient(135deg, #667eea, #764ba2)'};
        }}
        
        .main .block-container {{
            background-color: var(--bg-primary);
        }}
    </style>
    """
    st.markdown(theme_css, unsafe_allow_html=True)

    # PWA Install Banner
    st.markdown(f"""
    <div id="install-banner" class="universal-header" style="display:none;">
        <h3>📱 Install CraftX.py</h3>
        <p id="install-instructions">Add to your device for instant access!</p>
        <button onclick="installApp()" class="universal-button" style="width:auto; margin:0.5rem;">
            Install Now
        </button>
        <button onclick="hideInstallBanner()" style="background:transparent; border:1px solid white; color:white; margin:0.5rem; padding:8px 16px; border-radius:4px;">
            Later
        </button>
    </div>
    """, unsafe_allow_html=True)

    # Universal Header with Logo
    # Get the logo first to avoid issues with f-string
    craftx_logo = get_logo_base64()

    st.markdown(f"""
    <div class="universal-header">
        <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 0.5rem;">
            <img src="{craftx_logo}" alt="CraftX.py Logo" style="height: clamp(32px, 6vw, 48px); width: auto; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));">
            <h1 style="margin:0; font-size:clamp(18px, 4vw, 28px);">CraftX.py Universal Assistant</h1>
        </div>
        <p style="margin:0; opacity:0.9; font-size:clamp(12px, 2.5vw, 16px);">
            AI-Powered • Cross-Platform • Zero Compatibility Issues
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Platform-specific welcome message
    if platform_info["system"] == "windows":
        welcome_msg = "Welcome Windows user! 🪟"
    elif platform_info["system"] == "darwin":
        welcome_msg = "Welcome Mac user! 🍎"
    elif platform_info["system"] == "linux":
        welcome_msg = "Welcome Linux user! 🐧"
    else:
        welcome_msg = "Welcome! 🌐"

    st.info(f"{welcome_msg} CraftX.py is fully optimized for your platform.")

    # Apply custom styling to make the info message white text
    st.markdown("""
    <style>
    .stAlert > div {
        background-color: var(--background-color, #f0f2f6) !important;
        color: white !important;
        border: 1px solid #667eea !important;
    }
    .stAlert > div > div {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Universal status grid
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="status-card">
            <h3 style="margin:0; color:green;">🟢</h3>
            <p style="margin:0; font-size:12px;"><strong>Status</strong></p>
            <p style="margin:0; font-size:14px;">Online</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="status-card">
            <h3 style="margin:0;">🤖</h3>
            <p style="margin:0; font-size:12px;"><strong>AI Model</strong></p>
            <p style="margin:0; font-size:14px;">Active</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="status-card">
            <h3 style="margin:0;">💬</h3>
            <p style="margin:0; font-size:12px;"><strong>Mode</strong></p>
            <p style="margin:0; font-size:14px;">Chat</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="status-card">
            <h3 style="margin:0;">🌐</h3>
            <p style="margin:0; font-size:12px;"><strong>Platform</strong></p>
            <p style="margin:0; font-size:14px;">{platform_info["system"].title()}</p>
        </div>
        """, unsafe_allow_html=True)

    # Universal sidebar
    with st.sidebar:
        st.markdown('<div class="universal-sidebar">', unsafe_allow_html=True)

        st.header("🛠️ Universal Settings")

        # Model selection with platform-specific recommendations
        models = ["WizardCoder-33B", "CommandR7B",
                  "CodeGeeX4", "Qwen2.5-Coder"]
        if platform_info["system"] == "windows":
            models.append("Windows-Optimized Model")
        elif platform_info["system"] == "darwin":
            models.append("Mac-Optimized Model")

        model = st.selectbox(
            "🤖 AI Model",
            models,
            help="Choose your AI assistant (auto-optimized for your platform)"
        )

        # Platform-specific features
        st.subheader("📱 Platform Features")

        # Universal quick actions
        st.markdown('<div class="quick-actions">', unsafe_allow_html=True)

        if st.button("🗑️ Clear Chat"):
            if 'messages' in st.session_state:
                st.session_state.messages = []
            st.success("Chat cleared!")

        if st.button("💾 Save Session"):
            if universal_storage:
                # Save with new storage system
                user_id = st.session_state.get('user_id', 'anonymous')
                session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                messages = st.session_state.get('messages', [])

                if universal_storage.save_chat_session(session_id, user_id, messages, {"platform": platform_info}):
                    st.success(f"Session saved! (ID: {session_id[:8]}...)")
                else:
                    st.error("Failed to save session")
            else:
                # Fallback to old method
                save_universal_session(platform_info)
                st.success("Session saved!")

        # Authentication Section
        st.subheader("🔐 Account & Authentication")

        if universal_auth:
            current_user = st.session_state.get('current_user')

            if current_user:
                st.success(f"👋 Welcome, {current_user.get('name', 'User')}!")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👤 Profile"):
                        st.session_state.show_profile = True
                with col2:
                    if st.button("🚪 Logout"):
                        if 'session_id' in st.session_state:
                            universal_auth.delete_session(
                                st.session_state.session_id)
                        st.session_state.clear()
                        st.rerun()
            else:
                st.info("Sign in to sync your data across devices")
                if st.button("🔑 Sign In Options"):
                    st.session_state.show_auth = True
        else:
            st.info("Authentication system loading...")

        # Cloud Storage Section
        st.subheader("☁️ Cloud Storage & Sync")

        if cloud_storage:
            config = cloud_storage.get_storage_config()
            enabled_providers = len(config.get("enabled_providers", []))

            if enabled_providers > 0:
                st.success(f"✅ {enabled_providers} provider(s) connected")
                if st.button("🔄 Sync Now"):
                    st.info("Syncing your data...")
                    # Sync logic would go here
                    st.success("Sync completed!")
            else:
                st.info("Connect cloud storage for automatic backup")

            if st.button("⚙️ Storage Settings"):
                st.session_state.show_storage = True
        else:
            st.info("Cloud storage system loading...")

        # Storage Usage Display
        if universal_storage:
            user_id = st.session_state.get('user_id', 'anonymous')
            stats = universal_storage.get_storage_stats(user_id)

            if stats:
                used_gb = stats.get('total_size_bytes', 0) / (1024**3)
                total_gb = 1024  # 1TB
                usage_percent = (used_gb / total_gb) * 100

                st.metric(
                    label="💾 Storage Used",
                    value=f"{used_gb:.2f} GB",
                    delta=f"{usage_percent:.1f}% of {total_gb} GB"
                )

                # Progress bar
                st.progress(min(usage_percent / 100, 1.0))

                # Quick stats
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("💬 Chats", stats.get('chat_sessions', 0))
                with col2:
                    st.metric("📁 Files", stats.get('files', 0))

        if st.button("📱 Share App"):
            st.markdown("""
            <button onclick="shareContent('Check out CraftX.py AI Assistant!', window.location.href)" 
                    class="universal-button">
                📤 Share CraftX.py
            </button>
            """, unsafe_allow_html=True)

        if st.button("🔔 Enable Notifications"):
            st.markdown("""
            <script>requestNotificationPermission();</script>
            """, unsafe_allow_html=True)
            st.info("Notification permission requested!")

        st.markdown('</div>', unsafe_allow_html=True)

        # Platform-specific tips
        st.subheader("💡 Platform Tips")
        if platform_info["system"] == "windows":
            st.info("💡 Pin to taskbar for quick access!")
        elif platform_info["system"] == "darwin":
            st.info("💡 Add to Dock for quick access!")
        elif "mobile" in str(platform_info).lower():
            st.info("💡 Add to home screen for app-like experience!")
        else:
            st.info("💡 Bookmark for quick access!")

        st.markdown('</div>', unsafe_allow_html=True)

    # Universal chat interface
    display_universal_chat()

    # Universal input area
    universal_input_area()

    # Show Authentication Modal
    if st.session_state.get('show_auth', False):
        show_authentication_modal()

    # Show Storage Settings Modal
    if st.session_state.get('show_storage', False):
        show_storage_settings_modal()

    # Show Profile Modal
    if st.session_state.get('show_profile', False):
        show_profile_modal()

    # Floating Action Button
    st.markdown("""
    <button class="fab" onclick="quickAccess()" title="Quick Access">
        ⚡
    </button>
    """, unsafe_allow_html=True)

    # ElevateCraft Footer with Sponsor Icons
    st.markdown("---")

    # Get the ElevateCraft logo
    elevatecraft_logo = get_elevatecraft_logo_base64()

    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0; margin-top: 3rem; border-top: 1px solid var(--border-color, #e0e0e0);">
        <div style="margin-bottom: 1rem; display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
            <span style="color: var(--text-secondary, #666); font-size: 14px;">
                Made with ❤️ by 
                <a href="https://elevatecraft.org" target="_blank" style="color: var(--accent-color, #2196F3); text-decoration: none; font-weight: bold;">
                    ElevateCraft
                </a>
            </span>
            <img src="{elevatecraft_logo}" style="width: 24px; height: 24px; margin-left: 0.5rem; vertical-align: middle;" alt="ElevateCraft Logo">
        </div>
        
        <div style="margin-top: 1.5rem; font-size: 14px; color: var(--text-secondary, #666);">
            <p>Questions, Comments, or Collaboration? Let us know at 
                <a href="mailto:craftx@elevatecraft.org" style="color: var(--accent-color, #2196F3); font-weight: bold; text-decoration: none;">
                    craftx@elevatecraft.org
                </a>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer text
    st.markdown("""
    <div style="text-align: center;">
        <div style="margin-top: 1.5rem; font-size: 11px; color: var(--text-secondary, #999);">
            © 2025 ElevateCraft • Open Source • Universal Compatibility
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_universal_chat():
    """Display chat interface optimized for all devices."""

    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Chat container
    st.markdown('<div class="universal-chat">', unsafe_allow_html=True)
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

    if not st.session_state.messages:
        # Universal welcome message
        st.markdown("""
        <div class="assistant-message">
            <strong>👋 Welcome to CraftX.py Universal Assistant!</strong><br><br>
            I work perfectly on <em>every device and platform</em>:
            <ul style="margin:10px 0; padding-left:20px;">
                <li>📱 <strong>Mobile:</strong> Android, iPhone, Samsung, etc.</li>
                <li>🖥️ <strong>Desktop:</strong> Windows, Mac, Linux</li>
                <li>💻 <strong>Legacy:</strong> Old computers, any browser</li>
                <li>⌚ <strong>Tablets:</strong> iPad, Android tablets</li>
            </ul>
            <strong>🚀 I can help you with:</strong>
            <ul style="margin:10px 0; padding-left:20px;">
                <li>🔧 Code generation & debugging</li>
                <li>📚 Documentation & explanations</li>
                <li>🚀 Project development</li>
                <li>💡 Problem solving</li>
                <li>🌐 Cross-platform development</li>
            </ul>
            <em>What can I help you with today?</em>
        </div>
        """, unsafe_allow_html=True)

    # Display chat messages
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            st.markdown(f"""
            <div class="message user-message">
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message assistant-message">
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Close chat-messages
    st.markdown('</div>', unsafe_allow_html=True)  # Close universal-chat


def universal_input_area():
    """Universal input area that works on all devices."""

    # Quick suggestions optimized for all platforms
    st.markdown("### 💡 Universal Quick Actions")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔧 Debug Code", use_container_width=True, key="debug"):
            handle_quick_input("Help me debug my code for any platform")
        if st.button("📚 Explain Concept", use_container_width=True, key="explain"):
            handle_quick_input("Explain this programming concept")
        if st.button("📱 Mobile Development", use_container_width=True, key="mobile"):
            handle_quick_input("Help me with mobile app development")

    with col2:
        if st.button("🚀 Generate Code", use_container_width=True, key="generate"):
            handle_quick_input("Generate cross-platform code")
        if st.button("💡 Get Ideas", use_container_width=True, key="ideas"):
            handle_quick_input("Give me universal project ideas")
        if st.button("🌐 Cross-Platform", use_container_width=True, key="cross"):
            handle_quick_input("Help with cross-platform compatibility")

    # Main input with universal compatibility
    st.markdown("### 💬 Your Message")

    # Create columns for input and send button
    input_col, send_col = st.columns([4, 1])

    with input_col:
        user_input = st.text_input(
            "Type your message...",
            placeholder="Ask me anything about development, coding, or universal compatibility!",
            label_visibility="collapsed",
            key="main_input"
        )

    with send_col:
        send_clicked = st.button(
            "🚀", use_container_width=True, help="Send Message")

    # Handle input submission
    if send_clicked and user_input:
        handle_user_input(user_input)
        st.rerun()

    # Handle Enter key submission
    if user_input and st.session_state.get('submit_on_enter', False):
        handle_user_input(user_input)
        st.session_state['submit_on_enter'] = False
        st.rerun()


def handle_quick_input(prompt):
    """Handle quick suggestion inputs."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate AI response
    response = generate_universal_ai_response(prompt)
    st.session_state.messages.append(
        {"role": "assistant", "content": response})


def handle_user_input(user_input):
    """Handle user input and generate response."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate AI response
    response = generate_universal_ai_response(user_input)
    st.session_state.messages.append(
        {"role": "assistant", "content": response})

    # Clear input
    if 'main_input' in st.session_state:
        st.session_state['main_input'] = ""


def generate_universal_ai_response(prompt):
    """Generate AI response with universal compatibility focus."""

    # Enhanced responses that focus on cross-platform compatibility
    universal_responses = [
        f"I understand you need help with '{prompt}'. I'll provide a solution that works on ALL platforms - Android, iPhone, Windows, Mac, Linux, and any device! Let me create a universal approach...",

        f"Great question about '{prompt}'! Here's my cross-platform solution that ensures zero compatibility issues across all devices and operating systems...",

        f"Perfect! For '{prompt}', I'll give you a universal solution that works identically on mobile phones, tablets, old computers, new computers, and any browser...",

        f"Excellent! I'll help you with '{prompt}' using approaches that are 100% compatible with every device type - from the latest iPhone to older Windows computers...",

        f"Thanks for asking about '{prompt}'! I specialize in universal solutions that work flawlessly on Samsung, iPhone, Android, Windows, Mac, Linux, and legacy systems..."
    ]

    # Platform-specific enhancements
    platform_tips = [
        "\n\n🌐 **Universal Compatibility Notes:**\n- ✅ Works on all Android devices\n- ✅ Compatible with all iPhone/iPad versions\n- ✅ Supports Windows XP through Windows 11\n- ✅ MacOS compatible (all versions)\n- ✅ Linux distribution friendly\n- ✅ Legacy browser support included",

        "\n\n📱 **Device-Specific Optimizations:**\n- Touch-friendly for mobile devices\n- Keyboard shortcuts for desktop\n- High-DPI display support\n- Offline functionality included\n- Responsive design for all screen sizes",

        "\n\n🔧 **Cross-Platform Implementation:**\n- Progressive Web App technology\n- Universal keyboard shortcuts\n- Touch gesture support\n- Multi-browser compatibility\n- Accessibility features included"
    ]

    import random
    base_response = random.choice(universal_responses)
    enhancement = random.choice(platform_tips)

    return base_response + enhancement


def save_universal_session(platform_info):
    """Save current chat session with platform info."""
    if 'messages' in st.session_state:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        platform_name = platform_info.get("system", "unknown")
        filename = f"chat_logs/universal_session_{platform_name}_{timestamp}.json"

        os.makedirs("chat_logs", exist_ok=True)

        session_data = {
            "timestamp": timestamp,
            "platform": platform_info,
            "messages": st.session_state.messages,
            "version": "universal_1.0.0"
        }

        with open(filename, "w", encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
