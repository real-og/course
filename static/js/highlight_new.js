isHighLighted = false;

function highlightText() {

    var textContainer = document.getElementById("textContainer");
    var text = textContainer.innerText;

    fetch("/get_unknown", {
        method: "POST",
        headers: {
          "Content-Type": "text/plain;charset=UTF-8"
        },
        body: text
      })
        .then(response => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error("Произошла ошибка при отправке текста на сервер.");
          }
        })
        .then(data => {
            var highlightedWords = data.highlightedWords;


            var words = textContainer.querySelectorAll("b");
            if (isHighLighted) {
                var button = document.getElementById("highlightUnknown"); // Или другой селектор, например: document.querySelector(".myButton")
                button.textContent = "Подсветить незнакомое";

                var elements = document.querySelectorAll(".highlight");
                for (var i = 0; i < elements.length; i++) {
                    elements[i].classList.remove("highlight");
                }
                isHighLighted = false;

            } else {

                var button = document.getElementById("highlightUnknown"); // Или другой селектор, например: document.querySelector(".myButton")
                button.textContent = "Убрать выделение";

                words.forEach(function(wordElement) {
                    var word = wordElement.innerHTML;
                    if (highlightedWords.includes(word.toLowerCase().replace("$", 's').replace(/[^\w\s'-]/g, '').replace("'", '’'))) {
                        wordElement.classList.add("highlight");
                    }
                });
                isHighLighted = true;
            }
        })
      .catch(error => {
        console.error("Произошла ошибка:", error);
      });
  }

