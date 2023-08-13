<div style="text-align:center">
<h1>
Project-matuutium
</h1>
</div>

<img src="https://img.shields.io/badge/Python-3.11.4-blue" height="20" alt="Version-of-Python">

# どんなボット？
discordでFXっぽいことができるボット

matuurium(mtri)とchihalune(lune)と呼ばれる2種類の通貨をdiscordのユーザー間で取引できる

ビットコイン等の実在する通貨の変動に対応するものも制作予定

# 使い方は？年収は？彼女はいるの？
調べてみました！()

.envにボットのトークンを貼り付けてmain.pyを実行<br>
(隠しファイルが表示できる状態にしておきましょう)

全ユーザーは、どのコマンドよりも先に/registを実行してください<br>
コマンドを実行したときエラーが出る割合が減ります

# ファイル構成
main.py - 名前の通りメインファイル。 .envにトークンを貼った後に起動する

bank.py - 主にmtriの操作に使われる関数

lune.py - 主にluneの操作に使われる関数

ex.py - さまざまな操作の関数

db/<br>
　　_system/<br>
　　　　promo-codes.txt - プロモーションコードに関する情報<br>
　　　　log.txt - 送金等の操作のログ<br>
　　user/ - 各ユーザーの残高・取引情報

# コマンド一覧

/regist - "/db/user/"にユーザー用のフォルダを作る<br>
　　　　　ほかのコマンドを使用してもエラーが出る場合はまずこのコマンドを実行してください

/balance - mtriの残高を表示

/lune-balance - luneの残高を表示

/transfer - mtriをほかのユーザーに送金

/promo-code - プロモーションコードを使用

/order_buy & /order_sell - 注文を作成<br>
　　注文は注文価格をlune、数量をmtriで指定<br>
　　例:100luneを1mtriにしたい ==> /order_sell price 100 amount 1

# 使用するうえでの注意点
LICENSE.mdに記載されている内容を守って利用してください

ライセンスの内容を日本語でざっくりと説明

著作者からの許可なしの使用、改変、再配布はNG<br>
使用したかったら連絡入れること(そもそも使いたい人いるのか)

著作者、連絡先<br>
h4ribote<br>
Discord: h4ribote#0
