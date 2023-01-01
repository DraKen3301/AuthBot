import main, discord, deta, httpx, asyncio
from deta import Deta
from discord.ext import commands

class CommandsCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	async def refresh(self, ctx):
		conn = Deta(main.client_db)
		db = conn.Base("Auths")
		data = (db.fetch(limit=1000)).items
		for element in data:
			key, tk = element["key"], element["refresh_token"]
			refresh = main.refresh_token(key, tk)
			await ctx.reply(refresh, mention_author=False)
			await asyncio.sleep(3)
			
	@commands.command()
	async def count(self, ctx):
		conn = Deta(main.client_db)
		db = conn.Base("Auths")
		data = (db.fetch(limit=1000)).items
		await ctx.reply(len(data))
		
	@commands.command(aliases=["joinall"])
	async def pullall(self, ctx):
		conn = Deta(main.client_db)
		db = conn.Base("Auths")
		data = (db.fetch(limit=1000)).items
		joined = 0
		failed = 0
		for element in data:
			r = httpx.put(f"https://discord.com/api/v10/guilds/{ctx.guild.id}/members/{element['key']}",json={"access_token":element['access_token']},headers={"Authorization":"Bot " + main.client_token})
			await asyncio.sleep(2)
			print(r)
			if r.status_code == 201 or r.status_code == 204:
				joined += 1 
			else:
				failed += 1
		await ctx.reply(f"""[+] Joined: {joined}
[-] Failed: {failed} """)

	@commands.command(aliases=["join"])
	async def pull(self, ctx, id):
		try:
			conn = Deta(main.client_db)
			db = conn.Base("Auths")
			element = ((db.fetch(query={"key":str(id)})).items)[0]
			r = httpx.put(f"https://discord.com/api/v10/guilds/{ctx.guild.id}/members/{element['key']}",json={"access_token":element['access_token']},headers={"Authorization":"Bot " + main.client_token})
			await asyncio.sleep(2)
			print(r)
			if r.status_code == 201 or r.status_code == 204:
				await ctx.reply(f"""[+] Succesfully joined.""")
			else:
				await ctx.reply(f"""[-] Failed to join.""")
		except:
			await ctx.reply(f"""[-] Failed to join.""")
		

def setup(bot):
	bot.add_cog(CommandsCog(bot))