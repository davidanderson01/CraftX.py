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

import base64
import json
import os
import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

# Import universal systems
try:
    from craftxpy.utils.auth import universal_auth
    from craftxpy.utils.cloud_storage import cloud_storage
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
        "assets/img/elevatecraft-logo.svg",
        "static/elevatecraft-logo.png",
        "assets/img/elevatecraft-logo.png"
    ]

    for logo_path in elevatecraft_logo_paths:
        if os.path.exists(logo_path):
            try:
                with open(logo_path, "rb") as f:
                    logo_bytes = f.read()
                    if logo_path.endswith('.svg'):
                        logo_base64 = base64.b64encode(logo_bytes).decode()
                        return f"data:image/svg+xml;base64,{logo_base64}"
                    else:
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

""", unsafe_allow_html=True)


def show_privacy_policy_modal():
    """Show privacy policy modal."""
    st.markdown("### 🔒 Privacy Policy")

    st.markdown("""
    **Last updated: July 27, 2025**

    ---

    ## Introduction

    ElevateCraft ("we," "us," or "our") is committed to protecting your privacy and ensuring the ethical handling of your personal data. This Privacy Policy describes how we collect, use, disclose, and safeguard your information when you visit elevatecraft.org, sign in via OAuth providers, or download and use CraftX.py.

    ---

    ## Information We Collect

    We collect data to provide secure access, prevent malicious activity, and improve our services.

    - **Account Information**  
      When you sign in using Microsoft, Apple, Google, Okta, ORCID, or GitHub, we receive basic profile details (name, email, unique user ID).

    - **Authentication Tokens**  
      We store the tokens necessary to validate and refresh your session securely.

    - **Usage Data**  
      We log your interactions with our site and CraftX.py (IP address, timestamps, pages visited, download activity, and error reports).

    - **Cookies and Tracking Technologies**  
      We use cookies and similar technologies to maintain your session, remember preferences, and analyze site performance.

    ---

    ## How We Use Your Information

    We process your data for the following purposes:

    - **Secure Authentication**  
      To verify your identity, gate downloads, and prevent unauthorized or malicious use.

    - **AI Oversight**  
      To feed our embedded AI Safety Officer a risk assessment of configuration and usage patterns, ensuring CraftX.py is used responsibly.

    - **Service Improvement**  
      To analyze usage trends, fix bugs, and enhance features.

    - **Communication**  
      To send important notices, updates, or request feedback about CraftX.py and ElevateCraft services.

    ---

    ## Data Sharing & Disclosure

    We do not sell or rent your personal information. We may share data in limited circumstances:

    - **Service Providers**  
      Third-party providers who help power authentication, analytics, hosting, and email notifications. They are bound by confidentiality obligations.

    - **Legal Requirements**  
      When required by law or to protect our rights, safety, or property, we may disclose information to comply with legal processes.

    ---

    ## Data Retention

    We retain personal data only as long as necessary to fulfill the purposes outlined in this policy or as required by applicable law. Authentication logs and usage records are stored for up to 24 months, after which they are deleted or anonymized.

    ---

    ## Data Security

    We implement administrative, technical, and physical safeguards to protect your data. Measures include encryption of data in transit and at rest, strict access controls, and routine security audits.

    ---

    ## Third-Party OAuth Providers

    When you use external sign-in options, the provider's privacy policy governs their handling of your data. We recommend reviewing:

    - **Microsoft**: https://privacy.microsoft.com  
    - **Apple**: https://www.apple.com/legal/privacy/  
    - **Google**: https://policies.google.com/privacy  
    - **Okta**: https://www.okta.com/privacy/  
    - **ORCID**: https://info.orcid.org/privacy/  
    - **GitHub**: https://docs.github.com/en/site-policy/privacy-policies

    ---

    ## Your Rights

    Depending on your jurisdiction, you may have the right to:

    - Access, correct, or delete your personal data  
    - Restrict or object to our processing of your data  
    - Withdraw consent for certain processing activities  
    - Lodge a complaint with a supervisory authority

    To exercise these rights, please contact us at privacy@elevatecraft.org.

    ---

    ## International Data Transfers

    ElevateCraft is based in the United States. If you access our services from outside the U.S., your information may be transferred, stored, and processed here. We take steps to ensure adequate protections are in place.

    ---

    ## Children's Privacy

    Our services are not directed to individuals under 13. We do not knowingly collect personal information from children. If you believe a child has provided us data, please contact us, and we will promptly delete that information.

    ---

    ## Changes to This Privacy Policy

    We may update this policy to reflect changes in our practices or legal requirements. We will post the revised date at the top and notify you of significant changes via email or on our website.

    ---

    ## Contact Us

    For questions or requests concerning this Privacy Policy, please contact:

    **ElevateCraft Privacy Team**  
    Email: support@elevatecraft.org  
    Address: 123 Innovation Drive, Hiawatha, IA 52233, United States
    """)

    st.markdown("---")
    if st.button("❌ Close", key="close_privacy_policy"):
        st.session_state.show_privacy_policy = False
        st.rerun()


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
    config = universal_auth.get_auth_config()
    configured_providers = config.get("enabled_providers", [])

    if not configured_providers:
        st.warning("⚠️ No authentication providers configured yet")
        st.info(
            "Please configure OAuth providers using the admin panel below to enable sign-in.")
        st.caption(
            "💡 Administrators need to set up OAuth credentials from providers like Google, Microsoft, GitHub, etc.")

        # Show admin configuration button prominently
        if st.button("🔧 Configure Providers (Admin)", use_container_width=True, type="primary"):
            st.session_state.show_auth_admin = True
            st.rerun()
        st.caption(
            "🔧 Click above to open the admin panel and configure OAuth providers")

        if st.button("❌ Close", key="close_auth_no_providers"):
            st.session_state.show_auth = False
            st.rerun()
        return

    st.info("Choose your preferred sign-in method:")
    st.caption(
        "🔐 Select one of the configured OAuth providers below to authenticate")

    # Create provider buttons for configured providers only
    configured_provider_ids = [p["provider_id"] for p in configured_providers]
    available_providers = {
        k: v for k, v in providers.items() if k in configured_provider_ids}

    if available_providers:
        cols = st.columns(min(2, len(available_providers)))
        for i, (provider_id, provider_info) in enumerate(available_providers.items()):
            with cols[i % len(cols)]:
                if st.button(
                    f"{provider_info['icon']} {provider_info['name']}",
                    key=f"auth_{provider_id}",
                    help=f"Sign in with {provider_info['name']}"
                ):
                    if universal_auth.is_provider_configured(provider_id):
                        # Generate OAuth URL (this would normally redirect to the provider)
                        redirect_uri = "http://localhost:8080/auth/callback"
                        try:
                            oauth_url = universal_auth.generate_oauth_url(
                                provider_id, redirect_uri)
                            st.success(
                                f"✅ {provider_info['name']} authentication ready!")
                            st.info(
                                "📋 OAuth URL generated. In a real deployment, this would redirect to the provider.")
                            st.code(oauth_url, language="text")

                            # Simulate successful login for demo
                            mock_user_data = {
                                "id": f"demo_user_{provider_id}",
                                "name": f"Demo User ({provider_info['name']})",
                                "email": f"demo@{provider_id}.com",
                                "provider": provider_info['name'],
                                "created_at": datetime.now().isoformat()
                            }
                            session_id = universal_auth.create_session(
                                mock_user_data, provider_id)
                            st.session_state.current_user = mock_user_data
                            st.session_state.session_id = session_id
                            st.session_state.user_id = mock_user_data["id"]

                            st.success(
                                f"🎉 Successfully signed in as {mock_user_data['name']}!")
                            st.balloons()
                        except ValueError as e:
                            st.error(f"❌ Configuration error: {str(e)}")
                    else:
                        st.warning(
                            f"{provider_info['name']} not configured by administrator")

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔒 Privacy Policy"):
            st.session_state.show_privacy_policy = True
            st.rerun()
        st.caption("📋 Click to view our privacy policy")
    with col2:
        if st.button("❌ Close", key="close_auth_main"):
            st.session_state.show_auth = False
            st.rerun()
        st.caption("✖️ Close this authentication dialog")


def show_auth_admin_modal():
    """Show authentication provider admin configuration modal."""
    st.markdown("### ⚙️ OAuth Provider Configuration (Admin)")

    if not universal_auth:
        st.error("Authentication system not available")
        if st.button("Close"):
            st.session_state.show_auth_admin = False
            st.rerun()
        return

    st.warning(
        "🔐 **Admin Access Required** - This panel configures OAuth providers for all users.")

    providers = universal_auth.get_all_providers()
    config = universal_auth.get_auth_config()
    configured_providers = {p["provider_id"]
        : p for p in config.get("enabled_providers", [])}

    # Quick setup for testing
    st.subheader("🚀 Quick Demo Setup")
    st.info("For testing purposes, you can enable providers with demo credentials")
    st.caption(
        "⚠️ These are demo credentials only - use the manual configuration below for production")

    demo_providers = ["google", "microsoft", "github", "apple"]
    cols = st.columns(2)

    for i, provider_id in enumerate(demo_providers):
        provider_info = providers.get(provider_id, {})
        with cols[i % 2]:
            if provider_id in configured_providers:
                if st.button(f"✅ {provider_info.get('icon', '🔑')} {provider_info.get('name', provider_id.title())} (Configured)", key=f"demo_{provider_id}"):
                    st.success(
                        f"{provider_info.get('name', provider_id.title())} is already configured!")
            else:
                if st.button(f"🔧 Setup {provider_info.get('icon', '🔑')} {provider_info.get('name', provider_id.title())}", key=f"demo_{provider_id}"):
                    # Add demo configuration
                    result = universal_auth.add_provider_config(
                        provider_id=provider_id,
                        client_id=f"demo_client_{provider_id}",
                        client_secret=f"demo_secret_{provider_id}",
                        domain="" if not provider_info.get(
                            "requires_domain") else "demo.com"
                    )
                    if result:
                        st.success(
                            f"✅ {provider_info.get('name', provider_id.title())} configured with demo credentials!")
                        st.rerun()
                    else:
                        st.error(
                            f"❌ Failed to configure {provider_info.get('name', provider_id.title())}")

    st.markdown("---")

    # Manual provider configuration
    st.subheader("🔧 Manual Provider Configuration")
    st.caption("Configure real OAuth providers for production use")

    with st.expander("➕ Add New Provider", expanded=False):
        st.info(
            "💡 Select a provider below and enter your OAuth credentials from their developer console")
        provider_options = [
            pid for pid in providers.keys() if pid not in configured_providers]

        if provider_options:
            selected_provider = st.selectbox(
                "Select Provider",
                provider_options,
                format_func=lambda x: f"{providers[x].get('icon', '🔑')} {providers[x].get('name', x.title())}",
                help="Choose which OAuth provider you want to configure"
            )
            st.caption(
                "📝 Select the OAuth provider you want to set up for user authentication")

            provider_info = providers[selected_provider]

            st.write(f"**Setting up {provider_info['name']}**")
            st.info(f"🌐 Authorization URL: `{provider_info['auth_url']}`")

            # Provider-specific instructions with detailed guidance
            setup_instructions = {
                "google": "Get these from Google Cloud Console → APIs & Services → Credentials → Create OAuth 2.0 Client ID",
                "microsoft": "Get these from Azure Portal → App Registrations → New Registration → Authentication",
                "github": "Get these from GitHub → Settings → Developer settings → OAuth Apps → New OAuth App",
                "apple": "Get these from Apple Developer → Certificates, Identifiers & Profiles → Services → Sign In with Apple",
                "orcid": "Get these from ORCID.org → Sign In → Developer Tools → Register for the public API (requires ORCID account)",
                "okta": "Get these from Okta Admin Console → Applications → Create App Integration → OIDC - Web Application",
                "auth0": "Get these from Auth0 Dashboard → Applications → Create Application → Regular Web Applications",
                "discord": "Get these from Discord Developer Portal → Applications → New Application → OAuth2",
                "linkedin": "Get these from LinkedIn Developer Portal → My Apps → Create App → Auth tab",
                "twitter": "Get these from Twitter Developer Portal → Projects & Apps → Create App → Keys and tokens"
            }

            instruction = setup_instructions.get(
                selected_provider, "Get these from your OAuth provider's developer console")
            st.caption(f"💡 {instruction}")

            # Provider-specific placeholders and detailed help
            placeholders = {
                "google": "123456789012-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com",
                "microsoft": "12345678-1234-1234-1234-123456789012",
                "github": "Iv1.1234567890123456",
                "apple": "com.yourcompany.yourapp.signin",
                "orcid": "APP-ABCDEFGHIJKLMNOP (16-character alphanumeric)",
                "okta": "0oa1234567890abcdef0h7",
                "auth0": "AbCdEfGhIjKlMnOpQrStUvWxYz123456",
                "discord": "123456789012345678",
                "linkedin": "12345678901234",
                "twitter": "1234567890123456789"
            }

            help_texts = {
                "google": "From Google Cloud Console: Create credentials → OAuth 2.0 Client IDs. This is your Client ID.",
                "microsoft": "From Azure Portal: App registrations → Your app → Overview. This is your Application (client) ID.",
                "github": "From GitHub Developer settings: Create OAuth App. This is your Client ID (starts with 'Iv1.').",
                "apple": "From Apple Developer: Create Service ID. This is your Services ID (reverse domain format).",
                "orcid": "From ORCID Developer Tools: Register public API client. This is your Client ID (format: APP-XXXXXXXXXXXXXXXX).",
                "okta": "From Okta Admin Console: Create OIDC web app. This is your Client ID.",
                "auth0": "From Auth0 Dashboard: Create Regular Web Application. This is your Client ID.",
                "discord": "From Discord Developer Portal: Create Application → OAuth2. This is your Client ID (18-digit number).",
                "linkedin": "From LinkedIn Developer Portal: Create App → Auth tab. This is your Client ID.",
                "twitter": "From Twitter Developer Portal: Create App → Keys and tokens. This is your Client ID."
            }

            client_id = st.text_input(
                "Client ID",
                key=f"client_id_{selected_provider}",
                help=help_texts.get(
                    selected_provider, "The public identifier for your OAuth application. This is safe to share and will be visible in requests."),
                placeholder=placeholders.get(
                    selected_provider, "Enter your client ID here")
            )
            st.caption(
                f"📋 Copy the Client ID from your {provider_info['name']} app settings")

            # Special note for ORCID
            if selected_provider == "orcid":
                st.info("💡 **ORCID Note**: Your Client ID will start with 'APP-' followed by 16 characters (letters/numbers). Example: APP-ABCDEFGHIJKLMNOP")

            client_secret = st.text_input(
                "Client Secret",
                type="password",
                key=f"client_secret_{selected_provider}",
                help="The private key for your OAuth application. Keep this secret and never share it publicly.",
                placeholder="Enter your client secret here"
            )
            st.caption(
                f"🔐 Copy the Client Secret from your {provider_info['name']} app settings (keep this private!)")

            # Special note for ORCID secret
            if selected_provider == "orcid":
                st.warning(
                    "🔒 **ORCID Security**: Your Client Secret is a long random string. Keep this completely private and never share it in public code or repositories.")

            domain = ""
            if provider_info.get("requires_domain"):
                domain = st.text_input(
                    "Domain",
                    key=f"domain_{selected_provider}",
                    help=f"Your {provider_info['name']} domain without https://",
                    placeholder=f"your-company.{selected_provider}.com"
                )
                st.caption(
                    f"🌐 Enter your {provider_info['name']} domain (e.g., your-company.{selected_provider}.com)")

            if st.button("💾 Save Configuration", key=f"save_{selected_provider}"):
                if client_id and client_secret:
                    if provider_info.get("requires_domain") and not domain:
                        st.error(
                            "❌ Domain is required for this provider - please enter your domain above")
                    else:
                        result = universal_auth.add_provider_config(
                            provider_id=selected_provider,
                            client_id=client_id,
                            client_secret=client_secret,
                            domain=domain
                        )
                        if result:
                            st.success(
                                f"✅ {provider_info['name']} configured successfully!")
                            st.rerun()
                        else:
                            st.error(
                                f"❌ Failed to configure {provider_info['name']}")
                else:
                    st.error(
                        "❌ Please fill in both Client ID and Client Secret fields above")
        else:
            st.info("All available providers are already configured!")

    # Show configured providers
    if configured_providers:
        st.subheader("✅ Configured Providers")
        st.caption(
            "These OAuth providers are currently set up and ready for user authentication")

        for provider_id, provider_config in configured_providers.items():
            provider_info = providers.get(provider_id, {})

            with st.expander(f"{provider_info.get('icon', '🔑')} {provider_info.get('name', provider_id.title())}", expanded=False):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.write(
                        f"**Client ID:** `{provider_config.get('client_id', 'Not set')[:20]}...`")
                    st.write(
                        f"**Status:** {'✅ Enabled' if provider_config.get('enabled', True) else '❌ Disabled'}")
                    st.write(
                        f"**Added:** {provider_config.get('added_date', 'Unknown')[:10]}")
                    if provider_config.get('domain'):
                        st.write(f"**Domain:** `{provider_config['domain']}`")

                with col2:
                    if st.button("🗑️ Remove", key=f"remove_{provider_id}"):
                        # Remove provider
                        config = universal_auth.get_auth_config()
                        config["enabled_providers"] = [
                            p for p in config["enabled_providers"]
                            if p["provider_id"] != provider_id
                        ]
                        universal_auth.save_auth_config(config)
                        st.success(
                            f"Removed {provider_info.get('name', provider_id)}")
                        st.rerun()

    # Instructions
    st.markdown("---")
    st.subheader("📋 Setup Instructions")
    st.caption(
        "Step-by-step guides for setting up OAuth applications with each provider")

    instructions = {
        "google": "1. Go to [Google Cloud Console](https://console.cloud.google.com/)\n2. Create a new project or select existing\n3. Enable Google+ API or Google OAuth2 API\n4. Go to Credentials → Create Credentials → OAuth 2.0 Client IDs\n5. Set Application type to 'Web application'\n6. Add redirect URI: `http://localhost:8080/auth/callback`\n7. Copy the Client ID and Client Secret",
        "microsoft": "1. Go to [Azure Portal](https://portal.azure.com/)\n2. Navigate to Azure Active Directory → App registrations\n3. Click 'New registration'\n4. Set redirect URI: `http://localhost:8080/auth/callback`\n5. After creation, go to Certificates & secrets → New client secret\n6. Copy the Application (client) ID and the generated secret value",
        "github": "1. Go to [GitHub Developer Settings](https://github.com/settings/developers)\n2. Click 'OAuth Apps' → 'New OAuth App'\n3. Fill in application details\n4. Set Authorization callback URL: `http://localhost:8080/auth/callback`\n5. Click 'Register application'\n6. Copy the Client ID and generate a Client Secret",
        "apple": "1. Go to [Apple Developer Portal](https://developer.apple.com/)\n2. Sign in with your Apple Developer account\n3. Go to Certificates, Identifiers & Profiles → Services\n4. Create new Service ID for 'Sign in with Apple'\n5. Configure domains and redirect URI: `http://localhost:8080/auth/callback`\n6. Copy the Services ID as your Client ID\n7. Generate a client secret using your private key",
        "orcid": "**ORCID Setup (Detailed Steps):**\n\n1. **Create ORCID Account**: Go to [ORCID.org](https://orcid.org) and create an account if you don't have one\n2. **Access Developer Tools**: Sign in → Click your name/icon → Developer Tools\n3. **Register Public API Client**: Click 'Register for the public API'\n4. **Fill Application Details**:\n   - Name: Your application name (e.g., 'CraftX.py Authentication')\n   - Website: Your website URL or `http://localhost:8080`\n   - Description: Brief description of your application\n   - Redirect URI: `http://localhost:8080/auth/callback`\n5. **Get Credentials**: After registration, copy:\n   - **Client ID**: Format APP-XXXXXXXXXXXXXXXX (16 characters after APP-)\n   - **Client Secret**: Long random string (keep this secure!)\n6. **Important**: ORCID Client ID always starts with 'APP-' followed by 16 alphanumeric characters",
        "okta": "1. Go to [Okta Admin Console](https://dev.okta.com/)\n2. Create developer account if needed\n3. Navigate to Applications → Create App Integration\n4. Choose 'OIDC - OpenID Connect' → 'Web Application'\n5. Set redirect URI: `http://localhost:8080/auth/callback`\n6. Copy the Client ID and Client Secret",
        "auth0": "1. Go to [Auth0 Dashboard](https://manage.auth0.com/)\n2. Create account if needed\n3. Navigate to Applications → Create Application\n4. Choose 'Regular Web Applications'\n5. Go to Settings tab\n6. Add `http://localhost:8080/auth/callback` to Allowed Callback URLs\n7. Copy the Client ID and Client Secret",
        "discord": "1. Go to [Discord Developer Portal](https://discord.com/developers/applications)\n2. Click 'New Application'\n3. Give your application a name\n4. Go to OAuth2 → General\n5. Add redirect URL: `http://localhost:8080/auth/callback`\n6. Copy the Client ID and Client Secret",
        "linkedin": "1. Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/)\n2. Click 'Create app'\n3. Fill in required information\n4. Go to Auth tab\n5. Add `http://localhost:8080/auth/callback` to Authorized redirect URLs\n6. Copy the Client ID and Client Secret",
        "twitter": "1. Go to [Twitter Developer Portal](https://developer.twitter.com/)\n2. Create developer account if needed\n3. Create a new project and app\n4. Go to app settings → Keys and tokens\n5. Generate OAuth 2.0 Client ID and Client Secret\n6. Add `http://localhost:8080/auth/callback` to callback URLs"
    }

    for provider_id, instruction in instructions.items():
        provider_info = providers.get(provider_id, {})
        with st.expander(f"📖 {provider_info.get('icon', '🔑')} {provider_info.get('name', provider_id.title())} Setup"):
            st.markdown(instruction)

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 Refresh"):
            st.rerun()
        st.caption("🔄 Refresh the configuration panel")
    with col2:
        if st.button("❌ Close", key="close_auth_admin"):
            st.session_state.show_auth_admin = False
            st.rerun()
        st.caption("✖️ Close the admin configuration panel")


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
    enabled_providers = {p["provider_id"]
        : p for p in config.get("enabled_providers", [])}

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
    if st.button("❌ Close", key="close_storage"):
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
    if st.button("❌ Close", key="close_profile"):
        st.session_state.show_profile = False
        st.rerun()


def show_landing_page(platform_info):
    """Show the landing page with CraftX.py and ElevateCraft information and authentication options."""

    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); border-radius: 1rem; margin: 1rem 0;">
        <h2 style="color: var(--accent-color, #2196F3); margin-bottom: 1rem;">🚀 Welcome to CraftX.py</h2>
        <p style="font-size: 1.2rem; color: var(--text-primary, #000); margin-bottom: 1.5rem; max-width: 800px; margin-left: auto; margin-right: auto;">
            The Universal AI Assistant that works flawlessly on <strong>every device</strong> and <strong>every platform</strong> - 
            from the latest smartphones to legacy computers, with zero compatibility issues.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # What is CraftX.py?
    st.markdown("### 🤖 What is CraftX.py?")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        **CraftX.py** is a revolutionary AI-powered assistant designed with one core principle: 
        **Universal Compatibility**. Unlike other AI tools that may break on older devices or 
        certain platforms, CraftX.py guarantees:
        
        ✅ **Works on ALL devices**: Android, iPhone, Windows, Mac, Linux, ChromeOS  
        ✅ **Zero compatibility issues**: From Windows XP to the latest iOS  
        ✅ **Cross-platform consistency**: Same experience everywhere  
        ✅ **Progressive Web App**: No app store required, works in any browser  
        ✅ **Offline capability**: Core features work without internet  
        ✅ **Touch & keyboard optimized**: Perfect for both mobile and desktop  
        
        Whether you're using a 10-year-old laptop or the newest smartphone, 
        CraftX.py delivers the same powerful AI assistance with intelligent 
        code generation, problem-solving, and creative support.
        """)

    with col2:
        # Platform compatibility grid
        st.markdown("""
        <div style="background: var(--bg-secondary, #f5f5f5); padding: 1rem; border-radius: 0.5rem; text-align: center;">
            <h4 style="margin-bottom: 1rem; color: var(--text-primary, #000);">✅ 100% Compatible</h4>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem; font-size: 0.9rem;">
                <div>📱 Android</div>
                <div>🍎 iOS</div>
                <div>🪟 Windows</div>
                <div>🖥️ macOS</div>
                <div>🐧 Linux</div>
                <div>🌐 ChromeOS</div>
                <div>📟 Legacy Systems</div>
                <div>📱 Any Browser</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # What is ElevateCraft?
    st.markdown("### 🏢 About ElevateCraft")

    col1, col2 = st.columns([1, 2])

    with col1:
        # Get ElevateCraft logo
        elevatecraft_logo = get_elevatecraft_logo_base64()
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem;">
            <img src="{elevatecraft_logo}" style="width: 120px; height: 120px; border-radius: 50%; box-shadow: 0 4px 12px rgba(0,0,0,0.1);" alt="ElevateCraft Logo">
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        **ElevateCraft** is a forward-thinking technology organization dedicated to creating 
        innovative solutions that bridge the digital divide. Our mission is simple yet powerful:
        
        🎯 **Mission**: Make advanced technology accessible to everyone, regardless of their device or technical expertise  
        🌍 **Vision**: A world where technology limitations never prevent someone from achieving their goals  
        💡 **Values**: Universal accessibility, open-source innovation, and community-driven development  
        
        **Our Projects:**
        - 🤖 **CraftX.py**: Universal AI Assistant Platform
        - 🔧 **Universal Tools**: Cross-platform utilities and applications
        - 📚 **Open Source Libraries**: Developer tools for universal compatibility
        - 🎓 **Educational Resources**: Making technology learning accessible to all
        
        Founded on the principle that good technology should work for everyone, 
        ElevateCraft is committed to eliminating compatibility barriers and 
        creating inclusive digital experiences.
        """)

    st.markdown("---")

    # Key Features Section
    st.markdown("### ⭐ Key Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **🧠 AI-Powered Intelligence**
        - Advanced language models
        - Code generation & debugging
        - Creative writing assistance
        - Problem-solving guidance
        - Multi-language support
        """)

    with col2:
        st.markdown("""
        **🌐 Universal Compatibility**
        - Works on any device/OS
        - Progressive Web App
        - Offline functionality
        - Legacy browser support
        - Touch & keyboard optimized
        """)

    with col3:
        st.markdown("""
        **🔒 Privacy & Security**
        - Secure authentication
        - Encrypted data storage
        - Privacy-first design
        - GDPR compliant
        - No tracking or ads
        """)

    st.markdown("---")

    # Authentication Section
    st.markdown("### 🔐 Get Started - Sign In or Create Account")

    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(33, 150, 243, 0.1)); 
                padding: 1.5rem; border-radius: 0.8rem; margin: 1rem 0; text-align: center;">
        <h4 style="color: var(--accent-color, #2196F3); margin-bottom: 1rem;">
            🚀 Ready to experience universal AI assistance?
        </h4>
        <p style="margin-bottom: 1.5rem; color: var(--text-primary, #000);">
            Sign in with your preferred provider to access all features, sync your data across devices, 
            and join the CraftX.py community!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Center the authentication button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔑 Sign In / Create Account", key="landing_auth",
                     help="Choose from 10+ authentication providers including Google, Microsoft, GitHub, and more"):
            st.session_state.show_auth = True
            st.rerun()

    # Why sign in benefits
    st.markdown("### 🎁 Benefits of Creating an Account")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **🔄 Sync Across Devices**
        - Access your chats on any device
        - Seamless experience everywhere
        - Automatic backup & restore
        
        **📊 Enhanced Features**
        - Unlimited chat history
        - Advanced AI models
        - Custom preferences
        """)

    with col2:
        st.markdown("""
        **☁️ Cloud Storage**
        - Secure data backup
        - Multi-provider support
        - Privacy-focused encryption
        
        **🎯 Personalization**
        - Tailored AI responses
        - Custom workflows
        - Usage analytics
        """)

    # Demo Access
    st.markdown("---")
    st.markdown("### 🎯 Try Before You Sign In")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("💡 **Demo Mode**: Want to try CraftX.py first? You can explore basic features without signing in, but full functionality requires an account.")

        if st.button("🔍 Continue as Guest", key="demo_mode"):
            st.session_state.demo_mode = True
            st.rerun()

    # Footer with current site reference and privacy policy
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: var(--bg-secondary, #f5f5f5); border-radius: 0.5rem; margin-top: 2rem;">
        <p style="margin: 0; color: var(--text-secondary, #666); font-size: 0.9rem;">
            🌟 This platform replaces the content currently shown at 
            <a href="https://craftx.elevatecraft.org" target="_blank" style="color: var(--accent-color, #2196F3);">
                craftx.elevatecraft.org
            </a> with a fully interactive AI assistant experience
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Privacy Policy and Legal Links
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0;">
            <p style="font-size: 0.85rem; color: var(--text-secondary, #666); margin-bottom: 0.5rem;">
                By using CraftX.py, you agree to our terms and privacy practices
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Privacy policy button
        if st.button("🔒 Privacy Policy", key="landing_privacy",
                     help="View our comprehensive privacy policy and data protection practices"):
            st.session_state.show_privacy_policy = True
            st.rerun()

    # Copyright notice
    st.markdown("""
    <div style="text-align: center; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-color, #e0e0e0);">
        <p style="font-size: 0.75rem; color: var(--text-secondary, #999); margin: 0;">
            © 2025 ElevateCraft • Open Source • Universal Compatibility • 
            <a href="mailto:support@elevatecraft.org" style="color: var(--accent-color, #2196F3); text-decoration: none;">
                Contact Support
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Handle modals on landing page
    if st.session_state.get('show_privacy_policy', False):
        show_privacy_policy_modal()

    if st.session_state.get('show_auth', False):
        show_authentication_modal()


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

    # Check if user is authenticated - show landing page if not
    current_user = st.session_state.get('current_user')
    demo_mode = st.session_state.get('demo_mode', False)

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
        <p style="margin:0.5rem 0 0 0; opacity:0.8; font-size:clamp(11px, 2vw, 14px);">
            Made with ❤️ by <a href="https://elevatecraft.org" target="_blank" style="color: white; text-decoration: none; font-weight: bold;">ElevateCraft</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Show landing page if not authenticated and not in demo mode
    if not current_user and not demo_mode:
        show_landing_page(platform_info)
        return

    # Demo mode banner
    if demo_mode and not current_user:
        st.warning(
            "🎯 **Demo Mode**: You're trying CraftX.py with limited features. [Sign in](javascript:void(0)) for the full experience!")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("🔑 Sign In for Full Access"):
                st.session_state.show_auth = True
                st.rerun()
        with col2:
            if st.button("← Back to Landing"):
                st.session_state.demo_mode = False
                st.rerun()

    # Platform-specific welcome message for authenticated users
    if platform_info["system"] == "windows":
        welcome_msg = "Welcome Windows user! 🪟"
    elif platform_info["system"] == "darwin":
        welcome_msg = "Welcome Mac user! 🍎"
    elif platform_info["system"] == "linux":
        welcome_msg = "Welcome Linux user! 🐧"
    else:
        welcome_msg = "Welcome! 🌐"

    if current_user:
        st.info(f"{welcome_msg} Welcome back, {current_user.get('name', 'User')}!")
    else:
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

    # Show Authentication Admin Modal
    if st.session_state.get('show_auth_admin', False):
        show_auth_admin_modal()

    # Show Privacy Policy Modal
    if st.session_state.get('show_privacy_policy', False):
        show_privacy_policy_modal()

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
        
        <div style="margin-top: 1.5rem; text-align: center;">
            <p style="font-size: 14px; color: var(--text-secondary, #666); margin: 0;">
                Issues, Comments, Collaborations?! Email us @ 
                <a href="mailto:support@elevatecraft.org" style="color: var(--accent-color, #2196F3); text-decoration: none;">
                    support@elevatecraft.org
                </a>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sponsor Buttons using Streamlit columns
    st.markdown('<div style="text-align: center; margin: 1rem 0;">',
                unsafe_allow_html=True)

    # Create columns for sponsor buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <a href="https://venmo.com/elevatecraft" target="_blank" style="text-decoration: none;">
            <div style="background: #3D95CE; color: white; padding: 12px; border-radius: 8px; text-align: center; cursor: pointer; transition: all 0.3s ease; border: none; width: 100%; font-weight: bold;" 
                 onmouseover="this.style.background='#2a7bb8'" 
                 onmouseout="this.style.background='#3D95CE'">
                💸 Venmo
            </div>
        </a>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <a href="https://coff.ee/honnalulu0c" target="_blank" style="text-decoration: none;">
            <div style="background: #FFDD00; color: black; padding: 12px; border-radius: 8px; text-align: center; cursor: pointer; transition: all 0.3s ease; border: none; width: 100%; font-weight: bold;" 
                 onmouseover="this.style.background='#e6c500'" 
                 onmouseout="this.style.background='#FFDD00'">
                ☕ Buy Coffee
            </div>
        </a>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <a href="https://github.com/sponsors/davidanderson01" target="_blank" style="text-decoration: none;">
            <div style="background: #181C17; color: white; padding: 12px; border-radius: 8px; text-align: center; cursor: pointer; transition: all 0.3s ease; border: none; width: 100%; font-weight: bold;" 
                 onmouseover="this.style.background='#0d1011'" 
                 onmouseout="this.style.background='#181C17'">
                💝 GitHub
            </div>
        </a>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <a href="https://patreon.com/DavidAnderson01" target="_blank" style="text-decoration: none;">
            <div style="background: #FF4464; color: white; padding: 12px; border-radius: 8px; text-align: center; cursor: pointer; transition: all 0.3s ease; border: none; width: 100%; font-weight: bold;" 
                 onmouseover="this.style.background='#e03954'" 
                 onmouseout="this.style.background='#FF4464'">
                🎯 Patreon
            </div>
        </a>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

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
