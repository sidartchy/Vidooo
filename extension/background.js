// Background script for Vidooo extension

chrome.runtime.onInstalled.addListener((details) => {
  console.log('Vidooo extension installed');
  
  if (details.reason === 'install') {
    // First time installation
    chrome.storage.local.set({
      'vidooo_installed': true,
      'vidooo_version': '0.1.0'
    });
  }
});

// Handle extension icon click
chrome.action.onClicked.addListener((tab) => {
  if (tab.url && tab.url.includes('youtube.com/watch')) {
    // Open popup (handled by manifest)
    console.log('Vidooo popup opened for video:', tab.url);
  }
});

// Listen for tab updates to detect YouTube video pages
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url && tab.url.includes('youtube.com/watch')) {
    // Update extension icon or badge when on YouTube video
    chrome.action.setBadgeText({
      text: '●',
      tabId: tabId
    });
    
    chrome.action.setBadgeBackgroundColor({
      color: '#007bff',
      tabId: tabId
    });
  } else if (tab.url && !tab.url.includes('youtube.com/watch')) {
    // Clear badge when not on YouTube video
    chrome.action.setBadgeText({
      text: '',
      tabId: tabId
    });
  }
});
