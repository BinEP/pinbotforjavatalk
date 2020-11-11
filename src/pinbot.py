import discord


class Pinbot(discord.Client):
	def __init__(self, pin_emoji_id, votes_to_pin):
		super().__init__()
		self.pin_emoji_id = pin_emoji_id
		self.votes_to_pin = votes_to_pin
	
	async def on_ready(self):
		print("Logged in as %s with id %s" % (self.user.name, self.user.id))
		print("------")
	
	async def on_raw_reaction_add(self, reaction):
		channel = await self.fetch_channel(reaction.channel_id)
		message = await channel.fetch_message(reaction.message_id)
		user = await self.fetch_user(reaction.user_id)
		
		for eachReaction in message.reactions:
			if str(eachReaction.emoji) == self.pin_emoji_id:
				print("Detected pin request for message %d from %s with count %d" % (reaction.message_id, user.name, eachReaction.count))
				if eachReaction.count >= self.votes_to_pin:
					print("Pin votes (%d of %d) reached for message %d" % (eachReaction.count, self.votes_to_pin, reaction.message_id))
					await message.pin()
	
	async def on_raw_reaction_remove(self, reaction):
		channel = await self.fetch_channel(reaction.channel_id)
		message = await channel.fetch_message(reaction.message_id)
		user = await self.fetch_user(reaction.user_id)
		
		if str(reaction.emoji) == self.pin_emoji_id:
			remaining_votes = sum(str(eachReaction.emoji) == self.pin_emoji_id for eachReaction in message.reactions)
			print("Detected remove pin request for message id %d from %s - %d remain" % (reaction.message_id, user.name, remaining_votes))
			if remaining_votes <= 0:
				print("No pin votes remain for message %d - unpinning" % reaction.message_id)
				await message.unpin()
