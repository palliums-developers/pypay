import "ViolasServer.js" as violasServer

WorkerScript.onMessage = function(msg) {
    if (msg.action = 'getBalances') {
        msg.model.clear();
        violasServer.request('GET', '/1.0/violas/balance?addr='+msg.violasAddr, null, function(resp) {
            if (resp.code == 2000) {
                var entries = resp.data.balances;
                for (var i=0; i<entries.length; i++) {
                    msg.model.append(entries[i]);
                }
            }
        }, false);
        violasServer.request('GET', '/1.0/libra/balance?addr='+payController.libraAddr, null, function(resp) {
            if (resp.code == 2000) {
                var entries = resp.data.balances;
                for (var i=0; i<entries.length; i++) {
                    msg.model.append(entries[i]);
                }
            }
        }, false);
        msg.model.sync();
    }
}
