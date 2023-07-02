const translations = document.querySelectorAll('.translation');

// Добавление обработчика события для каждого элемента
translations.forEach(translation => {
  translation.addEventListener('click', function() {
    const currentTranslation = this.textContent;
    const parentTd = this.closest('td');
    const word = parentTd.previousElementSibling.querySelector('.word').textContent;

    this.style.display = 'none';

    const editMode = document.createElement('span');
    editMode.className = 'edit-mode';

    const editInput = document.createElement('input');
    editInput.type = 'text';
    editInput.value = currentTranslation;

    const saveButton = document.createElement('button');
    saveButton.textContent = 'Сохранить';

    const cancelButton = document.createElement('button');
    cancelButton.textContent = 'Отмена';

    editMode.appendChild(editInput);
    editMode.appendChild(saveButton);
    editMode.appendChild(cancelButton);

    parentTd.appendChild(editMode);
    editInput.focus();

    saveButton.addEventListener('click', function() {
      const newTranslation = editInput.value;

      // Отправка запроса на сервер с помощью fetch API
      fetch('/change_user_translation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          word: word,
          translation: newTranslation
        })
      })
      .then(response => response.json())
      .then(data => {
        // Обработка ответа от сервера
        console.log(data); // Пример обработки ответа
        
        translation.style.display = 'inline';
        parentTd.querySelector('.translation').textContent = newTranslation;
        editMode.remove();
      })
      .catch(error => {
        console.error('Произошла ошибка:', error);
      });
    });

    cancelButton.addEventListener('click', function() {
      translation.style.display = 'inline';
      editMode.remove();
    });
  });
});