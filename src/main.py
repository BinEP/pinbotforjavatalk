from pinbot import Pinbot
import os
import signal


def build_signal_handler(bot: Pinbot):
	def signal_handler(sig, frame):
		bot.close()
	return signal_handler


if __name__ == '__main__':
	print("Starting discord bot...")
	token = ""
	pin_emoji_id = ""
	votes_to_pin = 0
	
	try:
		token = os.environ['DISCORD_TOKEN']
	except KeyError:
		print("No discord bot token defined for 'DISCORD_TOKEN'")
		exit(-1)
	
	try:
		pin_emoji_id = os.environ['PIN_EMOJI']
	except KeyError:
		print("No emoji has been defined for 'PIN_EMOJI'")
		exit(-1)
	
	try:
		votes_to_pin_str = os.environ['VOTES_TO_PIN']
		try:
			votes_to_pin = int(votes_to_pin_str)
		except ValueError:
			print('Please enter an integer for env var VOTES_TO_PIN')
			exit(-1)
	except KeyError:
		print("No threshhold for pinning has been defined for 'VOTES_TO_PIN'")
		exit(-1)
	
	pinbot = Pinbot(pin_emoji_id=pin_emoji_id, votes_to_pin=votes_to_pin)
	
	print("Setting up signal handler...")
	signal.signal(signal.SIGINT, build_signal_handler(pinbot))
	signal.signal(signal.SIGTERM, build_signal_handler(pinbot))
	
	print("Connecting to discord...")
	pinbot.run(token)
