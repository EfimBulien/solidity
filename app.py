from flask import Flask, request, render_template, redirect, url_for
from flask_caching import Cache
from web3.middleware import geth_poa_middleware
from web3 import Web3
import string

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

accounts = web3.eth.accounts
address = web3.to_checksum_address('0xE4FfC25952a27bdaA2E899790656F63FEe4fC731')

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
    print(digits, punctuation, lowers, capitals, password)
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
            print(new_account, password)
            return render_template('success.html', message=f'Новый аккаунт создан: {new_account}')
        else:
            return render_template('error.html', message='Пароль не соответсвует требованиям.')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            public_key = request.form['key']
            password = request.form['password']
            web3.geth.personal.unlock_account(public_key, password)
            print(public_key, password)
            return redirect(url_for('dashboard', account=public_key))
        except Exception as e:
            return render_template('error.html', message=str(e))
    return render_template('login.html')


@app.route('/dashboard/<account>')
@cache.cached(timeout=60)
def dashboard(account):
    print(account)
    return render_template('dashboard.html', account=account)


@app.route('/balance/<account>')
@cache.cached(timeout=60)
def balance(account):
    try:
        account_balance = contract.functions.getBalance().call({'from': account})
        print(account,account_balance)
        return render_template('balance.html', balance=account_balance)
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/withdraw', methods=['POST'])
@cache.cached(timeout=60)
def withdraw():
    try:
        account = web3.to_checksum_address(request.form['account'])
        amount = int(request.form['amount'])
        if amount <= 0:
            print(amount)
            return render_template('error.html', message='Сумма должна быть больше 0.')
        _hash = contract.functions.withdraw(amount).transact({'from': account})
        print(account, amount, _hash)
        return render_template('success.html', message=f'Успешное списание средств. '
                                                       f'Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/create_estate', methods=['POST'])
@cache.cached(timeout=60)
def create_estate():
    try:
        account = web3.to_checksum_address(request.form['account'])
        estate_name = request.form['name']
        estate_address = request.form['address']
        estate_type = int(request.form['type'])
        rooms = int(request.form['rooms'])
        description = request.form['description']
        _hash = contract.functions.createEstate(estate_name, estate_address, estate_type, rooms, description).transact(
            {'from': account})
        print(account, estate_name, estate_address, estate_type, rooms, description, _hash)
        return render_template('success.html', message=f'Недвижимость успешно создана. '
                                                       f'Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/create_ad', methods=['POST'])
@cache.cached(timeout=60)
def create_ad():
    try:
        account = web3.to_checksum_address(request.form['account'])
        ad_id = int(request.form['id'])
        price = int(request.form['price'])
        if price <= 0:
            return render_template('error.html', message='Цена должна быть больше 0.')
        _hash = contract.functions.createAd(ad_id, price).transact({'from': account})
        print(account, ad_id, price, _hash)
        return render_template('success.html', message=f'Объявление создано. '
                                                       f'Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/purchase_estate', methods=['POST'])
def purchase_estate():
    try:
        account = web3.to_checksum_address(request.form['account'])
        estate_id = int(request.form['id'])
        _hash = contract.functions.purchaseEstate(estate_id).transact({'from': account})
        print(account, estate_id, _hash)
        return render_template('success.html', message=f'Недвижимость успешно приобретена. '
                                                       f'Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/update_estate', methods=['POST'])
@cache.cached(timeout=60)
def update_estate():
    try:
        account = web3.to_checksum_address(request.form['account'])
        estate_id = int(request.form['id'])
        estate_status = bool(request.form['status'])
        _hash = contract.functions.updateEstateStatus(estate_id, estate_status).transact({'from': account})
        print(account, estate_id, estate_status,_hash)
        return render_template('success.html', message=f'Статус недвижимости обновлен. '
                                                       f'Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        print(e)
        return render_template('error.html', message=str(e))


@app.route('/update_ad', methods=['POST'])
@cache.cached(timeout=60)
def update_ad():
    try:
        account = web3.to_checksum_address(request.form['account'])
        ad_id = int(request.form['id'])
        ad_status = int(request.form['status'])
        _hash = contract.functions.updateAdStatus(ad_id, ad_status).transact({'from': account})
        print(account, ad_id, ad_status,_hash)
        return render_template('success.html', message=f'Статус объявления обновлен. '
                                                       f'Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        print(e)
        return render_template('error.html', message=str(e))


@app.route('/get_all_ads', methods=['GET'])
@cache.cached(timeout=60)
def get_all_ads():
    try:
        ads = contract.functions.getAllAds().call()
        print(ads)
        return render_template('ads.html', ads=ads)
    except Exception as e:
        print(e)
        return render_template('error.html', message=str(e))


@app.route('/get_ad', methods=['GET'])
@cache.cached(timeout=60)
def get_ad():
    try:
        ad_id = request.args.get('ad_id', default=0, type=int)
        ad = contract.functions.getAd(ad_id).call()
        print(ad_id,ad)
        return render_template('ad.html', ad=ad)
    except Exception as e:
        print(e)
        return render_template('error.html', message=str(e))


@app.route('/get_all_estates', methods=['GET'])
@cache.cached(timeout=60)
def get_all_estates():
    try:
        estates = contract.functions.getAllEstates().call()
        print(estates)
        return render_template('estates.html', estates=estates)
    except Exception as e:
        print(e)
        return render_template('error.html', message=str(e))


@app.route('/get_estate', methods=['GET'])
@cache.cached(timeout=60)
def get_estate():
    try:
        estate_id = request.args.get('estate_id', default=0, type=int)
        estate = contract.functions.getEstate(estate_id).call()
        print(estate_id, estate)
        return render_template('estate.html', estate=estate)
    except Exception as e:
        print(e)
        return render_template('error.html', message=str(e))


if __name__ == '__main__':
    app.run(debug=True)
