import os
import pkg_resources




# todo
if os.uname()[1] == "localhost":
	response = os.system("pip3 install -r requirements.txt --no-cache-dir")
	if response == 0:
		print("Successfully Installed all requirements")
	else:
		print("Failed to install requirements")




# if you deployed this userbot using localhost method, then replace all the necessary parts of the variables given below after '=' sign with the required values.
# for example edit like 'API_ID = 1234567' instead of 'API_ID = os.getenv("API_ID")'
# Warning: don't touch anything else given below except the values you wanna change otherwise you'll get errors.
#-------------------------------------------------------------------------------------------------------------
class Config(object):
	""" configuration class """
	# api id of your telegram account (required)
	API_ID =(os.getenv("18564918"))
	# api hash of your telegram account (required)
	API_HASH = os.getenv("fd99995bc013e54c3649fb563d1d18b9")
	# create a session using command [ python3 session.py ] or use repl.it (required)
	SESSION = os.getenv("v0Y5SnIZMEeBYNgpnPjWPMKaZFRfb1eA6SBYMN5O3rIJ6i8qHmrxri68-BOAYATwq15O9LSDfwKncNqeZsGrliGNkwtfnR2LiVagdFNPinmJ7KtxrLq-kVJUIwFtzFt3Hm")
# ------------------
	# temporary download location (required)
	TEMP_DICT = os.getenv("TEMP_DICT", os.path.abspath(".") + "/downloads/")
	# official repo for updates
	UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "https://github.com/TeamAsterix/AsterixUB.git")
# ------------------
	# heroku api key (required -> if hosted on heroku)
	HEROKU_API_KEY = os.getenv("HEROKU_API_KEY")
	# heroku app name (required -> if hosted on heroku)
	HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
	# database url (required)
	DB_URI = os.getenv("postgresql://postgres:wkpOtCKYjtQcQkPjukax@containers-us-west-38.railway.app:5984/railway")
# ------------------
	# these users can use your userbot
	SUDO_USERS = [int(x) for x in os.getenv("SUDO_USERS", "").split()] # splits on spaces
	# a group to store logs, etc (required)
	LOG_CHAT =(os.getenv("-1001496311246"))
	# command handler, if you give (exclamation symbol = !) then you can do like this command: !ping => result: pong !
	PREFIX = os.getenv("PREFIX", ".")
	# for more info visit docs.pyrogram.org, workers section
	WORKERS = int(os.getenv("WORKERS", 8))
	# exclude official plugins from installing, give a space between plugin names
	NO_LOAD = [int(x) for x in os.getenv("NO_LOAD", "").split()] # splits on spaces
	# default reason for afk plugin
	AFK_TEXT = os.getenv("AFK_TEXT", "I am busy Now !")
# ------------------
	# add True to enable (default: False)
	PMPERMIT = os.getenv("PMPERMIT", False)
	# pmpermit pic (optional)
	PMPERMIT_PIC = os.getenv("PMPERMIT_PIC")
	# custom  pmpermit security text (optional)
	PMPERMIT_TEXT = os.getenv("PMPERMIT_TEXT", "Hey ! This is [ Asterix Userbot](https://t.me/TeamAsterix) Security System.\n**You will be blocked if you spammed my owner's pm**\nCurrently My Owner is busy! So Wait Until He Arrives. 👍🏻\nAnd Better Not To Spam His here!")
	# pmpermit warn limit (optional)
	PM_LIMIT = int(os.getenv("PM_LIMIT", 4))
	# this is used to get your accurate time 
	TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Kolkata")
# -------------------
	# your custom name (default: telegram name)
	USER_NAME = os.getenv("USER_NAME")
	# your custom bio (default: telegram bio)
	USER_BIO = os.getenv("USER_BIO")
	# used for alive plugin (default: asterixuserbot logo image)
	USER_PIC = os.getenv("USER_PIC", "")
	# add your telegram id if bot fails to get your id 
	USER_ID = os.getenv("USER_ID")
	# add your username if bot fails to get your username
	USER_USERNAME = os.getenv("USER_USERNAME")
# --------------------
	# this bio will be shown in '/help' menu (default: official bio from bot) 
	BOT_BIO = os.getenv("BOT_BIO")
	# your assistants custom name (default: Kushina)
	BOT_NAME = os.getenv("BOT_NAME", "Kushina")
	# your assistants alive pic (optional)
	BOT_PIC = os.getenv("BOT_PIC", "https://telegra.ph/file/3930fb44de59f65849f5b.jpg")
	# provide this if bot fails to get username of bot (optional)
	BOT_USERNAME = os.getenv("BOT_USERNAME")
	# telegram id of bot if failed to get automatically (optional)
	BOT_ID = os.getenv("BOT_ID")
	# access token of your bot, without this the bot will not work (required)
	TOKEN = os.getenv("TOKEN")
# ---------------------
	# thumbnail used while uploading plugins, etc. (optional)
	THUMB_PIC = os.getenv("THUMB_PIC", "material/images/asterix.png")
# ---------------------
	# your telegraph account name (default: Asterixuserbot)
	TL_NAME = os.getenv("TL_NAME")
	# this will be shown before (as a prefix) the texts in the help dex (default: None)
	HELP_EMOJI = os.getenv("HELP_EMOJI")


