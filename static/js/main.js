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


