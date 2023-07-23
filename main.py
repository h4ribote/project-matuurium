import discord
from discord import app_commands
import random
import ex as ex
import bank as bank
from config import bot_config

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

TOKEN = bot_config.TOKEN


@client.event
async def on_ready():
  print('成功しました')
  print(f'" {client.user} "としてログイン中')
  await client.change_presence(activity=discord.Game(name=str(ex.cl())))
  await tree.sync()


@client.event
async def on_message(message):
  # このボットからのメッセージを無効
  if message.author == client.user:
    return

  # メッセージが"なあ、"または"なぁ、"で始まっていたらメッセージを送信
  if message.content.startswith('なあ、') or message.content.startswith('なぁ、'):
    reply_massage = random.randint(0,9)
    emoji = "👍"
    if reply_massage <= 4:
      await message.add_reaction(emoji)
      await message.channel.send('もちろん！！')
    elif reply_massage >= 5 and reply_massage <= 8:
      await message.add_reaction(emoji)
      await message.channel.send('当たり前じゃないか！！')
    else:
      emoji ="❓"
      await message.add_reaction(emoji)
      await message.channel.send('いや別にそんなことはないと思いますけど')


@tree.command(name="yes", description="yes")
async def test_command(interaction: discord.Interaction):
  await interaction.response.send_message("yes")


@tree.command(name="agree", description="同意してあげます")
@app_commands.describe(con="同意してほしい内容(事実のみ使用可)",
                       sent="文章の種類(1~4)",
                       ene="訴えかけたい相手(sent=3の時のみ使用)")
async def agree_command(interaction: discord.Interaction,
                        con:str,
                        sent:int,
                        ene:str = "みんな"):
  if sent == 1:
    await interaction.response.send_message(f"はい！！私も{con}と思います！")
  elif sent == 2:
    await interaction.response.send_message(f"もちろん{con}よね")
  elif sent == 3:
    await interaction.response.send_message(f"まさか{ene}は{con}という事実を否定するのか？")
  else:
    await interaction.response.send_message(f"{con}！！")


@tree.command(name="regist", description="データベースに情報を登録します")
async def test_command(interaction: discord.Interaction):
  if ex.f_checker(interaction.user.id):
    await interaction.response.send_message("どうやら既に登録してるようです 忘れたのですか？",ephemeral=True)
  else:
    bank.register(interaction.user.id)
    await interaction.response.send_message('登録が完了しました',ephemeral=True)


@tree.command(name="balance", description="残高を確認します")
async def test_command(interaction: discord.Interaction):
  user_balance = bank.balance(interaction.user.id)
  await interaction.response.send_message(f'あなたの残高は{user_balance}です',ephemeral=True)
  

@tree.command(name="transfer", description="送金します")
@app_commands.describe(to="送金先(@から始まる(メンションする時みたいな)形にしてください)",
                       amount="送金額")
async def agree_command(interaction: discord.Interaction,
                        to:str,
                        amount:int):
  transfer_result = bank.transfer(to,amount,interaction.user.id)
  await interaction.response.send_message(transfer_result,ephemeral=True)



client.run(TOKEN)
