//var violasURL = "https://api4.violas.io"
var violasURL = "http://localhost:5000"

function request(verb, URL, obj, cb, async=true) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if(xhr.readyState === XMLHttpRequest.DONE) {
            if(cb) {
                try {
                    print('request: ' + verb + ' ' + URL)
                    if (xhr.status == 200) {
                        print(xhr.responseText.toString())
                        var res = JSON.parse(xhr.responseText.toString())
                        cb(res);
                    } else {
                        print(xhr.statusText)
                    }
                } catch(err) {
                    print(URL + ' : ' + err.message)
                }
            }
        }
    }
    xhr.open(verb, URL, async);
    xhr.timeout = 2000
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Accept', 'application/json');
    var data = obj?JSON.stringify(obj):''
    xhr.send(data)
}

function formatParams(params) {
    return "?" + Object.keys(params).map(function(key) {
            return key + "=" + params[key]
        }).join("&")
}
