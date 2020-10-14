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

    function getRate() {
        API.request('GET', 'https://api.exchangeratesapi.io/latest?base=USD', null, function(resp) {
                rates = resp.rates;
            });
    }

    function getTokenPublished() {
        API.request('GET', API.violasURL + '/1.0/violas/currency/published?addr=' + payController.addr, null, function(resp) {
            if (resp.code == 2000) {
                published = resp.data.published
                //console.log(published)
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
        //request('GET', API.violasURL + '/1.0/libra/currency', null, function(resp) {
        //    if (resp.code == 2000) {
        //        var entries = resp.data.currencies;
        //        for (var i=0; i<entries.length; i++) {
        //            tokenModel.append(entries[i])
        //        }
        //    }
        //});
    }

    function getBankAccountInfo(addr) {
        API.request('GET', API.violasURL + '/1.0/violas/bank/account/info?address=' + addr, null, function(resp) {
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

    function getDepositInfo(id, cb) {
        API.request('GET', API.violasURL + '/1.0/violas/bank/deposit/info?id='+ id + '&address=' + payController.addr,
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

    function getBorrowInfo(id, cb) {
        API.request('GET', API.violasURL + '/1.0/violas/bank/borrow/info?id='+ id + '&address=' + payController.addr,
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

    function getDepositOrder(addr, offset, limit, cb) {
        API.request('GET', API.violasURL + '/1.0/violas/bank/deposit/orders?address=' + addr + '&offset=' + offset + '&limit=' + limit, null, 
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
                    "status": d.status
                    })                   
            }
            if (cb) {
                cb()
            }
        });
    }

    function getBorrowOrder(addr, offset, limit, cb) {
    }

    function getOrderList() {
        API.request('GET', API.violasURL + '/1.0/violas/bank/deposit/order/list?address='+payController.addr+'&offset='+0+'&limit='+100+'&start='+(new Date("2020-01-01 00:00:00").getTime())+'&end='+(new Date().getTime()), null, 
            function(resp) {
            for (var i=0; i<resp.data;i++) {
                var d = resp.data[i]
                depositDetailModel.append({'currency':d.currency,
                    'date':d.date,
                    'orderId':d.id,
                    'logo':d.logo,
                    'status':d.status,
                    'value':d.value,
                    'total_count':d.total_count,
                    })                   
            }
        });
    }
}
