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
  
    // При отпускании кнопки мыши после выделения текста
    document.addEventListener('mouseup', function(event) {
      var selectedText = window.getSelection().toString().trim();
  
      // Проверяем, что выделенный текст не пустой
      if (selectedText !== '') {
        // Показываем всплывающее окно рядом с выделением
        popup.style.display = 'block';
        popup.style.top = event.pageY + 'px';
        popup.style.left = event.pageX + 'px';
  
        // Устанавливаем выделенный текст во всплывающем окне
        var popupText = document.getElementById('popupText');
        popupText.textContent = selectedText;
  
        // Обработчик нажатия на кнопку "Отправить"
        var sendButton = document.getElementById('sendButton');
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
  