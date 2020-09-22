var violasURL = "https://api4.violas.io"

function request(verb, partURL, obj, cb, async=true) {
    //print('request: ' + verb + ' ' + violasURL + partURL)
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if(xhr.readyState === XMLHttpRequest.DONE) {
            if(cb) {
                try {
                    //print(xhr.responseText.toString())
                    var res = JSON.parse(xhr.responseText.toString())
                    cb(res);
                } catch(err) {
                    print(partURL + ' : ' + err.message)
                }
            }
        }
    }
    xhr.open(verb, violasURL + partURL, async);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Accept', 'application/json');
    var data = obj?JSON.stringify(obj):''
    xhr.send(data)
}

function requestRate(verb, URL, obj, cb) {
    //print('request: ' + verb + ' ' + URL)
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
    xhr.send(data)
}
