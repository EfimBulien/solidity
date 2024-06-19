import datetime
import logging

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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    logger.info('Rendering home page.')
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        password = request.form['password']
        if check(password):
            new_account = web3.geth.personal.new_account(password)
            logger.info(f'{datetime.datetime.now()} - Account created: {new_account}')
            return render_template('success.html', message=f'Новый аккаунт создан: {new_account}')
        else:
            logger.warning(f'{datetime.datetime.now()} - Incorrect password attempt.')
            return render_template('error.html', message='Пароль не соответсвует требованиям.')
    logger.info('Rendering registration page.')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            public_key = request.form['key']
            password = request.form['password']
            web3.geth.personal.unlock_account(public_key, password)
            logger.info(f'{datetime.datetime.now()} - Account unlocked: {public_key}')
            return redirect(url_for('dashboard', account=public_key))
        except Exception as e:
            logger.error(f'{datetime.datetime.now()} - Error during login: {e}')
            return render_template('error.html', message=str(e))
    logger.info('Rendering login page.')
    return render_template('login.html')


@app.route('/dashboard/<account>')
@cache.cached(timeout=60)
def dashboard(account):
    logger.info(f'{datetime.datetime.now()} - Accessing dashboard for account: {account}')
    return render_template('dashboard.html', account=account)


@app.route('/balance/<account>')
@cache.cached(timeout=60)
def balance(account):
    try:
        account_balance = contract.functions.getBalance().call({'from': account})
        logger.info(f'{datetime.datetime.now()} - Retrieved balance for account {account}: {account_balance}')
        return render_template('balance.html', balance=account_balance)
    except Exception as e:
        logger.error(f'{datetime.datetime.now()} - Error retrieving balance for account {account}: {e}')
        return render_template('error.html', message=str(e))


@app.route('/withdraw', methods=['POST'])
@cache.cached(timeout=60)
def withdraw():
    try:
        account = web3.to_checksum_address(request.form['account'])
        amount = int(request.form['amount'])
        if amount <= 0:
            logger.warning(f'{datetime.datetime.now()} - Invalid withdrawal amount: {amount}')
            return render_template('error.html', message='Сумма должна быть больше 0.')
        _hash = contract.functions.withdraw(amount).transact({'from': account})
        logger.info(
            f'{datetime.datetime.now()} - Withdrawal successful for account {account}: {amount}, transaction hash: {_hash.hex()}')
        return render_template('success.html', message=f'Успешное списание средств. Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        logger.error(f'{datetime.datetime.now()} - Error during withdrawal for account {account}: {e}')
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
        logger.info(
            f'{datetime.datetime.now()} - Estate created by account {account}: {estate_name}, {estate_address}, type: {estate_type}, rooms: {rooms}, description: {description}, transaction hash: {_hash.hex()}')
        return render_template('success.html', message=f'Недвижимость успешно создана. Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        logger.error(f'{datetime.datetime.now()} - Error creating estate for account {account}: {e}')
        return render_template('error.html', message=str(e))


@app.route('/create_ad', methods=['POST'])
@cache.cached(timeout=60)
def create_ad():
    try:
        account = web3.to_checksum_address(request.form['account'])
        ad_id = int(request.form['id'])
        price = int(request.form['price'])
        if price <= 0:
            logger.warning(f'{datetime.datetime.now()} - Invalid ad price: {price}')
            return render_template('error.html', message='Цена должна быть больше 0.')
        _hash = contract.functions.createAd(ad_id, price).transact({'from': account})
        logger.info(
            f'{datetime.datetime.now()} - Ad created by account {account}: ad_id: {ad_id}, price: {price}, transaction hash: {_hash.hex()}')
        return render_template('success.html', message=f'Объявление создано. Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        logger.error(f'{datetime.datetime.now()} - Error creating ad for account {account}: {e}')
        return render_template('error.html', message=str(e))


@app.route('/purchase_estate', methods=['POST'])
def purchase_estate():
    try:
        account = web3.to_checksum_address(request.form['account'])
        estate_id = int(request.form['id'])
        _hash = contract.functions.purchaseEstate(estate_id).transact({'from': account})
        logger.info(
            f'{datetime.datetime.now()} - Estate purchased by account {account}: estate_id: {estate_id}, transaction hash: {_hash.hex()}')
        return render_template('success.html',
                               message=f'Недвижимость успешно приобретена. Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        logger.error(f'{datetime.datetime.now()} - Error purchasing estate for account {account}: {e}')
        return render_template('error.html', message=str(e))


@app.route('/update_estate', methods=['POST'])
@cache.cached(timeout=60)
def update_estate():
    try:
        account = web3.to_checksum_address(request.form['account'])
        estate_id = int(request.form['id'])
        estate_status = bool(request.form['status'])
        _hash = contract.functions.updateEstateStatus(estate_id, estate_status).transact({'from': account})
        logger.info(
            f'{datetime.datetime.now()} - Estate status updated by account {account}: estate_id: {estate_id}, status: {estate_status}, transaction hash: {_hash.hex()}')
        return render_template('success.html', message=f'Статус недвижимости обновлен. Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        logger.error(f'{datetime.datetime.now()} - Error updating estate status for account {account}: {e}')
        return render_template('error.html', message=str(e))


@app.route('/update_ad', methods=['POST'])
@cache.cached(timeout=60)
def update_ad():
    try:
        account = web3.to_checksum_address(request.form['account'])
        ad_id = int(request.form['id'])
        ad_status = int(request.form['status'])
        _hash = contract.functions.updateAdStatus(ad_id, ad_status).transact({'from': account})
        logger.info(
            f'{datetime.datetime.now()} - Ad status updated by account {account}: ad_id: {ad_id}, status: {ad_status}, transaction hash: {_hash.hex()}')
        return render_template('success.html', message=f'Статус объявления обновлен. Хэш транзакции: {_hash.hex()}')
    except Exception as e:
        logger.error(f'{datetime.datetime.now()} - Error updating ad status for account {account}: {e}')
        return render_template('error.html', message=str(e))


@app.route('/get_all_ads', methods=['GET'])
@cache.cached(timeout=60)
def get_all_ads():
    try:
        ads = contract.functions.getAllAds().call()
        logger.info(f'{datetime.datetime.now()} - Retrieved all ads: {ads}')
        return render_template('ads.html', ads=ads)
    except Exception as e:
        logger.error(f'{datetime.datetime.now()} - Error retrieving all ads: {e}')
        return render_template('error.html', message=str(e))


@app.route('/get_ad', methods=['GET'])
@cache.cached(timeout=60)
def get_ad():
    try:
        ad_id = request.args.get('ad_id', default=0, type=int)
        ad = contract.functions.getAd(ad_id).call()
        logger.info(f'{datetime.datetime.now()} - Retrieved ad {ad_id}: {ad}')
        return render_template('ad.html', ad=ad)
    except Exception as e:
        logger.error(f'{datetime.datetime.now()} - Error retrieving ad {ad_id}: {e}')
        return render_template('error.html', message=str(e))


@app.route('/get_all_estates', methods=['GET'])
@cache.cached(timeout=60)
def get_all_estates():
    try:
        estates = contract.functions.getAllEstates().call()
        logger.info(f'{datetime.datetime.now()} - Retrieved all estates: {estates}')
        return render_template('estates.html', estates=estates)
    except Exception as e:
        logger.error(f'{datetime.datetime.now()} - Error retrieving all estates: {e}')
        return render_template('error.html', message=str(e))


@app.route('/get_estate', methods=['GET'])
@cache.cached(timeout=60)
def get_estate():
    try:
        estate_id = request.args.get('estate_id', default=0, type=int)
        estate = contract.functions.getEstate(estate_id).call()
        logger.info(f'{datetime.datetime.now()} - Retrieved estate {estate_id}: {estate}')
        return render_template('estate.html', estate=estate)
    except Exception as e:
        logger.error(f'{datetime.datetime.now()} - Error retrieving estate {estate_id}: {e}')
        return render_template('error.html', message=str(e))


if __name__ == '__main__':
    app.run(debug=True)
