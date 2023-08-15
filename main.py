import os
from dotenv import load_dotenv
import discord
from discord import app_commands
import ex
import bank
import lune
import btc

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


@client.event
async def on_ready():
  print ('成功しました')
  await client.change_presence(activity=discord.Game(name=str(ex.cl())))
  print(f'" {client.user} "としてログイン中')
  await tree.sync()



@tree.command(name="ping", description='とっても簡素なつくりのコマンド 実行したとき"pong"と返ってこなかったらボットは恐らく重度のエラーを吐いています')
async def ping_command(interaction: discord.Interaction):
  await interaction.response.send_message("pong",ephemeral=True)


@tree.command(name="regist", description="データベースに情報を登録します")
async def regist_command(interaction: discord.Interaction):
  if ex.f_checker(interaction.user.id):
    await interaction.response.send_message("どうやら既に登録してるようです 忘れたのですか？",ephemeral=True)
  else:
    bank.register(interaction.user.id)
    await interaction.response.send_message('登録が完了しました',ephemeral=True)


@tree.command(name="mtri-balance", description="matuuriumの残高を確認します")
async def balance_command(interaction: discord.Interaction):
  user_balance = bank.balance(interaction.user.id)
  await interaction.response.send_message(f'あなたの残高は{user_balance}mtriです',ephemeral=True)


@tree.command(name="lune-balance", description="chihaluneの残高を確認します")
async def lune_balance_command(interaction: discord.Interaction):
  user_lune_balance = lune.balance(interaction.user.id)
  await interaction.response.send_message(f'あなたの残高は{user_lune_balance}luneです',ephemeral=True)


@tree.command(name="mtri-transfer", description="mtriを送金します")
@app_commands.describe(to="送金先のユーザー名(@から始まる形にしてください)",amount="送金額")
async def agree_command(interaction: discord.Interaction,to:str,amount:int):
  transfer_result = bank.transfer(to,amount,interaction.user.id)
  await interaction.response.send_message(transfer_result,ephemeral=True)


@tree.command(name="lune-transfer", description="luneを送金します")
@app_commands.describe(to="送金先のユーザー名(@から始まる形にしてください)",amount="送金額")
async def agree_command(interaction: discord.Interaction,to:str,amount:int):
  transfer_result = lune.transfer(interaction.user.id,to,amount)
  await interaction.response.send_message(transfer_result,ephemeral=True)


@tree.command(name="promo-code", description="プロモーションコードを使用します")
@app_commands.describe(code="コード")
async def promo_command(interaction: discord.Interaction,code:str):
  auth_result = str(ex.promo(code,interaction.user.id))
  await interaction.response.send_message(auth_result,ephemeral=True)


@tree.command(name="lune-buy", description="買い注文を作成(luneを購入)")
@app_commands.describe(price="注文価格(lune)",amount="注文数量(mtri)")
async def order_buy_command(interaction: discord.Interaction,price:int,amount:int):
  reply_result = lune.buy(price,amount,interaction.user.id)
  await interaction.response.send_message(reply_result,ephemeral=True)


@tree.command(name="lune-sell", description="売り注文を作成(luneを売却・mtriを購入)")
@app_commands.describe(price="注文価格(lune)",amount="注文数量(mtri)")
async def order_sell_command(interaction: discord.Interaction,price:int,amount:int):
  reply_result = lune.sell(price,amount,interaction.user.id)
  await interaction.response.send_message(reply_result,ephemeral=True)


@tree.command(name="order-cancel", description="注文をキャンセル")
@app_commands.describe(order_id="注文ID",buy_or_sell="取り消したい注文の種類 購入の場合はbuy、売却の場合はsell")
async def order_cansel_command(interaction: discord.Interaction,order_id:str,buy_or_sell:str):
  reply_result = lune.cancel_order(interaction.user.id,buy_or_sell,order_id)
  await interaction.response.send_message(reply_result,ephemeral=True)


@tree.command(name="history-order", description="注文履歴を表示")
@app_commands.describe(number="表示させる件数(全て表示するには0を指定)")
async def order_sell_command(interaction: discord.Interaction,number: int):
  reply_result = lune.show_order(interaction.user.id,number)
  await interaction.response.send_message(reply_result,ephemeral=True)


@tree.command(name="lune-rate", description="luneの取引価格を表示")
async def exchange_rate_command(interaction: discord.Interaction):
  reply_result = lune.exchange_rate()
  await interaction.response.send_message(reply_result,ephemeral=True)


@tree.command(name="lune-list", description="取引板？みんなの注文一覧？なんかそんなやつ  マジで便利だから作った  褒めて")
async def order_list_command(interaction: discord.Interaction):
  reply_result = lune.order_list()
  await interaction.response.send_message(reply_result,ephemeral=True)


@tree.command(name="btc-buy", description="btcを購入(lune=>btc)")
@app_commands.describe(amount="数量")
async def btc_buy_command(interaction: discord.Interaction,amount: int):
  btc.sync_price()
  reply_result = btc.buy(interaction.user.id,amount)
  await interaction.response.send_message(reply_result,ephemeral=True)


@tree.command(name="btc-sell", description="btcを売却(btc=>lune)")
@app_commands.describe(amount="数量")
async def btc__command(interaction: discord.Interaction,amount: int):
  btc.sync_price()
  reply_result = btc.sell(interaction.user.id,amount)
  await interaction.response.send_message(reply_result,ephemeral=True)


@tree.command(name="btc-rate", description="btcの取引価格を表示")
async def btc__command(interaction: discord.Interaction):
  btc.sync_price()
  reply_result = btc.exchange_rate()
  await interaction.response.send_message(reply_result,ephemeral=True)


@tree.command(name="btc_balance", description="btcの残高を表示")
async def btc__command(interaction: discord.Interaction):
  btc.sync_price()
  balance = btc.balance(interaction.user.id)
  reply_result = (f'残高は{balance}btcです')
  await interaction.response.send_message(reply_result,ephemeral=True)


client.run(TOKEN)

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