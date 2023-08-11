import os
from dotenv import load_dotenv
import discord
from discord import app_commands
import ex
import bank
import lune

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



@tree.command(name="ping", description='ping')
async def ping_command(interaction: discord.Interaction):
  await interaction.response.send_message("pong",ephemeral=True)


@tree.command(name="regist", description="データベースに情報を登録します")
async def regist_command(interaction: discord.Interaction):
  if ex.f_checker(interaction.user.id):
    await interaction.response.send_message("どうやら既に登録してるようです 忘れたのですか？",ephemeral=True)
  else:
    bank.register(interaction.user.id)
    await interaction.response.send_message('登録が完了しました',ephemeral=True)


@tree.command(name="balance", description="残高を確認します")
async def balance_command(interaction: discord.Interaction):
  user_balance = bank.balance(interaction.user.id)
  await interaction.response.send_message(f'あなたの残高は{user_balance}mtriです',ephemeral=True)


@tree.command(name="lune-balance", description="chihaluneの残高を確認します")
async def lune_balance_command(interaction: discord.Interaction):
  user_lune_balance = lune.balance(interaction.user.id)
  await interaction.response.send_message(f'あなたの残高は{user_lune_balance}luneです',ephemeral=True)


@tree.command(name="transfer", description="mtriを送金します")
@app_commands.describe(to="送金先のユーザー名(@から始まる形にしてください)",
                       amount="送金額")
async def agree_command(interaction: discord.Interaction,
                        to:str,
                        amount:int):
  transfer_result = bank.transfer(to,amount,interaction.user.id)
  await interaction.response.send_message(transfer_result,ephemeral=True)


@tree.command(name="promo-code", description="プロモーションコードを使用します")
@app_commands.describe(code="コード")
async def promo_command(interaction: discord.Interaction,code:str):
  auth_result = str(ex.promo(code,interaction.user.id))
  await interaction.response.send_message(auth_result,ephemeral=True)


@tree.command(name="order_buy", description="買い注文を作成(luneを購入)")
@app_commands.describe(price="注文価格(lune)",amount="注文数量(mtri)")
async def order_buy_command(interaction: discord.Interaction,price:int,amount:int):
  reply_result = lune.buy(price,amount,interaction.user.id)
  await interaction.response.send_message(reply_result,ephemeral=True)


@tree.command(name="order_sell", description="売り注文を作成(luneを売却・mtriを購入)")
@app_commands.describe(price="注文価格(lune)",amount="注文数量(mtri)")
async def order_sell_command(interaction: discord.Interaction,price:int,amount:int):
  reply_result = lune.sell(price,amount,interaction.user.id)
  await interaction.response.send_message(reply_result,ephemeral=True)


@tree.command(name="order_cancel", description="注文をキャンセル")
@app_commands.describe(order_id="注文ID",buy_or_sell="取り消したい注文の種類 購入の場合はbuy、売却の場合はsell")
async def order_cansel_command(interaction: discord.Interaction,order_id:str,buy_or_sell:str):
  reply_result = lune.cancel_order(interaction.user.id,buy_or_sell,order_id)
  await interaction.response.send_message(reply_result,ephemeral=True)


@tree.command(name="history_order", description="注文履歴を表示")
@app_commands.describe(number="表示させる件数(全て表示するには0を指定)")
async def order_sell_command(interaction: discord.Interaction,number: int):
  reply_result = lune.show_order(interaction.user.id,number)
  await interaction.response.send_message(reply_result,ephemeral=True)


@tree.command(name="price_list", description="取引価格を表示")
async def price_list_command(interaction: discord.Interaction):
  reply_result = lune.price_list()
  reply_result = "準備中"
  await interaction.response.send_message(reply_result,ephemeral=True)


client.run(TOKEN)