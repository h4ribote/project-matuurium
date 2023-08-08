import ex
import os


def register(id):
  if os.path.isdir(ex.path_dir(id)) == False:
    os.mkdir(ex.path_dir(id))
  regist_user = open(ex.path(id,"bank"),'w')
  regist_user.write('0')
  regist_user.close()
  regist_user = open(ex.path(id,"promo"),'w')
  regist_user.write('')
  regist_user.close()
  regist_user = open(ex.path(id,"lune"),'w')
  regist_user.write('0')
  regist_user.close()
  regist_user = open(ex.path(id,"order"),'w')
  regist_user.write('')
  regist_user.close()
  ex.log_maker(id,"system","regist","null")




def balance(id) -> int:
  with open(ex.path(id,"bank"), 'r') as file:
    content = file.read()
  return int(content)


def transfer(dest: str,amount: int,sourse: str):
  dest = str(ex.id_format(dest))


  if amount <= 0:
    return "不正な値です 送金額は0よりも大きい整数で入力してください"
  if ex.f_checker(sourse) == False:
    register(sourse)
  if ex.f_checker(dest) == False:
    return "送金先が見つかりません"
  if dest == sourse:
    return "送金元と送金先が同じです"
  if balance(sourse) < amount:
    return "残高が不足しています"


  dest_balance = (balance(dest))
  dest_balance = (dest_balance) + amount
  sourse_balance = (balance(sourse))
  sourse_balance = (sourse_balance) - amount

  with open(ex.path(sourse,"bank"), "w") as f:
    f.write(str(sourse_balance))
  with open(ex.path(dest,"bank"), "w") as f2:
    f2.write(str(dest_balance))
  ex.log_maker(sourse,dest,"transfer",amount)

  return (f'送金が完了しました\n送金先<@{dest}>:送金額 {amount}')