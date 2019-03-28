$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received number" + msg.number);
        console.warn("Received number" + msg.number);
        number_string = '<h1>' + msg.number.toString() + '</h1>';
        console.log("Received number" + msg.number.toString());
        alert(msg.number.toString());
        $('#log').html(number_string);
    });

});
