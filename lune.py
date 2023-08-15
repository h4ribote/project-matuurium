import ex
import bank
import time
import random
import datetime



def balance(user_id) -> int:

  with open(ex.path(user_id,"lune"), 'r') as file:
    content = file.read()

  return int(content)



def transfer(sourse: str,dest: str,amount: int):
  if ex.f_checker(sourse) == False:
    bank.register(sourse)
  if ex.f_checker(dest) == False:
    return "送金先が見つかりません"
  if amount <= 0:
    return "不正な値です 送金額は0よりも大きい整数で入力してください"
  if dest == sourse:
    return "送金元と送金先が同じです"
  sourse_balance = balance(sourse)
  dest_balance = balance(dest)
  

  if sourse_balance < amount:
    return "残高が不足しています"
  dest_balance = dest_balance + amount
  sourse_balance = sourse_balance - amount
  with open(ex.path(sourse,"lune"), 'w') as f:
    f.write(str(sourse_balance))
  with open(ex.path(dest,"lune"), 'w') as f2:
    f2.write(str(dest_balance))
  ex.log_maker(sourse,dest,"lune_transfer",f"{amount}lune")

  return (f'送金が完了しました\n送金先{dest}:送金額 {amount}')



def pay(sourse,dest,amount):

  sourse_balance = balance(sourse)
  dest_balance = balance(dest)
  sourse_balance = sourse_balance - amount
  dest_balance = dest_balance + amount

  with open(ex.path(sourse,"lune"), "w") as f:
    f.write(str(sourse_balance))
  with open(ex.path(dest,"lune"), "w") as f:
    f.write(str(dest_balance))

  return "complete"



def make_buy_order(price,amount,user_id: str):

  user_id = str(user_id)
  id_rnd = str(random.randint(0,9999))
  id_time = time.time()
  id_time = str(id_time)
  id_user = str(user_id[len(user_id) - 3 :])
  id_time = str(id_time[id_time.find(".") - 4:id_time.find(".")])
  trade_id = (id_user + id_time + id_rnd)
  write_line = (f'{trade_id}.{user_id}({price},{amount})')


  with open("./db/_system/exchange_buy.txt", 'a') as file:
    file.write(write_line)

  return trade_id



def order_loger(user_id: str,order_id: str,order: str):
  """
    注文のログを管理します

    Parameters:
        user_id (str) : uid\n
        order_id (str) : order_id\n
        order (str) : buy(新規買い)sell(新規売り)contract(約定)cancel(キャンセル)
    
    Returns:
        形式: <time>order_id[order-condition.time](price,amount)

  """
  with open(ex.path(user_id,"order"), 'r') as file:
    content = file.read()
  if order == "buy" or order == "sell":
    with open("./db/_system/exchange_"+order+".txt", 'r') as file:
      content_0 = file.read()



  current_time = datetime.datetime.now()
  year = current_time.year
  month = current_time.month
  day = current_time.day
  hour = current_time.hour
  minute = current_time.minute
  second = current_time.second
  time = (f'{year}-{month}-{day}  {hour}:{minute}:{second}')


  if order == "buy" or order == "sell":#新しくログ作成
    content_1 = content_0[content_0.find(order_id):]
    price = content_1[content_1.find("(")+1:content_1.find(",")]
    amount = content_1[content_1.find(",")+1:content_1.find(")")]
    content_2 = (f'<{time}>{order_id}[{order}-]({price},{amount})')
    log = content_2 + "\n"
    with open(ex.path(user_id,"order"), "a") as log_file:
      log_file.write(log)
    return

  elif order == "contract" or order == "cancel":#ログ編集
    content_1 = content[content.find(order_id):]
    content_2 = content[:content.find(order_id)]#前の注文まで
    content_3 = content_1[content_1.find(']'):]#"]"以降+次の注文から
    content_4 = content_1[:content_1.find('-')+1]
    log = content_2 + content_4 + order + "." + time + content_3

    with open(ex.path(user_id,"order"), "w") as log_file:
      log_file.write(log)
    return



def make_sell_order(price,amount,user_id: str):

  user_id = str(user_id)
  id_rnd = str(random.randint(0,9999))
  id_time = time.time()
  id_time = str(id_time)
  id_user = str(user_id[len(user_id) - 3 :])
  id_time = str(id_time[id_time.find(".") - 4:id_time.find(".")])
  trade_id = (id_user + id_time + id_rnd)
  write_line = (f'{trade_id}.{user_id}({price},{amount})')


  with open("./db/_system/exchange_sell.txt", 'a') as file:
    file.write(write_line)

  return trade_id



def change_buy_order(trade_id,price,amount,user_id):

  with open("./db/_system/exchange_buy.txt", 'r') as file:
    content_raw = file.read()

  content_2 = content_raw[content_raw.find(trade_id):]
  content_3 = content_2[:content_2.find(")")+1]
  new_order = (f'{trade_id}.{user_id}({price},{amount})')
  modified_content = content_raw.replace(content_3, new_order)

  with open("./db/_system/exchange_buy.txt", "w") as f:
    f.write(str(modified_content))

  return "complete"



def change_sell_order(trade_id,price,amount,user_id):

  with open("./db/_system/exchange_sell.txt", 'r') as file:
    content_raw = file.read()

  content_2 = content_raw[content_raw.find(trade_id):]
  content_3 = content_2[:content_2.find(")")+1]
  new_order = (f'{trade_id}.{user_id}({price},{amount})')
  modified_content = content_raw.replace(content_3, new_order)

  with open("./db/_system/exchange_sell.txt", "w") as f:
    f.write(str(modified_content))

  return "complete"



def delete_sell_order(trade_id: str,trade_user: str):

  with open("./db/_system/exchange_sell.txt", 'r') as file:
    content_raw = file.read()

  content_2 = content_raw[content_raw.find(trade_id):]
  content_3 = content_2[:content_2.find(")") + 1]
  modified_content = content_raw.replace(content_3, "")

  with open("./db/_system/exchange_sell.txt", 'w') as f:
    f.write(str(modified_content))
  
  return "complete"



def delete_buy_order(trade_id: str,trade_user: str):

  with open("./db/_system/exchange_buy.txt", 'r') as file:
    content_raw = file.read()

  content_2 = content_raw[content_raw.find(trade_id):]
  content_3 = content_2[:content_2.find(")") + 1]
  modified_content = content_raw.replace(content_3, "")

  with open("./db/_system/exchange_buy.txt", 'w') as f:
    f.write(str(modified_content))
  
  return "complete"



def sell(_price: int,_amount: int,_user_id):

  if _price <= 0 or _amount <= 0:
    return "不正な値です 注文額は0よりも大きい整数で入力してください"

  if ex.f_checker == False:
    bank.register(_user_id)
  
  if balance(_user_id) < _price*_amount:
    return (f"残高が不足しています\nlune残高:{balance(_user_id)}")

  with open("./db/_system/exchange_buy.txt", 'r') as file:
    content = file.read()
  
  search1 = "("
  search2 = ")"
  search3 = ","
  search4 = "."
  total_amount = int(_amount) #残り売却希望量
  i = 0
  ii = 0
  sold_lune = 0
  low_price = 0
  low_amount = 0
  low_trade = ""
  low_user = ""
  searched = 0

  while True:
    if content.find(search1) != -1 or searched == 1:#ここか最安値検索
      if searched == 1:#値リセット
        low_price = 0
        low_amount = 0
        low_trade = ""
        low_user = ""
        with open("./db/_system/exchange_buy.txt", 'r') as file:
          content = file.read()
        searched = 0
      trade_id = content[:content.find(search4)]
      user = content[content.find(search4) + 1:content.find(search1)]
      price = int(content[content.find(search1) + 1:content.find(search3)])
      amount = int(content[content.find(search3) + 1:content.find(search2)])
      if low_price > price or low_trade == "":
        low_price = price
        low_amount = int(amount)
        low_trade = trade_id
        low_user = user
      content = content[content.find(search2) + 1:]#最安値検索ここまで,検索済み部分削除
    else:
      searched = 1
      print(f'total_amount,{total_amount}:low_amount{low_amount}')
      if low_price <= _price and not(low_price == 0):#最安値が売却希望よりも安かったら
        if int(total_amount) >= int(low_amount):#残り購入希望量と同じか希望量のほうが多かったら
        #購入処理
          transfer(_user_id,low_user,low_amount*low_price)
          bank.transfer(low_user,low_amount,"exchange")
          delete_buy_order(low_trade,low_user)
          total_amount = total_amount - low_amount
          sold_lune = sold_lune + (low_amount*low_price)
          order_loger(low_user,low_trade,"contract")
          ii = 1
          if total_amount == 0:
            with open(f"./db/user/{_user_id}/order.txt", 'a') as file:
              file.write(f"<{ex.time_stamp}>{low_trade}[contract.{ex.time_stamp}]({low_price},{_amount})")
            return (f'売却が完了しました\n売却量:{sold_lune}lune\n売却価格:{low_amount}mtri')
        else:
          low_amount2 = low_amount - total_amount
          transfer(_user_id,low_user,total_amount*low_price)
          bank.transfer(_user_id,total_amount,"exchange")
          change_buy_order(low_trade,low_price,low_amount2,low_user)
          sold_lune = sold_lune + (total_amount*low_price)
          order_loger(low_user,low_trade,"contract")
          with open(f"./db/user/{_user_id}/order.txt", 'a') as file:
            file.write(f"<{ex.time_stamp}>{low_trade}[contract.{ex.time_stamp}]({low_price},{_amount})")
          return (f'売却が完了しました\n売却量:{sold_lune}lune\n売却価格:{_amount}mtri')
      else:#最安値が売却希望の値段より高い=即時売却可能な注文がない
        #注文を作成
        _amount_fin = total_amount
        user_trade_id = make_sell_order(_price,_amount_fin,_user_id)
        _amount_lune = _amount_fin*_price
        _purc = (_amount - _amount_fin) * _price
        transfer(_user_id,"exchange",_amount_lune)
        order_loger(_user_id,user_trade_id,"sell")
        msg1 = "注文が完了しました"
        msg2 = (f'注文ID:{user_trade_id}')
        msg3 = (f'売却予定量:{_amount_lune}lune')
        msg4 = "注文をキャンセルしたい場合は/cancel_orderを実行してください"
        msg5 = (f'注文の内、{_purc}luneは約定済みです')
        if ii == 0:
          return (f'{msg1}\n{msg2}\n{msg3}\n{msg4}')
        else:
          return (f'{msg1}\n{msg2}\n{msg3}\n{msg5}\n{msg4}')




def buy(_price: int,_amount: int,_user_id):

  if _price <= 0 or _amount <= 0:
    return "不正な値です 注文額は0よりも大きい整数で入力してください"

  if ex.f_checker == False:
    bank.register(_user_id)

  if bank.balance(_user_id) < _amount:
    return "残高が不足しています"

  with open("./db/_system/exchange_sell.txt", 'r') as file:
    content = file.read()
  
  search1 = "("
  search2 = ")"
  search3 = ","
  search4 = "."
  total_amount = _amount #残り購入希望量
  i = 0
  ii = 0
  bought_lune = 0
  high_price = 0
  high_amount = 0
  high_trade = ""
  high_user = ""
  searched = 0

  while i == 0:
    if content.find(search1) != -1 or searched == 1:#ここから最高値検索
      if searched == 1:#値リセット
        high_price = 0
        high_amount = 0
        high_trade = ""
        high_user = ""
        with open("./db/_system/exchange_sell.txt", 'r') as file:
          content = file.read()
        searched = 0
      trade_id = content[:content.find(search4)]
      user = content[content.find(search4) + 1:content.find(search1)]
      price = int(content[content.find(search1) + 1:content.find(search3)])
      amount = int(content[content.find(search3) + 1:content.find(search2)])
      if high_price < price or high_trade == "":
        high_price = price
        high_amount = amount
        high_trade = trade_id
        high_user = user
      content = content[content.find(search2) + 1:]#最高値検索ここまで,検索済み部分削除
    else:
      searched = 1
      if high_price >= _price:#最高値が購入希望の値段より高かったら
        if total_amount >= high_amount:#残り購入希望量と同じか希望量のほうが多かったら
        #購入処理
          transfer("exchange",_user_id,high_amount*high_price)
          bank.transfer(high_user,high_amount,_user_id)
          delete_sell_order(high_trade,high_user)
          total_amount = total_amount - high_amount
          bought_lune = bought_lune + (high_amount*high_price)
          order_loger(high_user,high_trade,"contract")
          ii = 1
          if total_amount == 0:
            with open(f"./db/user/{_user_id}/order.txt", 'a') as file:
              file.write(f"<{ex.time_stamp}>{high_trade}[contract.{ex.time_stamp}]({high_price},{_amount})")
            return (f'購入が完了しました\n購入量:{bought_lune}lune\n購入価格:{high_amount}mtri')
        else:
          high_amount2 = high_amount - total_amount
          transfer("exchange",_user_id,total_amount*high_price)
          bank.transfer(high_user,total_amount,_user_id)
          change_sell_order(high_trade,high_price,high_amount2,high_user)
          bought_lune = bought_lune + (total_amount*high_price)
          order_loger(high_user,high_trade,"contract")
          with open(f"./db/user/{_user_id}/order.txt", 'a') as file:
            file.write(f"<{ex.time_stamp}>{high_trade}[contract.{ex.time_stamp}]({high_price},{_amount})")
          return (f'購入が完了しました\n購入量:{bought_lune}lune\n購入価格:{_amount}mtri')
      else:#最高値が購入希望の値段より安い=即時購入可能な注文がない
        #注文を作成
        _amount_fin = total_amount
        user_trade_id = make_buy_order(_price,_amount_fin,_user_id)
        _amount_lune = _amount_fin*_price
        _purc = (_amount - _amount_fin) * _price
        bank.transfer("exchange",_amount_fin,_user_id)
        order_loger(_user_id,user_trade_id,"buy")
        msg1 = "注文が完了しました"
        msg2 = (f'注文ID:{user_trade_id}')
        msg3 = (f'購入予定量:{_amount_lune}lune')
        msg4 = "注文をキャンセルしたい場合は/cancel_orderを実行してください"
        msg5 = (f'注文の内、{_purc}luneは約定済みです')
        if ii == 0:
          return (f'{msg1}\n{msg2}\n{msg3}\n{msg4}')
        else:
          return (f'{msg1}\n{msg2}\n{msg3}\n{msg5}\n{msg4}')



def cancel_order(user_id: str,order: str,order_id: str):
  if not (order == "buy" or order == "sell"):
    return "orderはbuy(買い注文)かsell(売り注文)を入力してください"
  
  with open("./db/_system/exchange_" + order + ".txt", 'r') as file:
    content_raw = file.read()
  user_id = str(user_id)
  if content_raw.find(order_id) != -1:
    check_uid = content_raw[content_raw.find(order_id):]
    check_uid = str(check_uid[check_uid.find(".") + 1:check_uid.find("(")])
  else:
    return "注文IDが見つかりません"
  if check_uid != user_id:
    print(check_uid + ":" + user_id)
    return "この注文はキャンセルできません"
  
  if order == "buy":
    delete_buy_order(order_id,user_id)
  elif order == "sell":
    delete_sell_order(order_id,user_id)
  order_loger(user_id,order_id,"cancel")
  return (f'注文({order_id})をキャンセルしました')



def show_order(user_id: str,num: int):

  msg = "注文作成日時/注文ID/注文状態/価格(lune)/取引量(mtri)\n"

  with open(f"./db/user/{user_id}/order.txt", 'r') as file:
    content = file.read()

  if num <= 0:
    i = -1
  else:
    i = num

  while content.find("<") != -1 and i != 0:
    
    line_order = ""
    time_content = ""
    order_content = ""
    condition_content = ""
    condition_time = ""

    line_order = content[:content.find(")")]
    time_content = line_order[content.find("<")+1:content.find(">")]
    order_content = line_order[content.find(">")+1:content.find("[")]
    condition_content = line_order[content.find("[")+1:content.find("]")]
    if condition_content.find(".") != -1:
      condition_content2 = condition_content[:condition_content.find(".")]
      condition_time = condition_content[condition_content.find(".")+1:content.find("]")]
      condition_content = (f"{condition_content2}({condition_time})")
    price_content = line_order[content.find("(")+1:content.find(",")]
    amount_content = line_order[content.find(",")+1:]

    msg = (f"{msg}{time_content}/{order_content}/{condition_content}\n{price_content}lune/{amount_content}mtri\n")
    content = content[content.find(")")+1:]
    i = i - 1
  return(msg)



def exchange_rate() -> str:
  
  lowest = 0
  lowest_amount = 0
  highest = 0
  highest_amount = 0
  i = 0
  ii = 0

  with open(f"./db/_system/exchange_buy.txt", 'r') as data_buy:
    data_buy = data_buy.read()
  with open(f"./db/_system/exchange_sell.txt", 'r') as data_sell:
    data_sell = data_sell.read()
  

  while i == 0:# data_buy.find(")") != -1
    if data_buy.find(")") != -1:
      ii = 1 # 注文の存在の確認
      new_data_price = data_buy[data_buy.find("(")+1:data_buy.find(",")]
      new_data_amount = data_buy[data_buy.find(",")+1:data_buy.find(")")]
      new_data_price = int(new_data_price)
      new_data_amount = int(new_data_amount)
      data_buy = data_buy[data_buy.find(")")+1:]
      if lowest >= new_data_price or (lowest==new_data_price and lowest_amount < new_data_amount) or lowest == 0:
        lowest = new_data_price
        lowest_amount = new_data_amount
    elif ii == 0:
      output = "売り:注文なし\n"
      i = 1
    else:
      output = (f"売り:{lowest}lune => 1mtri\n")
      i = 1
  i = 0
  ii = 0
  while i == 0:
    if data_sell.find(")") != -1:
      ii = 1
      new_data_price = int(data_sell[data_sell.find("(")+1:data_sell.find(",")])
      new_data_amount = int(data_sell[data_sell.find(",")+1:data_sell.find(")")])
      new_data_price = int(new_data_price)
      new_data_amount = int(new_data_amount)
      data_sell = data_sell[data_sell.find(")")+1:]
      if highest <= new_data_price or (highest==new_data_price and highest_amount < new_data_amount) or highest ==0:
        highest = new_data_price
        highest_amount = new_data_amount
    elif ii == 0:
      output = output + "買い:注文なし"
      i = 1
    else:
      output = output + (f"買い:1mtri => {highest}lune")
      i = 1
  
  return (output)



def order_list() -> str:
  i = 0
  ii = 0
  output = "価格(lune)/数量(mtri)\n**売り**\n"
  list_order = {}

  with open(f"./db/_system/exchange_buy.txt", 'r') as data_buy:
    data_buy = data_buy.read()
  with open(f"./db/_system/exchange_sell.txt", 'r') as data_sell:
    data_sell = data_sell.read()
  
  while i == 0:
    if data_sell.find(")") != -1:
      ii = 1
      new_data_price = data_sell[data_sell.find("(")+1:data_sell.find(",")]
      new_data_amount = data_sell[data_sell.find(",")+1:data_sell.find(")")]
      data_sell = data_sell[data_sell.find(")")+1:]

      if new_data_price in list_order:
        list_order[str(new_data_price)] += int(new_data_amount)
      else:
        list_order[str(new_data_price)] = int(new_data_amount)

    elif ii == 1:
      i = 1
      sorted_items = sorted(list_order.items(), key=lambda x: x[1], reverse=True)
      list_order = dict(sorted_items)

      for price, amount in list_order.items():
        output += (f"{price}/{amount}\n")
    
    else:
      output += "注文なし\n"
      i = 1
  

  i = 0
  ii = 0
  output += "**買い**\n"
  
  
  while i == 0:
    if data_buy.find(")") != -1: # 注文の存在の確認
      ii = 1
      new_data_price = data_buy[data_buy.find("(")+1:data_buy.find(",")]
      new_data_amount = data_buy[data_buy.find(",")+1:data_buy.find(")")]
      data_buy = data_buy[data_buy.find(")")+1:]

      if new_data_price in list_order:
        list_order[str(new_data_price)] += int(new_data_amount)
      else:
        list_order[str(new_data_price)] = int(new_data_amount)
    elif ii == 1:
      i = 1
      sorted_items = sorted(list_order.items(), key=lambda x: x[1])
      list_order = dict(sorted_items)

      for price, amount in list_order.items():
        output += (f"{price}/{amount}\n")
    else:
      output += "注文なし\n"
      i = 1

  
  return (output)
"""
This software and its source code are provided "as is," without warranty of any kind, express or implied. The author of this software shall not be held liable for any damages arising from the use of this software.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to use the Software for non-commercial purposes only, including the rights to use, copy, modify, merge, publish, and distribute the Software, provided that the following conditions are met:

1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

2. Any use of the Software, in whole or in part, for the purpose of creating, operating, or maintaining a bot (automated software application) that interfaces with third-party platforms, services, or APIs (Application Programming Interfaces) as a bot user is strictly prohibited without explicit written permission from the author.

3. Redistributions of the Software, in whole or in part, must retain the above copyright notice, this permission notice, and the disclaimer contained herein.

For the avoidance of doubt, creating, operating, or maintaining a bot that interfaces with third-party platforms, services, or APIs as a bot user requires obtaining a separate, explicit written permission from the author.

For commercial use, please contact h4ribote.

h4ribote's
email: tyche.d0000@gmail.com
discord: h4ribote#0
"""