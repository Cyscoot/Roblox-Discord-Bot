from secrets import choice
import discord
from discord.ext import commands
import json
import requests

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = ">", intents = intents)
token = ""

random_bio = None
#BASICS 

@client.event
async def on_ready():
  print("The Bot is ready")

async def b_show(channel, tit, desc, img):
  if img != None:
    embed_img = discord.Embed(
      title = tit,
      description = desc,
      color = 0x18CBE8
    )
    embed_img.set_image(url=img)
    sender = await channel.send(embed=embed_img)
  else:
    embed = discord.Embed(
        title = tit,
        description = desc,
        color = 0x18CBE8
    )
    sender_ni = await channel.send(embed=embed)

#INFORMATIONS

@client.command()
async def devex(ctx, *, value=None):
  if value != None:
    await b_show(ctx, "Devex", f"{value} R$ converts to {int(int(value) / 10000 * 35)} USD", None)
  else:
    await b_show(ctx, "Devex", "100,000 R$ converts to 350 USD", None)


@client.event
async def on_member_join(member):
  await b_show(member, "Welcome !", "Welcome to our server, to verify yourself you need to verify your roblox account, to this type >verify.", None)
    
@client.command()
async def verify(ctx):
  jsonbase = open("database/accounts.json")
  jsoncheck = json.load(jsonbase)

  l_counter = 0

  for i in jsoncheck:
    l_counter += 1
    if int(jsoncheck[l_counter-1]["discord"]) == ctx.message.author.id:
      await b_show(ctx, "Error", "You are already signed up.", None)
      jsonbase.close()
      return

  jsonbase.close()

  table_word = ["like", "cheese", "pro", "guy", "red", "nice", "great", "yellow", "blue"]
  global random_bio
  random_bio = f"{choice(table_word)}, {choice(table_word)}, {choice(table_word)}"
  await b_show(ctx, "Verify", f"To verify your roblox account you need to change your bio to this this : {random_bio} \n Once done, type >checkbio [your roblox id] ", None)


@client.command()
async def checkbio(ctx, msg):
  page = requests.get(f"https://users.roblox.com/v1/users/{msg}").json()
  if page["description"] == random_bio:
    file_name = "database/accounts.json"
    with open(file_name) as fp:
      listObj = json.load(fp)
      fp.close()
  else:
    await b_show(ctx, "Error", "An error happends, make sure to change your bio. To try again do >verify.", None)
    return

  print(listObj)

  listObj.append({
    "discord" : f"{ctx.message.author.id}",
    "roblox" : f"{msg}"
  })

  with open(file_name, 'w') as json_file:
    json.dump(listObj, json_file, 
                        indent=4,  
                        separators=(',',': '))
 

  await b_show(ctx, "Thanks!", f"You now have access to our server. You can change your bio again.", None)


@client.command()
async def userinfos(ctx, member : discord.Member):
  jsonbase = open("database/accounts.json")
  jsoncheck = json.load(jsonbase)
  char_to_replace = {"<", ">", "@"}
  user_l_id = member.mention

  for i in char_to_replace:
    user_l_id = user_l_id.replace(i, "")

  l_counter = 0

  for i in jsoncheck:
    l_counter += 1
    if jsoncheck[l_counter-1]["discord"] == user_l_id:
      roblox_id = jsoncheck[l_counter-1]["roblox"]
      creation_date = requests.get(f"https://users.roblox.com/v1/users/{roblox_id}").json()["created"]
      mod_date = ""
      n = 13
      for i in range(len(creation_date) - n):
        mod_date = mod_date + creation_date[i]

      await b_show(ctx, "User Infos : ", f"**Roblox Account :** \n https://www.roblox.com/users/{roblox_id}/profile was create the {mod_date} \n **Discord Account :** \n ID : {user_l_id}", member.avatar_url)
      jsonbase.close()
      break

  jsonbase.close()

client.run(token)
