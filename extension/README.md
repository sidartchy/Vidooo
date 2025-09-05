# Vidooo Browser Extension

Basic browser extension for Vidooo - Chat with YouTube videos.

## Files

- `manifest.json` - Extension configuration
- `popup.html` - Extension popup interface
- `popup.js` - Popup functionality
- `content.js` - Content script for YouTube pages
- `background.js` - Background service worker
- `styles.css` - Extension styles

## Installation

1. Open Chrome/Edge and go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension` folder

## Features

- Detects YouTube video pages
- Shows "Hi from Vidooo extension!" message
- Basic popup interface
- Visual indicator on YouTube pages

## TODO

- Connect to backend API
- Implement chat functionality
- Add video transcript fetching
- Create chat interface
