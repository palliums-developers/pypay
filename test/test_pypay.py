from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

# curl -i http://localhost:5000
@app.route('/')
def index():
    return 'Bank api!'

# curl -i http://localhost:5000/1.0/violas/bank/account/info
@app.route('/1.0/violas/bank/account/info', methods=['GET'])
def bank_account_info():
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
def bank_product_deposit():
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
def bank_product_borrow():
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
def bank_deposit_info():
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
def bank_borrow_info():
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

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)

if __name__ == '__main__':
    app.debug =  True
    app.run()
