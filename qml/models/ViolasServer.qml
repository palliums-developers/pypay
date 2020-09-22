import QtQuick 2.15

Item {
    id: root

    property string violasURL: "https://api4.violas.io"

    function request(verb, partURL, obj, cb) {
        print('request: ' + verb + ' ' + violasURL + partURL)
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if(xhr.readyState === XMLHttpRequest.DONE) {
                if(cb) {
                    //print(xhr.responseText.toString())
                    var res = JSON.parse(xhr.responseText.toString())
                    cb(res);
                }
            }
        }
        xhr.open(verb, violasURL + partURL);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('Accept', 'application/json');
        var data = obj?JSON.stringify(obj):''
        if (obj) {
            print(data)
        }
        xhr.send(data)
    }

    function requestRate(verb, URL, obj, cb) {
        print('request: ' + verb + ' ' + URL)
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if(xhr.readyState === XMLHttpRequest.DONE) {
                if(cb) {
                    var res = JSON.parse(xhr.responseText.toString())
                    cb(res);
                }
            }
        }
        xhr.open(verb, URL);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('Accept', 'application/json');
        var data = obj?JSON.stringify(obj):''
        if (obj) {
            print(data)
        }
        xhr.send(data)
    }
}
