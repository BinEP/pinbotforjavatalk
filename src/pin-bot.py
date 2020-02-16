import discord
client = discord.Client()


votesToPin = 1
pinEmojiId = "<:test:677641023597576223>"

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

	print(str(reaction.emoji))
	if (str(reaction.emoji) == pinEmojiId) :
		print("detected pin request")
		if (reaction.count >= votesToPin) :
			print("Count > 0")
			await reaction.message.pin()


@client.event
async def on_reaction_remove(reaction, user):

	if (str(reaction.emoji) == pinEmojiId) :
		print("detected pin request")
		if (reaction.count == 0) :
			print("Count == 0")
			await reaction.message.unpin()


TOKEN = 'Njc3NjM3Njc0OTY5OTg5MTUz.XkXJyw.DcbyBD_55w1AfQonULAOLZJw6QU'


if __name__ == '__main__':
	client.run(TOKEN)