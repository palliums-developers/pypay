WorkerScript.onMessage = function(msg) {
    if (msg.action = 'getBalances') {
        msg.model.clear();
        request('GET', 'https://api4.violas.io/1.0/violas/balance?addr='+msg.violasAddr, null, function(resp) {
            if (resp.code == 2000) {
                var entries = resp.data.balances;
                for (var i=0; i<entries.length; i++) {
                    msg.model.append(entries[i]);
                }
            }
        });
        request('GET', 'https://api4.violas.io/1.0/libra/balance?addr='+msg.libraAddr, null, function(resp) {
            if (resp.code == 2000) {
                var entries = resp.data.balances;
                for (var i=0; i<entries.length; i++) {
                    msg.model.append(entries[i]);
                }
            }
        });
        msg.model.sync();
    }
}

function request(verb, URL, obj, cb) {
    //print('request: ' + verb + ' ' + URL)
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if(xhr.readyState === XMLHttpRequest.DONE) {
            if(cb) {
                try {
                    //print(xhr.responseText.toString())
                    var res = JSON.parse(xhr.responseText.toString())
                    cb(res);
                } catch(err) {
                    print(URL + ' : ' + err.message)
                }
            }
        }
    }
    xhr.open(verb, URL, false);
    xhr.timeout = 2000
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Accept', 'application/json');
    var data = obj?JSON.stringify(obj):''
    xhr.send(data)
}
