// Popup script for Vidooo extension

document.addEventListener('DOMContentLoaded', function() {
  const statusDiv = document.getElementById('status');
  const chatButton = document.getElementById('chatButton');
  
  // Check if we're on a YouTube video page
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    const currentTab = tabs[0];
    
    if (currentTab.url && currentTab.url.includes('youtube.com/watch')) {
      // Extract video ID from URL
      const videoId = extractVideoId(currentTab.url);
      
      if (videoId) {
        statusDiv.innerHTML = `
          <p><strong>Video detected!</strong></p>
          <p>Ready to chat with this video.</p>
        `;
        chatButton.disabled = false;
        chatButton.textContent = 'Start Chatting';
        
        chatButton.addEventListener('click', function() {
          // TODO: Implement chat functionality
          alert('Chat feature coming soon!');
        });
      } else {
        statusDiv.innerHTML = `
          <p>Not a valid YouTube video page.</p>
        `;
      }
    } else {
      statusDiv.innerHTML = `
        <p>Please navigate to a YouTube video.</p>
      `;
    }
  });
});

function extractVideoId(url) {
  const regex = /(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)/;
  const match = url.match(regex);
  return match ? match[1] : null;
}
