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
async def on_raw_reaction_add(reaction):

	channel = await client.fetch_channel(reaction.channel_id)
	message = await channel.fetch_message(reaction.message_id)
	user = await client.fetch_user(reaction.user_id)

	for eachReaction in message.reactions :
		if str(eachReaction.emoji) == pinEmojiId:
			print("Detected pin request for message id %d from %s with count %d" % (reaction.message_id, user.name, eachReaction.count))
			if eachReaction.count >= votesToPin:
				await message.pin()


@client.event
async def on_raw_reaction_remove(reaction):

	channel = await client.fetch_channel(reaction.channel_id)
	message = await channel.fetch_message(reaction.message_id)
	user = await client.fetch_user(reaction.user_id)

	if not any(eachReaction.emoji == pinEmojiId for eachReaction in message.reactions) :
		print("Detected remove pin request for message id %d from %s" % (reaction.message_id, user.name))
		await message.unpin()


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

