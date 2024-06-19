import datetime

from flask import Flask, request, render_template, redirect, url_for
from flask_caching import Cache
from web3.middleware import geth_poa_middleware
from web3 import Web3
from contract_info.abi_contract import abi
from contract_info.address_contract import address
from utils import check
from config import config

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

accounts = web3.eth.accounts
address = web3.to_checksum_address(address)
contract = web3.eth.contract(address=address, abi=abi)


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
            print(datetime.datetime.now(), new_account, password)
            app.logger.info(f'{datetime.datetime.now()} - Account created!')
            return render_template('success.html', message=f'Новый аккаунт создан: {new_account}')
        else:
            app.logger.info(f'{datetime.datetime.now()} - Incorrect password!')
            return render_template('error.html', message='Пароль не соответсвует требованиям.')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            public_key = request.form['key']
            password = request.form['password']
            web3.geth.personal.unlock_account(public_key, password)
            print(datetime.datetime.now(), public_key, password)
            return redirect(url_for('dashboard', account=public_key))
        except Exception as e:
            print(datetime.datetime.now(), e)
            return render_template('error.html', message=str(e))
    return render_template('login.html')


@app.route('/dashboard/<account>')
@cache.cached(timeout=60)
def dashboard(account):
    print(datetime.datetime.now(), account)
    return render_template('dashboard.html', account=account)


@app.route('/balance/<account>')
@cache.cached(timeout=60)
def balance(account):
    try:
        account_balance = contract.functions.getBalance().call({'from': account})
        print(datetime.datetime.now(), account, account_balance)
        return render_template('balance.html', balance=account_balance)
    except Exception as e:
        print(datetime.datetime.now(), e)
        return render_template('error.html', message=str(e))


@app.route('/withdraw', methods=['POST'])
@cache.cached(timeout=60)
def withdraw():
    try:
        account = web3.to_checksum_address(request.form['account'])
        amount = int(request.form['amount'])
        if amount <= 0:
            print(datetime.datetime.now(), amount)
            return render_template('error.html', message='Сумма должна быть больше 0.')
        _hash = contract.functions.withdraw(amount).transact({'from': account})
        print(datetime.datetime.now(), account, amount, _hash)
        return render_template('success.html', message=f'Успешное списание средств. '
                                                       f'Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        print(datetime.datetime.now(), e)
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
        print(datetime.datetime.now(), account, estate_name, estate_address, estate_type, rooms, description, _hash)
        return render_template('success.html', message=f'Недвижимость успешно создана. '
                                                       f'Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        print(datetime.datetime.now(), e)
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
        print(datetime.datetime.now(), account, ad_id, price, _hash)
        return render_template('success.html', message=f'Объявление создано. '
                                                       f'Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        print(datetime.datetime.now(), e)
        return render_template('error.html', message=str(e))


@app.route('/purchase_estate', methods=['POST'])
def purchase_estate():
    try:
        account = web3.to_checksum_address(request.form['account'])
        estate_id = int(request.form['id'])
        _hash = contract.functions.purchaseEstate(estate_id).transact({'from': account})
        print(datetime.datetime.now(), account, estate_id, _hash)
        return render_template('success.html', message=f'Недвижимость успешно приобретена. '
                                                       f'Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        print(datetime.datetime.now(), e)
        return render_template('error.html', message=str(e))


@app.route('/update_estate', methods=['POST'])
@cache.cached(timeout=60)
def update_estate():
    try:
        account = web3.to_checksum_address(request.form['account'])
        estate_id = int(request.form['id'])
        estate_status = bool(request.form['status'])
        _hash = contract.functions.updateEstateStatus(estate_id, estate_status).transact({'from': account})
        print(datetime.datetime.now(), account, estate_id, estate_status,_hash)
        return render_template('success.html', message=f'Статус недвижимости обновлен. '
                                                       f'Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        print(datetime.datetime.now(), e)
        return render_template('error.html', message=str(e))


@app.route('/update_ad', methods=['POST'])
@cache.cached(timeout=60)
def update_ad():
    try:
        account = web3.to_checksum_address(request.form['account'])
        ad_id = int(request.form['id'])
        ad_status = int(request.form['status'])
        _hash = contract.functions.updateAdStatus(ad_id, ad_status).transact({'from': account})
        print(datetime.datetime.now(), account, ad_id, ad_status,_hash)
        return render_template('success.html', message=f'Статус объявления обновлен. '
                                                       f'Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        print(datetime.datetime.now(), e)
        return render_template('error.html', message=str(e))


@app.route('/get_all_ads', methods=['GET'])
@cache.cached(timeout=60)
def get_all_ads():
    try:
        ads = contract.functions.getAllAds().call()
        print(datetime.datetime.now(), ads)
        return render_template('ads.html', ads=ads)
    except Exception as e:
        print(datetime.datetime.now(), e)
        return render_template('error.html', message=str(e))


@app.route('/get_ad', methods=['GET'])
@cache.cached(timeout=60)
def get_ad():
    try:
        ad_id = request.args.get('ad_id', default=0, type=int)
        ad = contract.functions.getAd(ad_id).call()
        print(datetime.datetime.now(), ad_id, ad)
        return render_template('ad.html', ad=ad)
    except Exception as e:
        print(datetime.datetime.now(), e)
        return render_template('error.html', message=str(e))


@app.route('/get_all_estates', methods=['GET'])
@cache.cached(timeout=60)
def get_all_estates():
    try:
        estates = contract.functions.getAllEstates().call()
        print(datetime.datetime.now(), estates)
        return render_template('estates.html', estates=estates)
    except Exception as e:
        print(datetime.datetime.now(), e)
        return render_template('error.html', message=str(e))


@app.route('/get_estate', methods=['GET'])
@cache.cached(timeout=60)
def get_estate():
    try:
        estate_id = request.args.get('estate_id', default=0, type=int)
        estate = contract.functions.getEstate(estate_id).call()
        print(datetime.datetime.now(), estate_id, estate)
        return render_template('estate.html', estate=estate)
    except Exception as e:
        print(datetime.datetime.now(), e)
        return render_template('error.html', message=str(e))


if __name__ == '__main__':
    app.run(debug=True)
