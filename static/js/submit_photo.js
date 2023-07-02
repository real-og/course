const form = document.getElementById('avatar-form');
const input = document.getElementById('avatar-input');

function reloadPageAfterDelay(delay) {
    setTimeout(function() {
        location.reload();
    }, delay);
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  
  const file = input.files[0];
  const formData = new FormData();
  formData.append('avatar', file);
  
  fetch('/upload-avatar', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    reloadPageAfterDelay(1000);
    // Обработка успешной загрузки аватарки
  })
  .catch(error => {
    // Обработка ошибки загрузки аватарки
  });
  reloadPageAfterDelay(1000);
});
