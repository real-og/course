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
})