from flask import Flask, request, jsonify, render_template, redirect, url_for
from web3.middleware import geth_poa_middleware
from web3 import Web3
import string

app = Flask(__name__)

web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

accounts = web3.eth.accounts
address = '0xDFFc380d425424f41A038fF726425F0Cf12E8Cef'

abi = '''[
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "estateID",
				"type": "uint256"
			},
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "adID",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "date",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "price",
				"type": "uint256"
			}
		],
		"name": "AdCreated",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "estateID",
				"type": "uint256"
			},
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "adID",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "date",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "enum EstateAgency.AdvertisementStatus",
				"name": "adStatus",
				"type": "uint8"
			}
		],
		"name": "AdUpdated",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "estateID",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "date",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "enum EstateAgency.EstateType",
				"name": "estateType",
				"type": "uint8"
			}
		],
		"name": "EstateCreated",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "buyer",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "adID",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "estateID",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "enum EstateAgency.AdvertisementStatus",
				"name": "adStatus",
				"type": "uint8"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "date",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "price",
				"type": "uint256"
			}
		],
		"name": "EstatePurchased",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "estateID",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "date",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "bool",
				"name": "isActive",
				"type": "bool"
			}
		],
		"name": "EstateUpdated",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "receiver",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "date",
				"type": "uint256"
			}
		],
		"name": "FundsSent",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "advertisements",
		"outputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "buyer",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "price",
				"type": "uint256"
			},
			{
				"internalType": "enum EstateAgency.AdvertisementStatus",
				"name": "adStatus",
				"type": "uint8"
			},
			{
				"internalType": "uint256",
				"name": "estateID",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "dateTime",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "adID",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "balanceSeller",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "estateID",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_price",
				"type": "uint256"
			}
		],
		"name": "createAd",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_addressOfEstate",
				"type": "string"
			},
			{
				"internalType": "enum EstateAgency.EstateType",
				"name": "_estateType",
				"type": "uint8"
			},
			{
				"internalType": "uint256",
				"name": "_rooms",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_describe",
				"type": "string"
			}
		],
		"name": "createEstate",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "estates",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "addressOfEstate",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "estateID",
				"type": "uint256"
			},
			{
				"internalType": "enum EstateAgency.EstateType",
				"name": "estateType",
				"type": "uint8"
			},
			{
				"internalType": "uint256",
				"name": "rooms",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "describe",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "bool",
				"name": "isActive",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "adID",
				"type": "uint256"
			}
		],
		"name": "getAd",
		"outputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "owner",
						"type": "address"
					},
					{
						"internalType": "address",
						"name": "buyer",
						"type": "address"
					},
					{
						"internalType": "uint256",
						"name": "price",
						"type": "uint256"
					},
					{
						"internalType": "enum EstateAgency.AdvertisementStatus",
						"name": "adStatus",
						"type": "uint8"
					},
					{
						"internalType": "uint256",
						"name": "estateID",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "dateTime",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "adID",
						"type": "uint256"
					}
				],
				"internalType": "struct EstateAgency.Advertisement",
				"name": "",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getAllAds",
		"outputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "owner",
						"type": "address"
					},
					{
						"internalType": "address",
						"name": "buyer",
						"type": "address"
					},
					{
						"internalType": "uint256",
						"name": "price",
						"type": "uint256"
					},
					{
						"internalType": "enum EstateAgency.AdvertisementStatus",
						"name": "adStatus",
						"type": "uint8"
					},
					{
						"internalType": "uint256",
						"name": "estateID",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "dateTime",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "adID",
						"type": "uint256"
					}
				],
				"internalType": "struct EstateAgency.Advertisement[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getAllEstates",
		"outputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "addressOfEstate",
						"type": "string"
					},
					{
						"internalType": "uint256",
						"name": "estateID",
						"type": "uint256"
					},
					{
						"internalType": "enum EstateAgency.EstateType",
						"name": "estateType",
						"type": "uint8"
					},
					{
						"internalType": "uint256",
						"name": "rooms",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "describe",
						"type": "string"
					},
					{
						"internalType": "address",
						"name": "owner",
						"type": "address"
					},
					{
						"internalType": "bool",
						"name": "isActive",
						"type": "bool"
					}
				],
				"internalType": "struct EstateAgency.Estate[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getBalance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "estateID",
				"type": "uint256"
			}
		],
		"name": "getEstate",
		"outputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "addressOfEstate",
						"type": "string"
					},
					{
						"internalType": "uint256",
						"name": "estateID",
						"type": "uint256"
					},
					{
						"internalType": "enum EstateAgency.EstateType",
						"name": "estateType",
						"type": "uint8"
					},
					{
						"internalType": "uint256",
						"name": "rooms",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "describe",
						"type": "string"
					},
					{
						"internalType": "address",
						"name": "owner",
						"type": "address"
					},
					{
						"internalType": "bool",
						"name": "isActive",
						"type": "bool"
					}
				],
				"internalType": "struct EstateAgency.Estate",
				"name": "",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "adID",
				"type": "uint256"
			}
		],
		"name": "purchaseEstate",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "adID",
				"type": "uint256"
			},
			{
				"internalType": "enum EstateAgency.AdvertisementStatus",
				"name": "_adStatus",
				"type": "uint8"
			}
		],
		"name": "updateAdStatus",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "estateID",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "_isActive",
				"type": "bool"
			}
		],
		"name": "updateEstateStatus",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "withdraw",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]'''
contract = web3.eth.contract(address=address, abi=abi)


def check(password):
    digits = any(char in string.digits for char in password)
    punctuation = any(char in string.punctuation for char in password)
    lowers = any(char in string.ascii_lowercase for char in password)
    capitals = any(char in string.ascii_uppercase for char in password)
    return digits and punctuation and lowers and capitals and len(password) >= 12


@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        password = request.form['password']
        if check(password):
            new_account = web3.geth.personal.new_account(password)
            return jsonify({'address': new_account})
        else:
            return jsonify({'error': 'Weak password'})
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        public_key = request.form['key']
        password = request.form['password']
        try:
            web3.geth.personal.unlock_account(public_key, password)
            return redirect(url_for('dashboard', account=public_key))
        except Exception as e:
            return jsonify({'error': str(e)})
    return render_template('login.html')


@app.route('/dashboard/<account>')
def dashboard(account):
    return render_template('dashboard.html', account=account)


@app.route('/balance/<account>')
def balance(account):
    try:
        account_balance = contract.functions.getBalance().call({'from': account})
        return jsonify({'balance': account_balance})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/withdraw', methods=['POST'])
def withdraw():
    account = request.form['account']
    amount = request.form['amount']
    try:
        amount = int(amount)
        if amount <= 0:
            return jsonify({'error': 'Amount must be greater than zero'})
        _hash = contract.functions.withdraw(amount).transact({'from': account})
        return jsonify({'message': 'Transaction sent', 'tx_hash': _hash.hex()})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/create_estate', methods=['POST'])
def create_estate():
    account = request.form['account']
    estate_name = request.form['name']
    estate_address = request.form['address']
    estate_type = request.form['type']
    rooms = request.form['rooms']
    description = request.form['description']
    try:
        estate_type = int(estate_type)
        rooms = int(rooms)
        _hash = (contract.functions.createEstate(estate_name, estate_address, estate_type, rooms, description).transact(
            {
                'from': account
            }
        ))
        return jsonify({'tx_hash': _hash.hex()})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/create_ad', methods=['POST'])
def create_ad():
    account = request.form['account']
    ad_id = request.form['id']
    price = request.form['price']
    try:
        ad_id = int(ad_id)
        price = int(price)
        if price <= 0:
            return jsonify({'error': 'Price must be greater than zero'})
        _hash = contract.functions.createAd(ad_id, price).transact({'from': account})
        return jsonify({'tx_hash': _hash.hex()})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/purchase_estate', methods=['POST'])
def purchase_estate():
    account = request.form['account']
    estate_id = request.form['id']
    try:
        estate_id = int(estate_id)
        _hash = contract.functions.purchaseEstate(estate_id).transact({'from': account})
        return jsonify({'tx_hash': _hash.hex()})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/update_estate', methods=['POST'])
def update_estate():
    account = request.form['account']
    estate_id = request.form['id']
    estate_status = request.form['status']
    try:
        estate_id = int(estate_id)
        estate_status = bool(estate_status)
        _hash = contract.functions.updateEstateStatus(estate_id, estate_status).transact({'from': account})
        return jsonify({'tx_hash': _hash.hex()})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/update_ad', methods=['POST'])
def update_ad():
    account = request.form['account']
    ad_id = request.form['id']
    ad_status = request.form['status']
    try:
        ad_id = int(ad_id)
        ad_status = int(ad_status)
        _hash = contract.functions.updateAdStatus(ad_id, ad_status).transact({'from': account})
        return jsonify({'tx_hash': _hash.hex()})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/get_all_ads', methods=['GET'])
def get_all_ads():
    try:
        ads = contract.functions.getAllAds().call()
        return jsonify({'ads': ads})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/get_ad/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):
    try:
        ad = contract.functions.getAd(ad_id).call()
        return jsonify({'ad': ad})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/get_all_estates', methods=['GET'])
def get_all_estates():
    try:
        estates = contract.functions.getAllEstates().call()
        return jsonify({'estates': estates})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/get_estate/<int:estate_id>', methods=['GET'])
def get_estate(estate_id):
    try:
        estate = contract.functions.getEstate(estate_id).call()
        return jsonify({'estate': estate})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
