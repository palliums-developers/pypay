WorkerScript.onMessage = function(msg) {
    if (msg.action = 'getBalances') {
        msg.model.clear()
        // bitcoin
        msg.model.append(
            {
                'chain': 'bitcoin',
                'name': 'BTC',
                'show_icon': "../icons/bitcoin.svg",
                'show_name': "BTC",
                'balance': msg.balance_bitcoin
            }
        )
        // libra
        if (msg.balances_libra.length == 0) {
            msg.model.append(
                {
                    'chain': 'diem',
                    'name': 'XUS',
                    'show_icon': "../icons/diem.svg",
                    'show_name': "XUS",
                    'balance': 0
                }
            )
        } else {
            for (var i=0; i<msg.balances_libra.length; i++) {
                var d = msg.balances_libra[i]
                if (d.name == 'XUS') {
                    msg.model.append(
                        {
                            'chain': 'diem',
                            'name': 'XUS',
                            'show_icon': "../icons/diem.svg",
                            'show_name': 'XUS',
                            'balance': d[d.name]
                        }
                    );
                }
            }
        }
        // violas
        if (msg.balances_violas.length == 0) {
            msg.model.append(
                {
                    'chain': 'violas',
                    'name': 'VLS',
                    'show_icon': "../icons/violas.svg",
                    'show_name': "VLS",
                    'balance': 0
                }
            )
        } else {
            for (var i=0; i<msg.balances_violas.length; i++) {
                var d = msg.balances_violas[i]
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
        msg.model.sync();
        WorkerScript.sendMessage({'action': 'update_model_tokens', 'status': 'success'})
    }
}
