import QtQuick 2.15

import "../models/API.js" as API

import PyPay 1.0

Item {
    property string address_bitcoin: ""
    property string address_libra: ""
    property string address_violas: ""
    property var btcValue: 0
    property var violasValue: {}
    property var rates: {}
    property var balances: []
    property var published: []
    property var localPublished: ["BTC","LBR","VLS"]
    property var bankAccountInfo: {
        "amount": 0.0,
        "borrow": 0.0,
        "total": 0.0,
        "yesterday": 0.0
    }
    property var bankDepositInfo: {
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
    property var bankBorrowInfo: {
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

    property string requestID: ""
    property var request_token: {
        'chain': 'bitcoin',
        'name': 'BTC',
        'show_icon': "../icons/bitcoin.svg",
        'show_name': 'BTC',
        'balance': 0
    }

    property alias token_balance_model: token_balance_model
    property alias tokenModel: tokenModel
    property alias depositModel: depositModel
    property alias borrowModel: borrowModel
    property alias intorModel: intorModel
    property alias questionModel: questionModel
    property alias currentDepositModel: currentDepositModel
    property alias depositDetailModel: depositDetailModel
    property alias currentBorrowModel: currentBorrowModel
    property alias borrowDetailModel: borrowDetailModel

    WorkerScript {
        id: worker
        source: "models/DataLoader.mjs"
    }

    ListModel {
        id: token_balance_model
    }

    ListModel {
        id: tokenModel
        ListElement {
            chain: "bitcoin"
            name: "BTC"
            show_name: "BTC"
            show_icon: "../icons/bitcoin.svg"
        }
        ListElement {
            chain: "libra"
            name: "LBR"
            show_name: "LBR"
            show_icon: "../icons/libra.svg"
        }
        ListElement {
            chain: "violas"
            name: "VLS"
            show_name: "VLS"
            show_icon: "../icons/violas.svg"
        }
    }

    ListModel {
        id: depositModel
    }

    ListModel {
        id: borrowModel
    }

    ListModel {
        id: intorModel
    }

    ListModel {
        id: questionModel
    }

    ListModel {
        id: currentDepositModel
    }

    ListModel {
        id: depositDetailModel
    }

    ListModel {
        id: currentBorrowModel
    }

    ListModel {
        id: borrowDetailModel
    }

    Connections {
        target: payController
        function onChanged_address_bitcoin() {
            address_bitcoin = payController.address_bitcoin
        }
        function onChanged_address_libra() {
            address_libra = payController.address_libra
        }
        function onChanged_address_violas() {
            address_violas = payController.address_violas
            get_token_blanace()
            var params = {"address": address_violas}
            getViolasValueViolas(params)
            getViolasCurrencyPublished(params)
            getViolasBankAccountInfo(params)
        }
    }

    //function getRateBaseUSD() {
    //    API.request('GET', 'https://api.exchangeratesapi.io/latest?base=USD', null, function(resp) {
    //            rates = resp.rates;
    //        });
    //}

    function getViolasValueBTC() {
        API.request('GET', API.violasURL + '/1.0/violas/value/btc', null, 
            function(resp) {
                if (resp.code == 2000) {
                    btcValue = resp.data["BTC"]
                }
            });
    }

    function getViolasValueViolas(params) {
        API.request('GET', API.violasURL + '/1.0/violas/value/violas' + API.formatParams(params), null, 
            function(resp) {
                if (resp.code == 2000) {
                    violasValue = resp.data
                }
            });
    }

    function getLibraBalance(params, cb) {
        API.request('GET', API.violasURL + '/1.0/libra/balance' + API.formatParams(params), null, 
            function(resp) {
                if (resp.code == 2000) {
                    balances = resp.data["balances"]
                    if (cb) {
                        cb()
                    }
                }
        });
    }

    function getViolasBalance(params, cb) {
        API.request('GET', API.violasURL + '/1.0/violas/balance' + API.formatParams(params), null, 
            function(resp) {
                if (resp.code == 2000) {
                    balances = resp.data["balances"]
                    if (cb) {
                        cb()
                    }
                }
        });
    }

    function getViolasCurrencyPublished(params) {
        API.request('GET', API.violasURL + '/1.0/violas/currency/published' + API.formatParams(params), null, function(resp) {
            if (resp.code == 2000) {
                published = resp.data.published
            }
        });
    }

    function getLibraCurrency() {
        API.request('GET', API.violasURL + '/1.0/libra/currency', null, function(resp) {
            if (resp.code == 2000) {
                var entries = resp.data.currencies;
                for (var i=0; i<entries.length; i++) {
                    if (entries[i].show_name != "LBR" && entries[i].name != "Coin1" && entries[i].name != "Coin2") {
                        var d = entries[i]
                        tokenModel.append(
                            {
                                "chain": "libra",
                                "name": d.name,
                                "show_name": d.show_name,
                                "show_icon": "../icons/libra.svg"
                            }
                        )
                    }
                }
            }
        });
    }

    function getViolasCurrency() {
        API.request('GET', API.violasURL + '/1.0/violas/currency', null, function(resp) {
            if (resp.code == 2000) {
                var entries = resp.data.currencies;
                for (var i=0; i<entries.length; i++) {
                    if (entries[i].show_name != "VLS" || entries[i].name != "LBR") {
                        var d = entries[i]
                        tokenModel.append(
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


    // Bank

    function getViolasBankAccountInfo(params, cb) {
        API.request('GET', API.violasURL + '/1.0/violas/bank/account/info' + API.formatParams(params), null, function(resp) {
                bankAccountInfo = resp.data;
                if (cb) {
                    cb()
                }
            });
    }

    function getViolasBankProductDeposit(cb) {
        API.request('GET', API.violasURL + '/1.0/violas/bank/product/deposit', null, function(resp) {
                var entries = resp.data;
                depositModel.clear()
                for (var i=0; i<entries.length; i++) {
                    depositModel.append(entries[i])
                }
                if (cb) {
                    cb()
                }
            });
    }

    function getViolasBankProductBorrow(cb) {
        API.request('GET', API.violasURL + '/1.0/violas/bank/product/borrow', null, function(resp) {
                var entries = resp.data;
                borrowModel.clear()
                for (var i=0; i<entries.length; i++) {
                    borrowModel.append(entries[i])
                }
                if (cb) {
                    cb()
                }
            });
    }

    function getViolasBankDepositInfo(params, cb) {
        API.request('GET', API.violasURL + '/1.0/violas/bank/deposit/info' + API.formatParams(params),
            null, function(resp) {
                bankDepositInfo = resp.data;
                intorModel.clear()
                for (var i=0; i<resp.data.intor.length; i++) {
                    intorModel.append({"title":resp.data.intor[i].title, "content":resp.data.intor[i].text})
                }
                questionModel.clear()
                for (var i=0; i<resp.data.question.length; i++) {
                    questionModel.append({"title":resp.data.question[i].title, "content":resp.data.question[i].text})
                }
                if (cb) {
                    cb()
                }
            });
    }

    function getViolasBankBorrowInfo(params, cb) {
        API.request('GET', API.violasURL + '/1.0/violas/bank/borrow/info' + API.formatParams(params),
            null, function(resp) {
                bankBorrowInfo = resp.data;
                intorModel.clear()
                for (var i=0; i<resp.data.intor.length; i++) {
                    intorModel.append({"title":resp.data.intor[i].title, "content":resp.data.intor[i].text})
                }
                questionModel.clear()
                for (var i=0; i<resp.data.question.length; i++) {
                    questionModel.append({"title":resp.data.question[i].title, "content":resp.data.question[i].text})
                }
                if (cb) {
                    cb()
                }
            });
    }

    function getViolasBankDepositOrders(params, cb) {
        API.request('GET', API.violasURL + '/1.0/violas/bank/deposit/orders' + API.formatParams(params), null,
            function(resp) {
            currentDepositModel.clear()
            for (var i=0; i<resp.data.length;i++) {
                var d = resp.data[i]
                currentDepositModel.append({
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

    function getViolasBankDepositOrderList(params, cb) {
        API.request('GET', API.violasURL + '/1.0/violas/bank/deposit/order/list' + API.formatParams(params), null, 
            function(resp) {
            depositDetailModel.clear()
            for (var i=0; i<resp.data.length;i++) {
                var d = resp.data[i]
                depositDetailModel.append({
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

    function getViolasBankBorrowOrders(params, cb) {
        API.request('GET', API.violasURL + '/1.0/violas/bank/borrow/orders' + API.formatParams(params), null, 
            function(resp) {
            currentBorrowModel.clear()
            for (var i=0; i<resp.data.length;i++) {
                var d = resp.data[i]
                currentBorrowModel.append({
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

    function getViolasBankBorrowOrderList(params, cb) {
        API.request('GET', API.violasURL + '/1.0/violas/bank/borrow/order/list' + API.formatParams(params), null, 
            function(resp) {
            borrowDetailModel.clear()
            for (var i=0; i<resp.data.length;i++) {
                var d = resp.data[i]
                borrowDetailModel.append({
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

    function get_token_blanace() {
        var msg = {'action':'getBalances', 'model':server.token_balance_model, 'libraAddr': payController.libra_addr, 'violasAddr': payController.addr};
        worker.sendMessage(msg);
    }

    function get_rate(chain, token) {
        if (chain == "bitcoin") {
            return btcValue
        } else if (chain == 'libra') {
            return 0
        } else if (token == "VLS" || token == "LBR") {
            return 0
        } else {
            return violasValue[token]
        }
    }

    function format_balance(chain, balance) {
        if (chain == 'bitcoin') {
            return (balance / 100000000).toFixed(8)
        } else if (chain == libra || chain == violas) {
            return (balance / 1000000).toFixed(6)
        } else {
            return balance
        }
    }
}
