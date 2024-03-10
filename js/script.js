const listenButton = document.getElementById('listenButton');
const responseDiv = document.getElementById('response');

listenButton.addEventListener('click', async () => {
  // Simulate voice input by making an API call to your python backend
  // This part requires further implementation based on your backend setup
  const response = await fetch('/api/listen');
  const text = await response.text();
  responseDiv.textContent = text;
});
