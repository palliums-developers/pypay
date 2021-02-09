// Violas back server interface file.
import QtQuick 2.15

Item {
    property var url_violas: "https://api4.violas.io"   // 内部测试链
    //property var url_violas: "http://localhost:5000"
    property var data_dir: payController.data_dir
    property var system_locale_name: payController.system_locale_name
    property var mnemonic: ""
    property var mnemonic_random: ""
    property var address_bitcoin: ""
    property var address_libra: ""
    property var address_violas: ""
    property var balance_bitcoin: 0 // BTC
    property var balances_libra: []
    property var balances_violas: []
    property var value_bitcoin: 0
    property var values_violas: {'VLS':0, 'GNIUSD':0, 'NEOUSD':0, 'PAMUSD':0, 'VBUSD':0, 'VHUSD':0, 'VLSUSD':0, 'VUSDC':0, 'vBTC':47965.534999999916, 'vUSDT':1, 'vWBTC':0}
    property var value_total: 0
    property var rates: {}
    property var currencies_published: []
    property var violas_transaction_detail: {}

    property var account_bank: {
        "amount": 0.0,
        "borrow": 0.0,
        "total": 0.0,
        "yesterday": 0.0
    }
    property var deposit_bank: {
        "id": "",
        "intor": [],
        "logo": "",
        "minimum_amount": 0,
        "minimum_step": 0,
        "name": "",
        "pledge_rate": 0,
        "question": [],
        "quota_limit": 0,
        "quota_used": 0,
        "rate": 0,
        "rate_desc": "",
        "token_address": "",
        "token_module": "",
        "token_name": "",
        "token_show_name": ""
    }
    property var borrow_bank: {
        "id": "",
        "intor": [],
        "logo": "",
        "minimum_amount": 0,
        "minimum_step": 0,
        "name": "",
        "pledge_rate": 0.0,
        "question": [],
        "quota_limit": 0,
        "quota_used": 0,
        "rate": 0.0,
        "token_address": "",
        "token_module": "",
        "token_name": "",
        "token_show_name": ""
    }
    property string id_requested_bank: ""
    property var token_requested_wallet: {
        'chain': 'bitcoin',
        'name': 'BTC',
        'show_icon': "../icons/bitcoin.svg",
        'show_name': 'BTC',
        'balance': 0
    }
    
    property var incentive_top20

    property alias model_tokens: model_tokens
    property alias model_currencies: model_currencies
    property alias model_history: model_history
    property alias model_address_book: model_address_book
    property alias model_products_deposit: model_products_deposit
    property alias model_products_borrow: model_products_borrow
    property alias model_intors: model_intors
    property alias model_questions: model_questions
    property alias model_orders_deposit: model_orders_deposit
    property alias model_details_order_deposit: model_details_order_deposit
    property alias model_orders_borrow: model_orders_borrow
    property alias model_details_order_borrow: model_details_order_borrow

    ListModel {
        id: model_tokens
    }
    ListModel {
        id: model_currencies
        ListElement {
            chain: "bitcoin"
            name: "BTC"
            show_name: "BTC"
            show_icon: "../icons/bitcoin.svg"
        }
        ListElement {
            chain: "diem"
            name: "XUS"
            show_name: "XUS"
            show_icon: "../icons/diem.svg"
        }
        ListElement {
            chain: "violas"
            name: "VLS"
            show_name: "VLS"
            show_icon: "../icons/violas.svg"
        }
    }
    ListModel {
        id: model_history
    }
    ListModel {
        id: model_address_book
    }
    ListModel {
        id: model_products_deposit
    }
    ListModel {
        id: model_products_borrow
    }
    ListModel {
        id: model_intors
    }
    ListModel {
        id: model_questions
    }
    ListModel {
        id: model_orders_deposit
    }
    ListModel {
        id: model_details_order_deposit
    }
    ListModel {
        id: model_orders_borrow
    }
    ListModel {
        id: model_details_order_borrow
    }

    Timer {
        id: timer
        interval: 5000
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: {
            if (appSettings.walletIsCreate) {
                var params_libra = { "addr": address_libra , "currency": "XUS" }
                get_balance_libra(params_libra)
                var params_violas = { "addr": address_violas }
                get_currencies_published(params_violas)
                get_balance_violas(params_violas, function() {
                    update_model_tokens()
                })
                get_account_bank(params_violas)
            }
        }
    }

    WorkerScript {
        id: worker
        source: "ViolasWorkerScript.mjs"
        onMessage: {
            if (messageObject.action == 'result_update_model_tokens') {
                var value_tmp = 0
                for (var i = 0; i < model_tokens.count; i++) {
                    var chain = model_tokens.get(i).chain
                    var show_name = model_tokens.get(i).show_name
                    var balance = model_tokens.get(i).balance
                    if (appWindow.currencies_show.includes(show_name)) {
                        value_tmp += get_rate(chain, show_name) * format_balance(chain, balance)
                    }
                }
                value_total = value_tmp
            }
        }
    }

    Connections {
        target: payController
        function onChanged_data_dir() {
            data_dir = payController.data_dir
        }
        function onChanged_system_locale_name() {
            system_locale_name = payController.system_locale_name
        }
        function onChanged_address_bitcoin() {
            address_bitcoin = payController.address_bitcoin
            console.log("bitcoin address: ", address_bitcoin)
        }
        function onChanged_address_libra() {
            address_libra = payController.address_libra
            console.log("diem address: ", address_libra)
            console.log("diem key_prefix_hex: ", payController.key_prefix_hex_libra)
            if (appSettings.walletIsCreate == false) {
                var params = { 
                    "address": address_libra, 
                    "auth_key_perfix": payController.key_prefix_hex_libra, 
                    "currency": "XUS",
                }
                get_libra_mint(params)
            }
        }
        function onChanged_address_violas() {
            address_violas = payController.address_violas
            var params = { "address": address_violas }
            get_value_violas(params)
            console.log("violas address: ", address_violas)
            console.log("violas key_prefix_hex: ", payController.key_prefix_hex_violas)
            if (appSettings.walletIsCreate == false) {
                var params = { 
                    "address": address_violas ,
                    "auth_key_perfix": payController.key_prefix_hex_violas,
                    "currency": "VLS",
                }
                get_violas_mint(params)
            }
        }
        function onChanged_mnemonic() {
            mnemonic = payController.mnemonic
        }
        function onChanged_mnemonic_random() {
            mnemonic_random = payController.mnemonic_random
        }
    }

    Component.onCompleted: {
        get_value_bitcoin()
        get_currencies_libra()
        get_currencies_violas()
        get_products_deposit()
        get_products_borrow()
        update_model_tokens()
    }

    function formatParams(params) {
        return "?" + Object.keys(params).map(function(key) {
            return key + "=" + params[key]
        }).join("&")
    }

    function request(verb, url, obj, cb, async=true) {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if(xhr.readyState === XMLHttpRequest.DONE) {
                if(cb) {
                    try {
                        print('request: ' + verb + ' ' + url)
                        if (xhr.status == 200) {
                            //print(xhr.responseText.toString())
                            var res = JSON.parse(xhr.responseText.toString())
                            cb(res);
                        } else {
                            print(xhr.statusText)
                        }
                    } catch(err) {
                        print(url + ' : ' + err.message)
                    }
                }
            }
        }
        xhr.open(verb, url, async);
        xhr.timeout = 3000
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('Accept', 'application/json');
        var data = obj?JSON.stringify(obj):''
        xhr.send(data)
    }

    function get_rates() {
        request('GET', 'https://api.exchangeratesapi.io/latest?base=USD', null, function(resp) {
            rates = resp.rates;
        });
    }

    function get_libra_mint(params) {
        request('GET', url_violas + '/1.0/libra/mint' + formatParams(params), null, 
            function(resp) {
                if (resp.code == 2000) {
                    console.log("diem account actived")
                }
            });
    }

    function get_violas_mint(params) {
        request('GET', url_violas + '/1.0/violas/mint' + formatParams(params), null, 
            function(resp) {
                if (resp.code == 2000) {
                    console.log("violas account actived")
                }
            });
    }

    function get_value_bitcoin() {
        request('GET', url_violas + '/1.0/violas/value/btc', null, 
            function(resp) {
                if (resp.code == 2000) {
                    value_bitcoin = resp.data[0]["rate"]
                }
            });
    }

    function get_value_violas(params) {
        request('GET', url_violas + '/1.0/violas/value/violas' + formatParams(params), null, 
            function(resp) {
                if (resp.code == 2000) {
                    var entries = resp.data
                    for (var i=0; i<entries.length; i++) {
                        values_violas[entries[i].name] = entries[i].rate
                    }
                    //console.log(JSON.stringify(values_violas))
                }
            });
    }

    function get_balance_libra(params) {
        request('GET', url_violas + '/1.0/libra/balance' + formatParams(params), null, function(resp) {
            if (resp.code == 2000) {
                balances_libra = resp.data["balances"]
            }
        });
    }

    function get_balance_violas(params, cb) {
        request('GET', url_violas + '/1.0/violas/balance' + formatParams(params), null, function(resp) {
            if (resp.code == 2000) {
                balances_violas = resp.data["balances"]
            }
            if (cb) {
                cb()
            }
        });
    }

    function get_currencies_published(params) {
        request('GET', url_violas + '/1.0/violas/currency/published' + formatParams(params), null, function(resp) {
            if (resp.code == 2000) {
                currencies_published = resp.data.published
            }
        });
    }

    function get_currencies_libra() {
        request('GET', url_violas + '/1.0/libra/currency', null, function(resp) {
            if (resp.code == 2000) {
                var entries = resp.data.currencies;
                for (var i=0; i<entries.length; i++) {
                    if (entries[i].show_name != "XUS" && entries[i].name != "XDX") {
                        var d = entries[i]
                        model_currencies.append(
                            {
                                "chain": "diem",
                                "name": d.name,
                                "show_name": d.show_name,
                                "show_icon": "../icons/diem.svg"
                            }
                        )
                    }
                }
            }
        });
    }

    function get_currencies_violas() {
        request('GET', url_violas + '/1.0/violas/currency', null, function(resp) {
            if (resp.code == 2000) {
                var entries = resp.data.currencies;
                for (var i=0; i<entries.length; i++) {
                    if (entries[i].show_name != "VLS" && entries[i].name != "XUS" && entries[i].name != "XDX") {
                        var d = entries[i]
                        model_currencies.append(
                            {
                                "chain": "violas",
                                "name": d.name,
                                "show_name": d.show_name,
                                "show_icon": "../icons/violas.svg"
                            }
                        )
                    }
                }
            }
        });
    }

    function get_history_violas(params) {
        model_history.clear()
        request('GET', url_violas + '/1.0/violas/transaction' + formatParams(params), null, function(resp) {
            if (resp.code == 2000) {
                var entries = resp.data;
                for (var i=0; i<entries.length; i++) {
                    var d = entries[i]
                    model_history.append(
                        {
                            "amount": d.amount,
                            "confirmed_time": d.confirmed_time,
                            "currency": d.currency,
                            "expiration_time": d.expiration_time, 
                            "gas": d.gas,
                            "gas_currency": d.gas_currency,
                            "receiver": d.receiver == null ? "" : d.receiver,
                            "sender": d.sender == null ? "" : d.sender,
                            "sequence_number": d.sequence_number,
                            "status": d.status,
                            "type": d.type,
                            "version": d.version
                        }
                    )
                }
            }
        });
    }

    function get_account_bank(params) {
        request('GET', url_violas + '/1.0/violas/bank/account/info' + formatParams(params), null, function(resp) {
            account_bank = resp.data;
        });
    }

    function get_products_deposit() {
        request('GET', url_violas + '/1.0/violas/bank/product/deposit', null, function(resp) {
            var entries = resp.data;
            model_products_deposit.clear()
            for (var i=0; i<entries.length; i++) {
                model_products_deposit.append(entries[i])
            }
        });
    }

    function get_products_borrow() {
        request('GET', url_violas + '/1.0/violas/bank/product/borrow', null, function(resp) {
            var entries = resp.data;
            model_products_borrow.clear()
            for (var i=0; i<entries.length; i++) {
                model_products_borrow.append(entries[i])
            }
       });
    }

    function get_deposit_bank(params, cb) {
        request('GET', url_violas + '/1.0/violas/bank/deposit/info' + formatParams(params), null, function(resp) {
            deposit_bank = resp.data;
            model_intors.clear()
            for (var i=0; i<resp.data.intor.length; i++) {
                model_intors.append({"title":resp.data.intor[i].title, "content":resp.data.intor[i].text})
            }
            model_questions.clear()
            for (var i=0; i<resp.data.question.length; i++) {
                model_questions.append({"title":resp.data.question[i].title, "content":resp.data.question[i].text})
            }
            if (cb) {
                cb()
            }
        });
    }

    function get_borrow_bank(params, cb) {
        request('GET', url_violas + '/1.0/violas/bank/borrow/info' + formatParams(params), null, function(resp) {
            borrow_bank = resp.data;
            model_intors.clear()
            for (var i=0; i<resp.data.intor.length; i++) {
                model_intors.append({"title":resp.data.intor[i].title, "content":resp.data.intor[i].text})
            }
            model_questions.clear()
            for (var i=0; i<resp.data.question.length; i++) {
                model_questions.append({"title":resp.data.question[i].title, "content":resp.data.question[i].text})
            }
            if (cb) {
                cb()
            }
        });
    }

    function get_orders_deposit(params, cb) {
        request('GET', url_violas + '/1.0/violas/bank/deposit/orders' + formatParams(params), null, function(resp) {
            model_orders_deposit.clear()
            for (var i=0; i<resp.data.length;i++) {
                var d = resp.data[i]
                model_orders_deposit.append({
                    "currency": d.currency,
                    "earnings": d.earnings,
                    "orderId": d.id,
                    "logo": d.logo,
                    "principal": d.principal,
                    "rate": d.rate,
                    "status": d.status,
                    "total_count": d.total_count
                    })                   
            }
            if (cb) {
                cb()
            }
        });
    }

    function get_details_order_deposit(params, cb) {
        request('GET', url_violas + '/1.0/violas/bank/deposit/order/list' + formatParams(params), null, 
            function(resp) {
            model_details_order_deposit.clear()
            for (var i=0; i<resp.data.length;i++) {
                var d = resp.data[i]
                model_details_order_deposit.append({
                    'currency': d.currency,
                    'date': d.date,
                    'orderId': d.id,
                    'logo': d.logo,
                    'status': d.status,
                    'value': d.value,
                    'total_count': d.total_count
                    })
            }
            if (cb) {
                cb()
            }
        });
    }

    function get_orders_borrow(params, cb) {
        request('GET', url_violas + '/1.0/violas/bank/borrow/orders' + formatParams(params), null, function(resp) {
            model_orders_borrow.clear()
            for (var i=0; i<resp.data.length;i++) {
                var d = resp.data[i]
                model_orders_borrow.append({
                    'amount': d.amount,
                    'orderId': d.id,
                    'logo': d.logo,
                    'name': d.name,
                    'available_borrow': d.available_borrow,
                    'total_count': d.total_count
                    })
            }
            if (cb) {
                cb()
            }
        });
    }

    function get_details_order_borrow(params, cb) {
        request('GET', url_violas + '/1.0/violas/bank/borrow/order/list' + formatParams(params), null, function(resp) {
            model_details_order_borrow.clear()
            for (var i=0; i<resp.data.length;i++) {
                var d = resp.data[i]
                model_details_order_borrow.append({
                    'currency': d.currency,
                    'date': d.date,
                    'orderId': d.id,
                    'logo': d.logo,
                    'status': d.status,
                    'value': d.value,
                    'total_count': d.total_count
                    })
            }
            if (cb) {
                cb()
            }
        });
    }

    ///

    // /1.0/violas/incentive/mobile/verify
    function incentive_mobile_verify(params, cb) {
        request('GET', url_violas + '/1.0/violas/incentive/mobile/verify' + formatParams(params), null, function(resp) {
            if (cb) {
                cb()
            }
        });
    }

    // /1.0/violas/incentive/inviter/info
    function incentive_inviter_info(params, cb) {
        request('GET', url_violas + '/1.0/violas/incentive/inviter/info' + formatParams(params), null, function(resp) {
            
            if (cb) {
                cb()
            }
        });
    }

    // /1.0/violas/incentive/inviter/top20
    function incentive_inviter_top20(params, cb) {
        request('GET', url_violas + '/1.0/violas/incentive/inviter/top20' + formatParams(params), null, function(resp) {
            
            if (cb) {
                cb()
            }
        });
    }

    // /1.0/violas/incentive/check/verified
    function incentive_check_verified(params, cb) {
        request('GET', url_violas + '/1.0/violas/incentive/check/verified' + formatParams(params), null, function(resp) {
            
            if (cb) {
                cb()
            }
        });
    }

    // /1.0/violas/incentive/orders/invite
    function incentive_orders_invite(params, cb) {
        request('GET', url_violas + '/1.0/violas/incentive/orders/invite' + formatParams(params), null, function(resp) {
            
            if (cb) {
                cb()
            }
        });
    }

    // /1.0/violas/incentive/orders/pool
    function incentive_orders_pool(params, cb) {
        request('GET', url_violas + '/1.0/violas/incentive/orders/pool' + formatParams(params), null, function(resp) {
            
            if (cb) {
                cb()
            }
        });
    }

    // /violas/1.0/incentive/orders/bank
    function incentive_orders_bank(params, cb) {
        request('GET', url_violas + '/1.0/violas/incentive/orders/bank' + formatParams(params), null, function(resp) {
            
            if (cb) {
                cb()
            }
        });
    }

    // /violas/1.0/incentive/mint/info
    function incentive_mint_info(params, cb) {
        request('GET', url_violas + '/1.0/violas/incentive/mint/info' + formatParams(params), null, function(resp) {
            
            if (cb) {
                cb()
            }
        });
    }

    // /violas/1.0/incentive/top20
    function incentive_top20(params, cb) {
        request('GET', url_violas + '/1.0/violas/incentive/top20' + formatParams(params), null, function(resp) {
            
            if (cb) {
                cb()
            }
        });
    }

    ////////////////////////////////

    function format_timestamp(timestamp) {    // timestamp 秒
        var ptDate = new Date(timestamp*1000)
        return ptDate.toLocaleString(Qt.locale("de_DE"), "yyyy-MM-dd HH:mm:ss    ")
    }

    function update_model_tokens() {
        var msg = {
            'action': 'request_update_model_tokens',
            'balance_bitcoin': balance_bitcoin,
            'balances_libra': balances_libra,
            'balances_violas': balances_violas,
            'model': model_tokens
        };
        worker.sendMessage(msg);
    }

    function get_rate(chain, token) {
        if (chain == "bitcoin") {
            return value_bitcoin
        } else if (token == "VLS" || token == "XUS") {
            return 0
        } else {
            return values_violas[token]
        }
    }

    function format_balance(chain, balance) {
        if (chain == 'bitcoin') {
            return (balance / 100000000).toFixed(8)
        } else if (chain == 'diem' || chain == 'violas') {
            return (balance / 1000000).toFixed(6)
        } else {
            return balance
        }
    }

    function get_currency_balance(chain, currency) {
        for (var i = 0; i < model_tokens.count; i++) {
            var obj = model_tokens.get(i)
            if (obj["chain"] == chain && obj["name"] == currency) {
                return format_balance(chain, obj["balance"])
            }
        }
    }

    function open_url(url) {
        payController.open_url(url)
    }

    function copy_text(text) {
        payController.copy_text(text)
    }

    function create_wallet() {
        payController.create_wallet()
    }

    function delete_wallet() {
        payController.delete_wallet()
    }

    function create_wallet_from_mnemonic(mnemonic) {
        payController.create_wallet_from_mnemonic(mnemonic)
    }

    function gen_random_mnemonic() {
        payController.gen_random_mnemonic()
    }

    function change_locale(locale_name) {
        payController.change_locale(locale_name)
    }

    function publish_currency(chain, currency) {
        payController.publish_currency(chain, currency)
    }
    
    function gen_qr(chain, show_name) {
        payController.gen_qr(chain, show_name)
    }

    function send_coin(address, amount, chain, currency) {
        payController.send_coin(address, amount, chain, currency)
    }
}
