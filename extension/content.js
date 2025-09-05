// Content script for Vidooo extension

console.log('Vidooo extension loaded on YouTube');

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getVideoInfo') {
    const videoInfo = getVideoInfo();
    sendResponse(videoInfo);
  }
});

function getVideoInfo() {
  // Extract video information from YouTube page
  const videoId = extractVideoId(window.location.href);
  const title = document.querySelector('h1.ytd-video-primary-info-renderer')?.textContent?.trim();
  const channel = document.querySelector('#channel-name a')?.textContent?.trim();
  
  return {
    videoId: videoId,
    title: title || 'Unknown Title',
    channel: channel || 'Unknown Channel',
    url: window.location.href
  };
}

function extractVideoId(url) {
  const regex = /(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)/;
  const match = url.match(regex);
  return match ? match[1] : null;
}

// Add a small indicator that extension is active
function addExtensionIndicator() {
  const indicator = document.createElement('div');
  indicator.id = 'vidooo-indicator';
  indicator.style.cssText = `
    position: fixed;
    top: 10px;
    right: 10px;
    background: #007bff;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-family: Arial, sans-serif;
    z-index: 10000;
    opacity: 0.8;
  `;
  indicator.textContent = 'Vidooo';
  document.body.appendChild(indicator);
  
  // Remove indicator after 3 seconds
  setTimeout(() => {
    if (indicator.parentNode) {
      indicator.parentNode.removeChild(indicator);
    }
  }, 3000);
}

// Add indicator when page loads
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', addExtensionIndicator);
} else {
  addExtensionIndicator();
}
