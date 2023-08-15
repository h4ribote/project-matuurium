import ex
import lune
import requests



def get_price() -> int:
    response = requests.get("https://api.bybit.com/v2/public/tickers", params={"symbol": "BTCUSDT"})

    if response.status_code == 200:
        data = response.json()
        if data['ret_code'] == 0:
            price = str(data['result'][0]['last_price'])
            price = price[:price.find(".")]
            return int(price)
        else:
            print("API Error:", data['ret_msg'])
            return None
    else:
        return None


def sync_price():
    _price = get_price()
    if _price == None:
        return False
    else:
        with open("./db/_system/btc_buy.txt", "w") as file:
            file.write(str(_price))
        with open("./db/_system/btc_sell.txt", "w") as file:
            file.write(str(_price - 5))
        return True


def exchange_rate() -> str:
     _buy = price_buy()
     _sell = price_sell()
     return (f'買い:{_buy}\n売り:{_sell}')


def price_sell() -> int:
    with open("./db/_system/btc_sell.txt", 'r') as file:
        content = file.read()
    return int(content)


def price_buy() -> int:
    with open("./db/_system/btc_buy.txt", 'r') as file:
        content = file.read()
    return int(content)


def balance(user_id) -> int:
    with open(ex.path(user_id,"btc"),"r") as file:
        content = file.read()
    return content


def sell(user_id,amount) -> str:
    _price = price_sell()
    _btc_balance = int(balance(user_id))
    _lune_balance = int(lune.balance(user_id))
    if _btc_balance < amount:
        return "btcが不足しています"
    with open(ex.path(user_id,"btc"), "w") as file:
            file.write(str(_btc_balance - amount))
    with open(ex.path(user_id,"lune"), "w") as file:
            file.write(str(_lune_balance+(amount*_price)))
    return (f"btcを売却しました\n約定:{ex.time_stamp()}\n価格:{_price}\n数量:{amount}")


def buy(user_id,amount: int) -> str:
    amount = int(amount)
    _price = price_buy()
    _balance = int(lune.balance(user_id))
    _btc_balance = int(balance(user_id))
    
    print (f'{balance(user_id)}\n{amount}\n{_price}\n{_balance}')

    if _balance < (amount*_price):
        return "luneが不足しています"
    with open(ex.path(user_id,"btc"), "w") as file:
            _input_balance = _btc_balance + amount
            file.write(str(_input_balance))
    with open(ex.path(user_id,"lune"), "w") as file:
            _input_balance = _balance-(amount*_price)
            file.write(str(_input_balance))
    return (f"btcを購入しました\n約定:{ex.time_stamp()}\n価格:{_price}\n数量:{amount}")