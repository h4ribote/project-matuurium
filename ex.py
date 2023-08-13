import os
import datetime
import bank

def path(user_id: str,content: str) -> str:
  user_id = id_format(user_id)
  """
    データベースのファイルのパスを出力

    Parameters:
        user_id (str): ユーザーID\n
        content (str): データの種類

    Returns:
        str:'./db/user/{user_id}/{content}.txt'
  """
  return (f'./db/user/{user_id}/{content}.txt')

def path_dir(user_id: str) -> str:
  user_id = id_format(user_id)
  return ('./db/user/' + str(user_id) + '/')

def f_checker(user_id: str):
  """
    データベースにファイルが存在するかを確認

    Parameters:
        user_id (str): ユーザーID

    Returns:
        bool:ファイルが存在する=True,ファイルが存在しない=False
  """
  user_id = id_format(user_id)
  is_dir = os.path.isdir(path_dir(str(user_id)))
  if is_dir:
    return True
  else:
    return False

def id_format(user_id: str) -> str:
  user_id = str(user_id)
  remove1 = "<@"
  remove2 = ">"
  user_id = user_id.replace(remove1, "")
  user_id = user_id.replace(remove2, "")
  return str(user_id)

def cl() -> str:
  activity = "Made by h4ribote"
  return str(activity)

def log_maker(f: str,t: str,i: str,a: str) -> str:
  """
    取引のログをタイムスタンプ付きで作成します

    Parameters:
        f (str): 取引の作成元\n
        t (str): 取引の対象\n
        i (str): 取引の種類(例:transfer)\n
        a (str): 取引量\n

    Returns:
        str:" <時間> (種類:"取引量") from <作成元> to <対象>\n" 
  """
  current_time = datetime.datetime.now()
  year = current_time.year
  month = current_time.month
  day = current_time.day
  hour = current_time.hour
  minute = current_time.minute
  second = current_time.second
  time = (f'<{year}-{month}-{day}  {hour}:{minute}:{second}>')
  with open(('./db/_system/log.txt'), 'a') as log:
    log.write(f'{time} ({i}:"{a}") from <{f}> to <{t}>\n')


def promo(code:str,user_id:str):
  if f_checker(user_id) == False:
    bank.register(user_id)
  code = code + "="
  user_id = id_format(user_id)
  with open("./db/_system/promo-codes.txt", 'r') as file:
    content = file.read()
  with open(path(user_id,"promo"), 'r') as file:
    used = file.read()
  if code in content:
    if (code + "used") in used:
      return "使用済みのコードです"
    else:
      index = content.find(code)
      if index != -1:
        # ターゲットの文字列が見つかった場合
        content0 = content[content.find(code):]
        reward = int(content0[content0.find("=")+1:content0.find("(")])
        times = int(content0[content0.find("(")+1:content0.find(")")])#times=使用回数
        if times == 0:
          return "既に使用可能な回数を超えたコードです"
        else:
          times = str(times - 1)
        bank.transfer(user_id,reward,"!admin-bank")
        reward = str(reward)
        with open((f'./db/user/{user_id}/promo.txt'), 'a') as text:
          text.write(f'{code}used\n')
        content1 = content[:content.find(code)]
        content2 = content0[:content0.find("(")+1]
        content3 = content0[content0.find(")"):]
        new_content = content1 + content2 + times + content3
        with open("./db/_system/promo-codes.txt", "w") as count:
          count.write(new_content)
        code = code.replace("=","")
        log_maker("system",user_id,"promo:" + code,reward)
        return ("登録が完了しました\ncode:" + code + " 報酬:" + reward)
      else:
        return "不正なコードです"
  else:
    return "コードが存在しません"


def time_stamp() -> str:
  current_time = datetime.datetime.now()
  year = current_time.year
  month = current_time.month
  day = current_time.day
  hour = current_time.hour
  minute = current_time.minute
  second = current_time.second
  time = (f'{year}-{month}-{day}  {hour}:{minute}:{second}')
  return time
