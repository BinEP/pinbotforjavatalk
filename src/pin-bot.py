import discord
import os


TOKEN = None
pinEmojiId = None
votesToPinStr = None
votesToPin = None

client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_server_join(server):
	string = """ Just add reaction of :specialpin:, and the message pinned! Requires """
	string += str(votesToPin)
	string += " votes to Pin"
	return await client.send_message(
		server.default_channel,
		""" Just add reaction of :specialpin:, and the message pinned! Requires """
		)

@client.event
async def on_reaction_add(reaction, user):
	if str(reaction.emoji) == pinEmojiId:
		print("Detected add pin request for message id %d from %s with count %d" % (reaction.message.id, user.name, reaction.count))
		if reaction.count >= votesToPin:
			await reaction.message.pin()


@client.event
async def on_reaction_remove(reaction, user):
	if str(reaction.emoji) == pinEmojiId:
		print("Detected remove pin request for message id %d from %s with count %d" % (reaction.message.id, user.name, reaction.count))
		if reaction.count == 0:
			await reaction.message.unpin()


if __name__ == '__main__':
	print("Starting discord bot...")
	try:
		TOKEN = os.environ['DISCORD_TOKEN']
	except KeyError:
		print("No discord bot token defined for 'DISCORD_TOKEN'")

	try:
		pinEmojiId = os.environ['PIN_EMOJI']
	except KeyError:
		print("No emoji has been defined for 'PIN_EMOJI'")


	try:
		votesToPinStr = os.environ['VOTES_TO_PIN']
	except KeyError:
		print("No threshhold for pinning has been defined for 'VOTES_TO_PIN'")

	try:
		votesToPin = int(votesToPinStr)
	except ValueError:
		print('Please enter an integer for env var VOTES_TO_PIN')


	if TOKEN == None or pinEmojiId == None or votesToPin == None or votesToPinStr == None :
		print("Terminating discord bot due to invalid environment variables")
		exit(-1)
	
	print("Connecting to discord...")
	client.run(TOKEN)

