import time
import asyncio
import html

from pyrogram.types import Message, ChatPermissions, User

from pyrogram.errors import UserAdminInvalid, PeerIdInvalid, UsernameNotOccupied

from asterix import app

from asterix.helpers import (
	gen,
)




app.CMD_HELP.update(
	{"utils" : (
		"utils",
		{
		"settitle [ @username ] [ title ]" : "Set title of an admin.",
		"invite [ @username ]" : "Invite a user / bot in your chat.",
		"admins" : "Get list of admins.",
		"report [ reply to user ]" : "Report a spammer or idiot.",
		"all" : "Tag recent 100 members, use carefully.",
		"bots" : "Get list of bots in a chat.",
		"kickme" : "Leave a chat, use it carefully.",
		"members [ @username ]" : "Get number of members in  a chat.",
		"join [@username]" : "Join a chat with just a command.",
		"slowmo [seconds | off]" : "Set slow mode in a chat, use only [ 10, 30, 60, 300, 900, 3600, off ] . . .",
		}
		)
	}
)




@app.on_message(gen("settitle", allow = ["sudo", "channel"]))
async def admintitle_handler(_, m: Message):
	if await app.check_private(m):
		return

	reply = m.reply_to_message
	if await app.IsAdmin(m) is True:
		if app.long(m) == 3:
			try:
				user_data = m.command[1]
				title = m.command[2]
				try:
					user = await app.get_users(user_data)
				except (UserAdminInvalid, PeerIdInvalid, UsernameNotOccupied):
					return await app.send_edit(m, "The username | id seems to be invalid  . . .", text_type=["mono"], delme=4)
				await app.send_edit(m, f"Setting `{user_data}`s title as `{title}` . . .")
				admin = user.id
				user_name = user.first_name
				user_chat_info = await app.get_chat_member(m.chat.id, admin)
				is_admin = user_chat_info.status
				if is_admin == "member":
					await app.send_edit(m, f"{user_name} is not an admin in this chat, use {app.PREFIX}promote command to promote them.", delme=3, text_type=["mono"])
				else:
					await app.set_administrator_title(m.chat.id, admin, title)
					await app.send_edit(m, f"**{user_name}'s** title is successfully changed to **{title}**")
			except Exception as e:
				await app.error(m, e)

		elif app.long(m) == 2 and reply:
			try:
				title = m.command[1]
				user = reply
				admin = user.from_user.id
				user_name = user.from_user.first_name
				user_chat_info = await app.get_chat_member(m.chat.id, admin)
				is_admin = user_chat_info.status
				if is_admin == "member":
					await app.send_edit(m, f"{user_name} is not an admin in this chat . . .", delme=3, text_type=["mono"])
				else:
					await app.set_administrator_title(m.chat.id, admin, title)
					await app.send_edit(m, f"{user_name}'s title is successfully changed to `{title}`", delme=5, text_type=["mono"])
			except Exception as e:
				await app.error(m, e)
		elif app.long(m) == 1 and not reply:
			await app.send_edit(m, "Reply or give me username | id after command . . .", text_type=["mono"], delme=3)
		else:
			await app.send_edit(m, "Something went wrong, Try again later.", text_type=["mono"], delme=3)
	else:
		await app.send_edit(m, "Sorry you are not an admin here . . .", delme=3, text_type=["mono"])




@app.on_message(gen("invite", allow = ["sudo", "channel"]))
async def invite_handler(_, m):
	if await app.check_private(m):
		return

	await app.send_edit(m, "⏳ • Hold on . . .", text_type=["mono"])
		
	reply = m.reply_to_message
	if reply:
		user = reply.from_user.id
	elif not reply and app.long(m) > 1:
		user = m.command[1]
	else:
		return await app.send_edit(m, "I can't invite ghost, can I ?", text_type=["mono"])

	try:
		get_user = await app.get_users(user)
	except (UserAdminInvalid, PeerIdInvalid, UsernameNotOccupied):
		return await app.send_edit(m, "The username | id seems to be invalid  . . .", text_type=["mono"], delme=4)

	await app.add_users(get_user.id, m.chat.id)
	await app.send_edit(m, f"Added {get_user.first_name} to the chat!")



@app.on_message(gen(["admins", "adminlist"], allow = ["sudo", "channel"]))
async def adminlist_handler(_, m):
	if await app.check_private(m):
		return

	await app.send_edit(m, "⏳ • Hold on. . .", text_type=["mono"])

	if app.long(m) >= 2:
		try:
			chat = m.command[1]
			group = await app.get_chat(chat)
		except UserAdminInvalid or PeerIdInvalid or UsernameNotOccupied:
			return await app.send_edit(m, "The username | id seems to be invalid  . . .", text_type=["mono"], delme=4)
	else:
		chat = m.chat.id
		group = await app.get_chat(chat)

	creator = []
	admin = []
	bot_admin = []

	creator.clear()
	admin.clear()
	bot_admin.clear()

	async for x in app.iter_chat_members(m.chat.id, filter="administrators"):
		if x.status == "creator":
			creator.append("{}".format(app.MentionMarkdown(x.user.id, x.user.first_name)))
		if x.status == "administrator":
			if x.user.is_bot:
				bot_admin.append("{}".format(app.MentionMarkdown(x.user.id, x.user.first_name)))
			else:
				admin.append("{}".format(app.MentionMarkdown(x.user.id, x.user.first_name)))

	total = len(creator) + len(admin) + len(bot_admin)
	teks = "Admins in {}\n\n".format(group.title)
	teks += "Creator:\n\n{}".format("".join(creator))
	teks += "\n\nUser:\n\n{}".format("\n".join(admin))
	teks += "\n\nBot:\n\n{}".format("\n".join(bot_admin))
	teks += "\n\nTotal {} admins".format(total)

	if teks:
		await app.send_edit(m, teks)
	else:
		await app.send_edit(m, "Something went wrong, Please try again later.", delme=3, text_type=["mono"])




@app.on_message(gen("report", allow = ["sudo", "channel"]))
async def reportadmin_handler(_, m: Message):
	if await app.check_private(m):
		return

	reply = m.reply_to_message
	if app.long(m) >= 2:
		text = m.text.split(None, 1)[1]
	else:
		text = False
	group = await app.get_chat(m.chat.id)

	admin = []
	async for x in app.iter_chat_members(m.chat.id, filter="administrators"):
		if x.status == "administrator" or x.status == "creator":
			if x.user.is_bot is False:
				admin.append(app.MentionHtml(x.user.id, "\u200b"))
	await app.send_edit(m, "Reporting . . .", text_type=["mono"])
	if reply:
		if text:
			teks = "{} is reported to admins.\n**Reason:** {}".format(app.MentionMarkdown(reply.from_user.id, reply.from_user.first_name), text)
		else:
			teks = "{} is reported to admins.".format(app.MentionMarkdown(reply.from_user.id, reply.from_user.first_name))
	else:
		return await app.send_edit(m, "Reply to someone to report him to admins . . .", delme =4, text_type=["mono"])
	teks += " ".join(admin)
	await app.send_edit(m, teks)




@app.on_message(gen("all", allow = ["sudo"]))
async def tagall_handler(app, m: Message):
	if await app.check_private(m):
		return

	reply = m.reply_to_message
	if app.long(m) >= 2:
		text = m.text.split(None, 1)[1]
	else:
		text = "Hello Everyone "
	await app.send_edit(m, "Wait . . .")

	async for x in app.iter_chat_members(m.chat.id):
		if x.user.is_bot is False:
			text += app.MentionHtml(x.user.id, "\u200b")
	if reply:
		await app.send_message(m.chat.id, text, reply_to_message_id=reply.message_id, parse_mode="html")
	else:
		await app.send_edit(m, text, parse_mode="html")




@app.on_message(gen(["bots"], allow = ["sudo"]))
async def botlist_handler(_, m: Message):
	if await app.check_private(m):
		return

	reply = m.reply_to_message
	replyid = None
	if app.long(m) >= 2:
		chat = m.text.split(None, 1)[1]
		grp = await app.get_chat(chat)
	else:
		chat = m.chat.id
		grp = await app.get_chat(chat)
	if reply:
		replyid = reply.message_id
	await m.edit("⏳ • Hold on. . .")

	bots = []
	bots.clear()
	async for x in app.iter_chat_members(chat):
		try:
			bot_info = x.user.first_name + " " + x.user.last_name
		except:
			bot_info = x.user.first_name
		if bot_info is None:
			bot_info = "💀 Deleted account"
		if x.user.is_bot is True:
			bots.append(app.MentionMarkdown(x.user.id, bot_info))
	teks = "**Bots in `{}`**\n\n".format(grp.title)
	for x in bots:
		teks += " • {}\n".format(x)
	teks += "\nTotal {} Bots".format(len(bots))
	if replyid:
		await app.send_m(
			m.chat.id, 
			teks, 
			reply_to_message_id=replyid
			)
	else:
		await app.send_edit(m, teks)




@app.on_message(gen("kickme", allow = ["sudo", "channel"]))
async def leavechat_handler(_, m):
	if await app.check_private(m):
		return

	try:
		await app.send_edit(m, f"{app.UserMention()} left the chat . . .")
		await asyncio.sleep(1)
		await app.leave_chat(m.chat.id)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("members", allow = ["sudo", "channel"]))
async def membercount_handler(_, m):
	if await app.check_private(m):
		return

	if app.long(m) == 1:
		try:
			num = await app.get_chat_members_count(m.chat.id)
			await app.send_edit(m, f"`{num}` members {m.chat.title}")
		except UsernameNotOccupied or PeerIdInvalid:
			await app.send_edit(m, "The username | id does not exist . . .", text_type=["mono"])
	elif len(m.command) >= 2:
		try:
			mid = m.command[1]
			num = await app.get_chat_members_count(mid)
			await app.send_edit(m, f"`{num}` members in {mid}")
		except UsernameNotOccupied:
			await app.send_edit(m, "The username does not exist . . .", text_type=["mono"])
	else:
		await app.send_edit(m, f"Usage: `{app.PREFIX}members` or `{app.PREFIX}members [chat username | id]` ", delme=5)




@app.on_message(gen("join", allow = ["sudo", "channel"]))
async def joinchat_handler(_, m: Message):
	if app.long(m) == 1:
		await app.send_edit(m, "Give me some chat id | username after command . . .", text_type=["mono"], delme=5)
	elif app.long(m) > 1:
		chat = m.command[1]
		try:
			data = await app.get_chat(chat)
			done = await app.join_chat(chat)
			if data and done:
				await app.send_edit(m, f"Successfully joined `{data.title}`")
			else:
				await app.send_edit(m, "Couldn't join chat !")
		except Exception as e:
			await app.error(m, e)
	elif app.long(m) > 4096:
		await app.send_edit(m, "Maximum 4096 characters allowed . . .", text_type=["mono"], delme=5)




@app.on_message(gen("slowmo", allow = ["sudo"]))
async def slowmode_handler(_, m: Message):
	if app.check_private(m):
		return

	if await app.IsAdmin(m) is True:
		if app.long(m) == 1:
			sec = 10
		elif app.long(m) > 1:
			sec = m.command[1]
			if sec == "off":
				await app.set_slow_mode(m.chat.id, None)
				await app.send_edit(m, "Slow mode is now turned off.", delme=3, text_type=["mono"])
			elif int(sec) not in [10, 30, 60, 300, 900, 3600]:
				return await app.send_edit(m, "Please choose seconds from here: [`10`, `30`, `60`, `300`, `900`, `3600`]")
		elif app.long(m) > 4096:
			return await app.send_edit(m, "Only 4096 characters are allowed . . .", text_type=["mono"], delme=3)

		try:
			sec = int(sec)
			await app.set_slow_mode(m.chat.id, sec)
			await app.send_edit(m, f"Updated slow mode to `{sec}` seconds.", delme=4)
		except Exception as e:
			await app.error(m, e)
	else:
		await app.send_edit(m, "Sorry, you are not an admin here . . .", delme=4, text_type=["mono"])
