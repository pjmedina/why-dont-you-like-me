$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    socket.on('newnumber',function(msg) {
        const numberElement = document.getElementById('log');
        numberElement.innerHTML = '';
        numberElement.innerHTML = msg.number;
    });


});
