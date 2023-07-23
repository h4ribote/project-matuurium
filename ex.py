import os
import datetime

def path(user_id: str,content: str) -> str:
  """
    データベースのファイルのパスを出力

    Parameters:
        user_id (str): ユーザーID\n
        content (str): データの種類

    Returns:
        str:'./db/user/{user_id}/{content}.txt'
  """
  return (f'./db/{user_id}/{content}.txt')

def path_dir(user_id: str) -> str:
  return ('./db/' + str(user_id) + '/')

def f_checker(user_id: str):
  is_dir = os.path.isdir(path_dir(str(user_id)))
  if is_dir:
    return True
  else:
    return False

def id_format(id: str):
  remove1 = "<@"
  remove2 = ">"
  id = id.replace(remove1, "")
  id = id.replace(remove2, "")
  return id

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
  with open(path("_system","log"), 'a') as log:
    log.write(f'{time} ({i}:"{a}") from <{f}> to <{t}>\n')