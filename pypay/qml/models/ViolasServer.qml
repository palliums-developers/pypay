import QtQuick 2.15

Item {
    id: root

    property string baseURL: "https://api4.violas.io"

    function request(verb, partURL, obj, cb) {
        print('request: ' + verb + ' ' + baseURL + partURL)
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            print('xhr: on ready state change: ' + xhr.readyState)
            if(xhr.readyState === XMLHttpRequest.DONE) {
                if(cb) {
                    var res = JSON.parse(xhr.responseText.toString())
                    cb(res);
                }
            }
        }
        xhr.open(verb, baseURL + partURL);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('Accept', 'application/json');
        var data = obj?JSON.stringify(obj):''
        xhr.send(data)
    }
}
