import os
import sys
import math
import requests
import heroku3

from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid

from asterix import app, gen




app.CMD_HELP.update(
	{"heroku" : (
		"heroku",
		{
		"shutdown" : "Turn off your userbot by turning off the dynos.",
		"restart" : "Restart your userbot.",
		"usage" : "Check your heroku dyno usage.",
		"vars" : "Get a list of enabled vars in your heroku account.",
		"setvar [key] [value]" : "Set config vars of heroku through a command.",
		"getvar [key]" : "Get a existing var value from heroku config.",
		"delvar" : "Delete a existing heroku var from heroku config.",
		"logs" : "Get heroku logs as a file (Extension: .txt).",
		"textlogs" : "Get logs pasted in nekobin, not as a file."
		}
		)
	}
)




heroku_api = "https://api.heroku.com"

useragent = (
	"Mozilla/5.0 (Linux; Android 9; SM-G975F) "
	"AppleWebKit/537.36 (KHTML, like Gecko) "
	"Chrome/80.0.3987.149 Mobile Safari/537.36"
)



if (app.HEROKU_API_KEY and app.HEROKU_APP_NAME):
	heroku_app = heroku3.from_key(app.HEROKU_API_KEY).apps()[app.HEROKU_APP_NAME]
else:
	heroku_app = None



# shut-down dyno 
@app.on_message(gen("shutdown"))
async def shutdown_handler(_, m: Message):
	if await not_heroku(m):
		return 

	try:
		await app.send_message(
			app.LOG_CHAT, 
			"#shutdown \n" 
			"Bot is now turned off !!\nTurn it on manually on heroku.com"
		)
	except PeerIdInvalid:
		pass
	try:
		await app.send_edit(
			m, 
			"Dynos are truned off, if you want turn them on manually from heroku.com",
			text_type=["mono"]
		)
		heroku_app.process_formation()["worker"].scale(0)
	except Exception as e:
		await app.error(m, e)




# restart your bot 
@app.on_message(gen("restart"))
async def restart_handler(_, m: Message):
	if await not_heroku(m):
		return

	try:
		m = await app.send_edit(m, "Restarting . . .", text_type=["mono"])
		restart = heroku_app.restart()
		if restart:
			await app.send_edit(
				m, 
				"Restarted . . .!\nPlease wait for 3 min or more to restart userbot . . .", 
				text_type=["mono"]
			)
		else:
			await app.send_edit(
				m, 
				"Failed to restart userbot, try again later . . .",
				text_type=["mono"]
			)
	except Exception as e:
		await app.error(m, e)




# get usage of your dyno hours from heroku
@app.on_message(gen("usage", allow = ["sudo"]))
async def dynostats_handler(_, m: Message):
	if await not_heroku(m):
		return

	Heroku = heroku3.from_key(app.HEROKU_API_KEY)
	m = await app.send_edit(m, "Checking usage . . .", text_type=["mono"])
	u_id = Heroku.account().id
	try:
		if u_id:
			headers = {
				"User-Agent": useragent,
				"Authorization": f"Bearer {app.HEROKU_API_KEY}",
				"Accept": "application/vnd.heroku+json; version=3.account-quotas",
			}
			path = "/accounts/" + u_id + "/actions/get-quota"
			r = requests.get(heroku_api + path, headers=headers)
			if r.status_code != 200:
				return await app.send_edit(
					m, 
					"Error: something bad happened`\n\n" f"> {r.reason}\n",
					text_type=["mono"]
				)
			result = r.json()
			quota = result["account_quota"]
			quota_used = result["quota_used"]
			# used hours
			remaining_quota = quota - quota_used
			percentage = math.floor(remaining_quota / quota * 100)
			minutes_remaining = remaining_quota / 60
			hours = math.floor(minutes_remaining / 60)
			minutes = math.floor(minutes_remaining % 60)
			# remaining
			App = result["apps"]
			try:
				App[0]["quota_used"]
			except IndexError:
				AppQuotaUsed = 0
				AppPercentage = 0
			else:
				AppQuotaUsed = App[0]["quota_used"] / 60
				AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
			AppHours = math.floor(AppQuotaUsed / 60)
			AppMinutes = math.floor(AppQuotaUsed % 60)

			await app.send_edit(
				m, 
				"**Dyno Usage**:\n\n"
				f"**Total Dyno Hours:** `550 Hours`\n\n"
				f"**⧓ Dyno usage for App:** __`{app.HEROKU_APP_NAME}`__\n"
				f"\r• `{AppHours}h {AppMinutes}m`"
				f"**|**  [ `{AppPercentage}`**%** ]\n\n"
				f"**⧓ Quota remaining this month:**\n"
				f"\r• `{hours} Hours & {minutes} Mins`"
				f" |  [ `{percentage}%` ]"
			)
	except Exception as e:
		await app.error(m, e)




# get list of vars from heroku 
@app.on_message(gen("vars", allow = ["sudo"]))
async def herokuvars_handler(_, m: Message):
	if await not_heroku(m):
		return

	try:
		m = await app.send_edit(
			m, 
			"Fetching all vars from Heroku . . .", 
			text_type=["mono"]
			)
		heroku_vars = heroku_app.config()
		vars_dict = heroku_vars.to_dict()
		vars_keys = list(vars_dict.keys())
		msg = "**All Heroku Vars:**\n\n"
		num = 0
		for i in vars_keys:
			num += 1
			msg += f"**{num}**: `{i}`\n"

		msg += f"\n**Total `{num}` vars found.**"
		await app.send_edit(m, msg)
	except Exception as e:
		await app.error(m, e)




# set vars in heroku 
@app.on_message(gen("setvar"))
async def setvar_handler(_, m: Message):
	if await not_heroku(m):
		return

	if app.long(m) < 3:
		await app.send_edit(
			m, 
			f"`{app.PREFIX}setvar [key] [value]`"
		)
	elif app.long(m) >= 3:
		key = m.command[1]
		value = m.command[2]
		heroku_vars = heroku_app.config()
		try:
			if key and value in heroku_vars:
				await app.send_edit(
					m, 
					f"{key} is already in vars with value {value}"
				)
			elif not key in heroku_vars:
				await app.send_edit(
					m, 
					f"Added var •> `{key}` = `{value}`", 
					disable_web_page_preview=True
				)
				heroku_vars[key] = value
			else:
				await app.send_edit(
					m,
					"Something went wrong, try again later !",
					text_type=["mono"]
				)
		except Exception as e:
			await app.error(m, e)




# get vars from heroku vars
@app.on_message(gen("getvar"))
async def getvar_handler(_, m: Message):
	if await not_heroku(m):
		return

	if app.long(m) == 1:
		return await app.send_edit(
			m, 
			f"`{app.PREFIX}getvar [key name]`"
		)
	elif app.long(m) >= 2:
		key = m.command[1]
		heroku_vars = heroku_app.config()
		try:
			if heroku_vars:
				await app.send_edit(
					m, 
					f"**Key exists:**\n\n`{key}` = `{heroku_vars[key]}`"
				)
			else:
				await app.send_edit(
					m, 
					"Failed to get heroku key . . .",
					text_type=["mono"]
				)
		except Exception as e:
			await app.error(m, e)




# delete vars in heroku 
@app.on_message(gen("delvar"))
async def delvar_handler(_, m: Message):
	if await not_heroku(m):
		return

	if app.long(m) == 1:
		return await app.send_edit(
			m, 
			f"{app.PREFIX}delvar [key name]", 
			text_type=["mono"]
		)
	elif app.long(m) >= 2:
		m = await app.send_edit(
			m, 
			"Verifying var in heroku config vars . . .", 
			delme=3, 
			text_type=["mono"]
		)

		key = m.command[1]
		heroku_vars = heroku_app.config()

		if key not in heroku_vars:
			return await app.send_edit(
				m, 
				f"**`{key}`** does not exist in heroku vars . . .", 
				delme=3
			)

		try:
			del heroku_vars[key]
		except Exception as e:
			return await app.error(m, e)
		await app.send_edit(
			m, 
			f"Successfully deleted var = [ {key} ] from heroku vars !", 
			delme=4
		)
	else:
		await app.send_edit(
			m, 
			f"Usage: `{app.PREFIX}delvar [key name]` use this format.",
			delme=4
		)




# get logs from heroku in file format (.txt)
@app.on_message(gen("logs", allow = ["sudo"]))
async def logs_handler(_, m: Message):
	if await not_heroku(m):
		return

	m = await app.send_edit(m, "⏳ • hold on . . .", text_type=["mono"])
	logsdata = heroku_app.get_log()
	if logsdata:
		try:
			filename = f"./downloads/{app.username}_logs.txt"
			file = open(filename, "w+")
			file.write(logsdata)
			file.close()
			await app.send_document(
				m.chat.id,
				filename,
				caption=f"Uploaded By: {app.UserMention()}")
			if os.path.exists(filename):
				os.remove(filename)
			await m.delete()
		except Exception as e:
			await app.error(m, e)
	else:
		await app.send_edit(m, "Failed to get logs . . .", delme=3)




# get logs from heroku in nekobin link, not as a file 
@app.on_message(gen(["textlogs", "tlogs"], allow = ["sudo"]))
async def textlogs_handler(_, m: Message):
	if await not_heroku(m):
		return

	m = await app.send_edit(m, "⏳ • hold on . . . ", text_type=["mono"])
	logsdata = heroku_app.get_log()
	if logsdata:
		try:
			url = await app.HasteBinPaste(logsdata)
			text = f"Heroku Logs: [press here]({url})"
			await app.send_edit(m, text, disable_web_page_preview=True)
		except Exception as e:
			await app.error(m, e)
	else:
		await app.send_edit(m, f"Failed to get the heroku text logs, try `{app.PREFIX.split()[0]}logs` command.", delme=4)




async def not_heroku(m: Message):
	if not (
		app.HEROKU_APP_NAME
		and app.HEROKU_API_KEY
		):
		return await app.send_edit(
			m, 
			"Please fill heroku credentials for this command to work [`HEROKU_APP_NAME`, `HEROKU_API_KEY`"
		)
		return True
	return False
