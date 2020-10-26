import QtQuick 2.14

import "../models/API.js" as API

import PyPay 1.0

Item {
    property var rates: {}
    property var balances: []
    property var published: []
    property var bankAccountInfo: ({})
    property var bankDepositInfo: ({})
    property var bankBorrowInfo: ({})

    property alias tokenModel: tokenModel
    property alias depositModel: depositModel
    property alias borrowModel: borrowModel
    property alias intorModel: intorModel
    property alias questionModel: questionModel
    property alias currentDepositModel: currentDepositModel
    property alias depositDetailModel: depositDetailModel
    property alias currentBorrowModel: currentBorrowModel
    property alias borrowDetailModel: borrowDetailModel

    ListModel {
        id: tokenModel
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

    function getRate() {
        API.request('GET', 'https://api.exchangeratesapi.io/latest?base=USD', null, function(resp) {
                rates = resp.rates;
            });
    }

    function getTokenPublished(params) {
        API.request('GET', API.violasURL + '/1.0/violas/currency/published' + API.formatParams(params), null, function(resp) {
            if (resp.code == 2000) {
                published = resp.data.published
            }
        });
    }

    function getViolasCurrency() {
        API.request('GET', API.violasURL + '/1.0/violas/currency', null, function(resp) {
            if (resp.code == 2000) {
                var entries = resp.data.currencies;
                for (var i=0; i<entries.length; i++) {
                    tokenModel.append(entries[i])
                }
            }
        });
    }

    function getLibraCurrency() {
        API.request('GET', API.violasURL + '/1.0/libra/currency', null, function(resp) {
            if (resp.code == 2000) {
                var entries = resp.data.currencies;
                for (var i=0; i<entries.length; i++) {
                    tokenModel.append(entries[i])
                }
            }
        });
    }


    // Bank

    function getBankAccountInfo(params) {
        API.request('GET', API.violasURL + '/1.0/violas/bank/account/info' + API.formatParams(params), null, function(resp) {
                bankAccountInfo = resp.data;
            });
    }

    function getDeposit() {
        API.request('GET', API.violasURL + '/1.0/violas/bank/product/deposit', null, function(resp) {
                var entries = resp.data;
                for (var i=0; i<entries.length; i++) {
                    depositModel.append(entries[i])
                }
            });
    }

    function getBorrow() {
        API.request('GET', API.violasURL + '/1.0/violas/bank/product/borrow', null, function(resp) {
                var entries = resp.data;
                for (var i=0; i<entries.length; i++) {
                    borrowModel.append(entries[i])
                }
            });
    }

    function getDepositInfo(params, cb) {
        API.request('GET', API.violasURL + '/1.0/violas/bank/deposit/info' + API.formatParams(params),
            null, function(resp) {
                bankDepositInfo = resp.data;
                for (var i=0; i<resp.data.intor.length; i++) {
                    intorModel.append({"title":resp.data.intor[i].title, "content":resp.data.intor[i].text})
                }
                for (var i=0; i<resp.data.question.length; i++) {
                    questionModel.append({"title":resp.data.question[i].title, "content":resp.data.question[i].text})
                }
                if (cb) {
                    cb()
                }
                console.log(JSON.stringify(bankDepositInfo))
            });
    }

    function getBorrowInfo(params, cb) {
        API.request('GET', API.violasURL + '/1.0/violas/bank/borrow/info' + API.formatParams(params),
            null, function(resp) {
                bankBorrowInfo = resp.data;
                for (var i=0; i<resp.data.intor.length; i++) {
                    intorModel.append({"title":resp.data.intor[i].title, "content":resp.data.intor[i].text})
                }
                for (var i=0; i<resp.data.question.length; i++) {
                    questionModel.append({"title":resp.data.question[i].title, "content":resp.data.question[i].text})
                }
                if (cb) {
                    cb()
                }
                console.log(JSON.stringify(bankBorrowInfo))
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
}
