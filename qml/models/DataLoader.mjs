//var violasURL = "https://api4.violas.io"
var violasURL = "http://localhost:5000"

function request(verb, URL, obj, cb, async=true) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if(xhr.readyState === XMLHttpRequest.DONE) {
            if(cb) {
                try {
                    print('request: ' + verb + ' ' + URL)
                    //print(xhr.responseText.toString())
                    var res = JSON.parse(xhr.responseText.toString())
                    cb(res);
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

WorkerScript.onMessage = function(msg) {
    if (msg.action = 'getBalances') {
        msg.model.clear();
        // bitcoin
        msg.model.append(
            {
                'chain': 'bitcoin',
                'name': 'BTC',
                'show_icon': "../icons/bitcoin.svg",
                'show_name': "BTC",
                'balance': 0
            }
        )
        
        // libra
        request('GET', violasURL + '/1.0/libra/balance?addr=' + msg.libraAddr, null, function(resp) {
            if (resp.code == 2000) {
                var entries = resp.data.balances;
                for (var i=0; i<entries.length; i++) {
                    var d = entries[i]
                    if (d.name != 'Coin1' && d.name != 'Coin2') {
                        msg.model.append(
                            {
                                'chain': 'libra',
                                'name': d.name,
                                'show_icon': "../icons/libra.svg",
                                'show_name': d.show_name,
                                'balance': d[d.name]
                            }
                        );
                    }
                }
            }
        }, false);

        // violas
        request('GET', violasURL + '/1.0/violas/balance?addr=' + msg.violasAddr, null, function(resp) {
            if (resp.code == 2000) {
                var entries = resp.data.balances;
                for (var i=0; i<entries.length; i++) {
                    var d = entries[i]
                    msg.model.append(
                        {
                            'chain': 'violas',
                            'name': d.name,
                            'show_icon': "../icons/violas.svg",
                            'show_name': d.show_name,
                            'balance': d[d.name]
                        }
                    );
                }
            }
        }, false);
        msg.model.sync();
    }
}
