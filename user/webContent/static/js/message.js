/**
 * Created by mugbya on 16-10-5.
 */

$(document).ready(function() {

    setTimeout(requestInventory, 100);

});

// function requestInventory() {
//     jQuery.getJSON('//localhost:8888/message/status', {user: $('.user').html()},
//         function(data, status, xhr) {
//             $('.message_all').html(data['sum']);
//             $('.message').html(data['unread']);
//             setTimeout(requestInventory, 0);
//         }
//     );
// }

function requestInventory() {
    var domain = window.location.hostname;
    var port = window.location.port;
    var host = 'ws://' + domain + ':' + port +'/message/status';

    var websocket = new WebSocket(host);

    websocket.onopen = function (evt) { };
    websocket.onmessage = function(evt) {
        var unread = $.parseJSON(evt.data)['unread'];
        if (unread > 0){
            var span_node = document.createElement('span');
            var a_node = $('.dropdown-toggle');

            span_node.innerHTML = '(' + unread + ')';
            a_node.append(span_node);
        }


        var message = $.parseJSON(evt.data)['message'];
        var ul_node = $('.dropdown-menu');
        var li_node = document.createElement('li');

        if(message['status'] != 0){
           li_node.innerHTML = '<div class="message-line">' + message['username'] + '评论了你的博客'
                + '<a href="/blog/' + message['eventSource']+ '?message=' + message['id']+ '">' + message['data'] + '</a></div>';
        }else {
           li_node.innerHTML = '<div class="message-line-brown">' + message['username'] + '评论了你的博客'
                + '<a href="/blog/' + message['eventSource']+ '?message=' + message['id']+ '">' + message['data'] + '</a></div>';
        }

        ul_node.prepend(li_node);

    };
    websocket.onerror = function (evt) { };
}