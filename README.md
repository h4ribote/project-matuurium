<div style="text-align:center">
<h1>
Project-matuutium
</h1>
</div>
https://img.shields.io/badge/Python-{version}-blue

# どんなボット？
discordでFXっぽいことができるボット
matuurium(mtri)とchihalune(lune)と呼ばれる2種類の通貨をdiscordのユーザー間で取引できる
ビットコイン等の実在する通貨の変動に対応するものも制作予定

# 使い方は？年収は？彼女はいるの？
調べてみました！()

.envにボットのトークンを貼り付けてmain.pyを実行

# ファイル構成

main.py - 名前の通りメインファイル。 .envにトークンを貼った後に起動する

bank.py - 主にmtriの操作に使われる関数

lune.py - 主にluneの操作に使われる関数

ex.py - さまざまな操作の関数

db/
  _system/
         promo-codes.txt - プロモーションコードに関する情報
         log.txt - 送金等の操作のログ
  user/ - 各ユーザーの残高・取引情報

# コマンド一覧

/regist - "/db/user/"にユーザー用のフォルダを作る

/balance - mtriの残高を表示

/lune-balance - luneの残高を表示

/transfer - mtriをほかのユーザーに送金

/promo-code - プロモーションコードを使用

/order_buy & /order_sell - 注文を作成
    注文は注文価格をlune、数量をmtriで指定
    例:100luneを1mtriにしたい ==> /order_sell price 100 amount 1

# 作成者
h4ribote
Discord: h4ribote#0