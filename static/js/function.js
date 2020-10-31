var username = null;
var status = true;
var room = window.location.pathname;
if(room == '/'){
    console.log('No Room Provided');
}
else{
    room = room.toLowerCase().substring(1,);
    $("#room-name").html(room[0].toUpperCase()+room.substring(1,12));
}

console.log('Entered Room -> ',room);

var socket = io.connect(location.protocol+'//' + document.domain + ':' + location.port);
socket.on('connect',function(){
    if(username == null){
        username = prompt("What's your name?");
        if(username == null){
            username = 'Anonymous';
        }
    };
    var data = {
        "username": username,
        "room": room,
        "new": status
    };
    socket.emit('join' , data);
    status = false;
    
});

// socket.on('disconnect',function(){
//     notie.alert({ type: 'warning', text: '<b>'+username+'</b> : Disconnected From Server  Trying Again ... </p>', time: 3 });

// });

socket.on('message',function(msg){
    $("#messages").append('<p class = ><b>'+msg.user+'</b> : '+msg.message+' <span class="time-span">'+msg.time+'</span></p>');

});

socket.on('alert',function(msg){
    notie.alert({ type: msg.class, text: '<b>'+msg.user+'</b> : '+msg.message+' <span class="time-span">'+msg.time+'</span>', time: 3 });
    $('#mymessage').focus();
});
$('#button-addon1').on('click',function(){
    var data = {
        "user": username,
        "message": $('#mymessage').val(),
        "room": room
    };
    if(socket.connected){
        socket.emit('message' , data) ;
        $('#mymessage').val('');
    }
    else{
        notie.alert({ type: 'warning', text: '<b>'+msg.user+'</b> : Not Connected Right Now...<br> Refresh or Try again Later.. <span class="time-span">('+msg.time+')</span>', time: 3 });
        $('#mymessage').focus();
    }
    
});
$('#mymessage').keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
        var data = {
        "user": username,
        "message": $('#mymessage').val(),
        "room": room
        };
        // console.log('its now working here');
        if(socket.connected){
            socket.emit('message' , data) ;
            $('#mymessage').val('');
        }
        else{
            notie.alert({ type: 'warning', text: '<b>'+msg.user+'</b> : Not Connected Right Now... Refresh or Try again Later.. <span class="time-span">('+msg.time+')</span>', time: 3 });
            $('#mymessage').focus();
        }
    }
});

$(window).bind("beforeunload", function(){
        var data = {
        "username": username,
        "room": room
    }
    socket.emit('leave',data);
});

