$(document).ready(function(){

    $('.lyrics').on('click', 'b', function(){
        
        $.ajax({
            url: '/add/',
            type: 'post',
            contentType: 'application/json',
            data: JSON.stringify({
                text: $(this).text()
            }),
         
            succcess: function(responce){
                console.log(responce);
            
            }
        });
        $(this).toggleClass('high') ;
    })
    $('.dlt-row').on('click', 'b', function(){
        
        $.ajax({
            url: '/delete/',
            type: 'post',
            contentType: 'application/json',
            data: JSON.stringify({
                text: $(this).parent().prev().prev().text()
            }),
         
            succcess: function(responce){
                console.log(responce);
            
            }
        });
        $(this).text('удалено') ;
        $(this).parent().parent().hide();
    })
})

document.addEventListener('DOMContentLoaded', function() {
    // Получаем ссылку на всплывающее окно
    var popup = document.getElementById('popup');
    var sendButton = document.getElementById('sendButton');
  
    // При отпускании кнопки мыши после выделения текста
    document.addEventListener('mouseup', function(event) {
      var selectedText = window.getSelection().toString().trim();
  






      // Проверяем, что выделенный текст не пустой
      if (selectedText !== '') {
        // Получаем объект Range для выделения
        var selectionRange = window.getSelection().getRangeAt(0);
  
        // Получаем прямоугольник выделения
        var selectionRect = selectionRange.getBoundingClientRect();
  
        // Получаем позицию прокрутки окна
        var scrollY = window.scrollY || window.pageYOffset;
  
        // Показываем всплывающее окно рядом с выделением
        popup.style.display = 'block';
  
        // Проверяем, есть ли достаточно места сверху для отображения окна
        var spaceAbove = selectionRect.top - popup.offsetHeight;
  
        if (spaceAbove > 0) {
          // Если есть место сверху, отображаем окно над выделением
          popup.style.top = (selectionRect.top + scrollY - popup.offsetHeight) + 'px';
        } else {
          // Если места сверху недостаточно, отображаем окно под выделением
          popup.style.top = (selectionRect.top + scrollY + selectionRect.height) + 'px';
        }
  
        popup.style.left = selectionRect.left + 'px';
        popup.style.width = Math.max(selectionRect.width, sendButton.offsetWidth + sendButton.width) + 'px';
  









        // Устанавливаем выделенный текст во всплывающем окне
        var popupText = document.getElementById('popupText');
        popupText.textContent = selectedText;
  
        // Обработчик нажатия на кнопку "Отправить"
        
        sendButton.style.display = 'block';
        sendButton.onclick = function() {
          // Отображаем текст "Одну минуту..." во время ожидания
          popupText.textContent = 'Одну минуту...';
          sendButton.style.display = 'none';
          // Формируем объект с выделенным текстом
          var data = {
            selectedText: selectedText
          };
  
          // Отправляем POST-запрос на сервер с выделенным текстом в формате JSON
          var xhr = new XMLHttpRequest();
          xhr.open('POST', '/get_explaination', true);
          xhr.setRequestHeader('Content-Type', 'application/json');
  
          xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
              // При получении ответа от сервера
              popupText.textContent = xhr.responseText; // Отображаем ответ от сервера
            }
          };
  
          xhr.send(JSON.stringify(data));
        };
      } else {
        // Если выделение пустое, скрываем всплывающее окно
        popup.style.display = 'none';
      }
    });
  });
  