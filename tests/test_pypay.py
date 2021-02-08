from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

# curl -i http://localhost:5000
@app.route('/')
def test_index():
    return 'Bank api!'

@app.route('/1.0/libra/balance', methods=['GET'])
def test_libra_balance():
    data = {
        "balances": [
            {
                "LBR": 10000000,
                "name": "XUS",
                "show_icon": "http://52.27.228.84:4000/1.0/violas/icon/libra.png",
                "show_name": "XUS",
                "address": ""
            }
        ]
    }
    return jsonify({'code': 2000, 'data': data, 'message': 'ok'})


"""

# curl -i http://localhost:5000/1.0/violas/balance
@app.route('/1.0/violas/balance', methods=['GET'])
def test_violas_balance():
    address = request.args.get("address")
    data = {
        "balances": [
            {
                "LBR": 10000,
                "name": "LBR",
                "show_icon": "http://52.27.228.84:4000/1.0/violas/icon/libra.png",
                "show_name": "VLS",
                "address": ""
            },
            {
                "VLSGBP": 1000,
                "name": "VLSGBP",
                "show_icon": "http://52.27.228.84:4000/1.0/violas/icon/libra.png",
                "show_name": "VLSGBP",
                "address": ""
            },
            {
                "VLSUSD": 3000,
                "name": "VLSUSD",
                "show_icon": "http://52.27.228.84:4000/1.0/violas/icon/libra.png",
                "show_name": "VLSUSD",
                "address": ""
            },
        ]
    }
    return jsonify({'code': 2000, 'data': data, 'message': 'ok'})

@app.route('/1.0/violas/value/btc', methods=['GET'])
def test_violas_value_btc():
    data = {
        "BTC": 9823
    }
    return jsonify({'code': 2000, 'data': data, 'message': 'ok'})

@app.route('/1.0/violas/value/violas', methods=['GET'])
def test_violas_value_violas():
    data = {
        "LBR": 0,
        "VLSUSD": 1,
        "VLSGBP": 0.79
    }
    return jsonify({'code': 2000, 'data': data, 'message': 'ok'})

@app.route('/1.0/libra/currency', methods=['GET'])
def test_libra_currency():
    data = {
        "currencies": [
            {
                "address": "",
                "module": "Coin1",
                "name": "Coin1",
                "show_icon": "http://52.27.228.84:4000/1.0/violas/icon/libra.png",
                "show_name": "n1"
            },
            {
                "address": "",
                "module": "Coin2",
                "name": "Coin2",
                "show_icon": "http://52.27.228.84:4000/1.0/violas/icon/libra.png",
                "show_name": "n2"
            },
            {
                "address": "",
                "module": "LBR",
                "name": "LBR",
                "show_icon": "http://52.27.228.84:4000/1.0/violas/icon/libra.png",
                "show_name": "LBR"
            }
        ]
    }
    return jsonify({'code': 2000, 'data': data, 'message': 'ok'})

@app.route('/1.0/violas/currency', methods=['GET'])
def test_violas_currency():
    data = {
        "currencies": [
            {
                "address": "",
                "module": "VLSGBP",
                "name": "VLSGBP",
                "show_icon": "http://52.27.228.84:4000/1.0/violas/icon/libra.png",
                "show_name": "VLSGBP"
            },
            {
                "address": "",
                "module": "VLSUSD",
                "name": "VLSUSD",
                "show_icon": "http://52.27.228.84:4000/1.0/violas/icon/libra.png",
                "show_name": "VLSUSD"
            },
            {
                "address": "",
                "module": "LBR",
                "name": "LBR",
                "show_icon": "http://52.27.228.84:4000/1.0/violas/icon/libra.png",
                "show_name": "VLS"
            }
        ]
    }
    return jsonify({'code': 2000, 'data': data, 'message': 'ok'})

@app.route('/1.0/violas/currency/published', methods=['GET'])
def test_violas_currency_published():
    data = {
        "published": [
            "LBR",
            "VLSUSD"
        ]
    }
    return jsonify({'code': 2000, 'data': data, 'message': 'ok'})

# curl -i http://localhost:5000/1.0/violas/bank/account/info
@app.route('/1.0/violas/bank/account/info', methods=['GET'])
def test_bank_account_info():
    address = request.args.get("address")
    data = {
        "amount": 2000.34,
        "borrow": 1403.23,
        "total": 42.76,
        "yesterday": 0.3
    }
    return jsonify({'code': 2000, 'data': data, 'message': 'ok'})

# /1.0/violas/bank/product/deposit
@app.route('/1.0/violas/bank/product/deposit', methods=['GET'])
def test_bank_product_deposit():
    data = [
        {
            "desc": "deposit 1",
            "id": "100001",
            "logo": "https://api4.violas.io/1.0/violas/icon/violas.png",
            "name": "a",
            "rate": 0.032,
            "rate_desc": "年化利率",
            "token_module": "BTC"
        },
        {
            "desc": "deposit 2",
            "id": "100002",
            "logo": "https://api4.violas.io/1.0/violas/icon/violas.png",
            "name": "b",
            "rate": 0.032,
            "rate_desc": "年化利率",
            "token_module": "BTC"
        }
    ]
    return jsonify({'code': 2000, 'data': data, 'message': 'ok'})

# /1.0/violas/bank/product/borrow
@app.route('/1.0/violas/bank/product/borrow', methods=['GET'])
def test_bank_product_borrow():
    data = [
        {
            "desc": "borrow 1",
            "id": "200001",
            "logo": "https://api4.violas.io/1.0/violas/icon/violas.png",
            "name": "a",
            "rate": 0.032,
            "rate_desc": "年化利率",
            "token_module": "BTC"
        },
        {
            "desc": "borrow 2",
            "id": "200002",
            "logo": "https://api4.violas.io/1.0/violas/icon/violas.png",
            "name": "b",
            "rate": 0.032,
            "rate_desc": "年化利率",
            "token_module": "BTC"
        }
    ]
    return jsonify({'code': 2000, 'data': data, 'message': 'ok'})

# /1.0/violas/bank/deposit/info
@app.route('/1.0/violas/bank/deposit/info', methods=['GET'])
def test_bank_deposit_info():
    data = {
        "id": "1000001",
        "intor": [
          {
            "text": "对利息的计算规则进行说明",
            "title": "①"
          },
          {
            "text": "平台保证用户资金的安全",
            "title": "②"
          }
        ],
        "logo": "https://api4.violas.io/1.0/violas/icon/violas.png",
        "minimum_amount": 1000000,
        "minimum_step": 1000000,
        "name": "USD存款01",
        "pledge_rate": 0.5,
        "question": [
          {
            "text": "使用Violas Wallet钱包直接购买。",
            "title": "怎么买？"
          },
          {
            "text": "很安全",
            "title": "安全么？"
          }
        ],
        "quota_limit": 1000000000,
        "quota_used": 0,
        "rate": 0.04,
        "rate_desc": "年化收益率",
        "token_address": "00000000000000000000000000000001",
        "token_module": "USD",
        "token_name": "USD",
        "token_show_name": "USD"
    }
    return jsonify({'code': 2000, 'data': data, 'message': 'ok'})

# /1.0/violas/bank/borrow/info
@app.route('/1.0/violas/bank/borrow/info', methods=['GET'])
def test_bank_borrow_info():
    data = {
        "id": "2000001",
        "intor": [
          {
            "text": "对利息的计算规则进行说明",
            "title": "①"
          },
          {
            "text": "平台保证用户资金的安全",
            "title": "②"
          }
        ],
        "logo": "https://api4.violas.io/1.0/violas/icon/violas.png",
        "minimum_amount": 1000000,
        "minimum_step": 1000000,
        "name": "USD借款01",
        "pledge_rate": 0.5,
        "question": [
          {
            "text": "使用Violas Wallet钱包直接购买。",
            "title": "怎么买？"
          },
          {
            "text": "很安全",
            "title": "安全么？"
          }
        ],
        "quota_limit": 1000000000,
        "quota_used": 0,
        "rate": 0.06,
        "token_address": "00000000000000000000000000000001",
        "token_module": "USD",
        "token_name": "USD",
        "token_show_name": "USD"
    }
    return jsonify({'code': 2000, 'data': data, 'message': 'ok'})

# /1.0/violas/bank/deposit/orders
@app.route('/1.0/violas/bank/deposit/orders', methods=['GET'])
def test_bank_deposit_orders():
    address = request.args.get("address")
    offset = int(request.args.get("offset"))
    limit = int(request.args.get("limit"))
    data = []
    count = 11
    for i in range(count):
        data.append({
                "currency": "LBR",
                "earnings": 22,
                "id": "2000001",
                "logo": "https://api4.violas.io/1.0/violas/icon/violas.png",
                "principal": 1500,
                "rate": 3.9,
                "status": 1,
                "total_count": count
            })
    return jsonify({'code': 2000, 'data': data[offset : offset+limit], 'message': 'ok'})

# /1.0/violas/bank/deposit/order/list
@app.route('/1.0/violas/bank/deposit/order/list', methods=['GET'])
def test_bank_deposit_order_list():
    address = request.args.get("address")
    offset = int(request.args.get("offset"))
    limit = int(request.args.get("limit"))
    data = []
    count = 31
    for i in range(count):
        data.append({
                "currency": "LBR",
                "date": 1518391892,
                "id": "2000001",
                "logo": "https://api4.violas.io/1.0/violas/icon/violas.png",
                "status": 1,
                "value": 182.22,
                "total_count": count
            })
    return jsonify({'code': 2000, 'data': data[offset : offset+limit], 'message': 'ok'})

# /1.0/violas/bank/borrow/orders
@app.route('/1.0/violas/bank/borrow/orders', methods=['GET'])
def test_bank_borrow_orders():
    address = request.args.get("address")
    offset = int(request.args.get("offset"))
    limit = int(request.args.get("limit"))
    data = []
    count = 11
    for i in range(count):
        data.append({
                "amount": 1500,
                "id": "2000001",
                "logo": "https://api4.violas.io/1.0/violas/icon/violas.png",
                "name": "LBR",
                "available_borrow": 1500,
                "total_count": count
            })
    return jsonify({'code': 2000, 'data': data[offset : offset+limit], 'message': 'ok'})

# /1.0/violas/bank/borrow/order/list
@app.route('/1.0/violas/bank/borrow/order/list', methods=['GET'])
def test_bank_borrow_order_list():
    address = request.args.get("address")
    offset = int(request.args.get("offset"))
    limit = int(request.args.get("limit"))
    data = []
    count = 121
    for i in range(count):
        data.append({
                "currency": "LBR",
                "date": 1518391892,
                "id": "2000001",
                "logo": "https://api4.violas.io/1.0/violas/icon/violas.png",
                "status": 1,
                "value": 182.22,
                "total_count": count
            })
    return jsonify({'code': 2000, 'data': data[offset : offset+limit], 'message': 'ok'})


"""

@app.errorhandler(404)
def test_not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)

if __name__ == '__main__':
    app.debug =  True
    app.run()
