import discord
from datetime import datetime
import pytz


class Pinbot(discord.Client):
	def __init__(self, pin_emoji_id, votes_to_pin):
		super().__init__()
		self.pin_emoji_id = pin_emoji_id
		self.votes_to_pin = votes_to_pin
	
	async def on_ready(self):
		print("Logged in as %s with id %s" % (self.user.name, self.user.id))
		print("------")
		current_time = datetime.today().astimezone(pytz.timezone("US/Central")).strftime("%b %d %H:%M")
		await self.change_presence(activity=discord.Game(name="life since %s" % current_time))
	
	async def close(self):
		print("Disconnecting from discord...")
		await self.change_presence(activity=None, status=discord.Status.offline)
		return await super().close()
	
	async def on_raw_reaction_add(self, reaction):
		channel = await self.fetch_channel(reaction.channel_id)
		message = await channel.fetch_message(reaction.message_id)
		user = await self.fetch_user(reaction.user_id)

		if str(reaction.emoji) == self.pin_emoji_id:
			message_reaction = next((reaction for reaction in message.reactions if str(reaction.emoji) == self.pin_emoji_id), None)
			if message_reaction is not None:
				print("Detected pin request for message %d from %s with count %d" % (reaction.message_id, user.name, message_reaction.count))
				if message_reaction.count >= self.votes_to_pin:
					print("Pin votes (%d of %d) reached for message %d" % (message_reaction.count, self.votes_to_pin, reaction.message_id))
					await message.pin()
	
	async def on_raw_reaction_remove(self, reaction):
		channel = await self.fetch_channel(reaction.channel_id)
		message = await channel.fetch_message(reaction.message_id)
		user = await self.fetch_user(reaction.user_id)
		
		if str(reaction.emoji) == self.pin_emoji_id:
			message_reaction = next((reaction for reaction in message.reactions if str(reaction.emoji) == self.pin_emoji_id), None)
			remaining_votes = 0 if message_reaction is None else message_reaction.count
			print("Detected remove pin request for message id %d from %s - %d remain" % (reaction.message_id, user.name, remaining_votes))
			if remaining_votes <= 0:
				print("No pin votes remain for message %d - unpinning" % reaction.message_id)
				await message.unpin()
