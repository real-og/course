const form = document.getElementById('avatar-form');
const input = document.getElementById('avatar-input');

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
    // Обработка успешной загрузки аватарки
  })
  .catch(error => {
    // Обработка ошибки загрузки аватарки
  });
});
