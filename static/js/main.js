
$('#button-addon1').on('click',function(){
    var key = $('#myroom').val().toLowerCase();
    window.location.href =  location.protocol+'//' + document.domain + ':' + location.port + '/' + key;
});
$('#myroom').keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
        var key = $('#myroom').val().toLowerCase();
        window.location.href = location.protocol+'//' + document.domain + ':' + location.port + '/' + key;
        
    }
});
