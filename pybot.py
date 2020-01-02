import discord
import io
import aiohttp
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('READY')

# end - on_ready

@client.event
async def on_message(message:discord.Message):
    server_id = 661689102340456509
    text_id = 661689102340456515
    image_id = 661693924376838164
    link_id = 661694005863514125
    image_extensions = ['.png', '.jpg', '.jpeg']
    data = 0
    linked_image = False
    image = False
    link = False
    # ensuring the bot does not react to its own messages, as its sent messages are sent through this event
    if message.author != client.user:
        # determining if the message is a Discord-recognized link with a rich preview
        if message.content.startswith('http'):
            link = True
        # determining whether or not any images are attached to the message, this accounts for uploaded images and images from the clipboard
        for extension in image_extensions:
            try: 
                if message.attachments[0].filename.endswith(extension): 
                    image = True
                    # HTTP request to upload an image via a link, rather than a local upload
                    async with aiohttp.ClientSession() as session:
                        async with session.get(message.attachments[0].url) as resp:
                            if resp.status != 200:
                                return
                            data = io.BytesIO(await resp.read())
            except IndexError:
                if message.content.endswith(extension):
                    linked_image = True

        # if an image is sent to the text-only channel
        if message.channel.id == text_id and image:
            await client.get_guild(server_id).get_channel(image_id).send(content = "From: " + message.author.mention) 
            await client.get_guild(server_id).get_channel(image_id).send(file = discord.File(data, 'redirect.png'))
            await message.delete(delay = 3) # delaying the delete to ensure the image stays uploaded to Discord while being redirected to the image channel

        # if a linked image is sent to the text-only channel
        elif message.channel.id == text_id and linked_image:
            await client.get_guild(server_id).get_channel(image_id).send(content = "From: " + message.author.mention)
            await client.get_guild(server_id).get_channel(image_id).send(content = message.content)
            await message.delete(delay = 3) # delaying the delete to ensure the image stays uploaded to Discord while being redirected to the image channel

        # if a link is sent to the text-only channel
        elif message.channel.id == text_id and link:
            await client.get_guild(server_id).get_channel(link_id).send(content = "From: " + message.author.mention)
            await client.get_guild(server_id).get_channel(link_id).send(content = message.content)
            await message.delete()

        # if neither an image nor a linked image is sent to the image-only channel
        elif message.channel.id == image_id and not image and not linked_image:
            if link:
                await client.get_guild(server_id).get_channel(link_id).send(content = "From: " + message.author.mention) 
                await client.get_guild(server_id).get_channel(link_id).send(content = message.content)
                await message.delete()
            else:
                await client.get_guild(server_id).get_channel(text_id).send(content = "From: " + message.author.mention)
                await client.get_guild(server_id).get_channel(text_id).send(content = message.content)
                await message.delete()

        # if a linked image, image, or text is sent to the link-only channel
        elif message.channel.id == link_id and (not link or linked_image):
            if image:
                await client.get_guild(server_id).get_channel(image_id).send(content = "From: " + message.author.mention)
                await client.get_guild(server_id).get_channel(image_id).send(file = discord.File(data, 'redirect.png'))
                await message.delete(delay = 3)
            elif linked_image:
                await client.get_guild(server_id).get_channel(image_id).send(content = "From: " + message.author.mention)
                await client.get_guild(server_id).get_channel(image_id).send(content = message.content)
                await message.delete(delay = 3)
            else:
                await client.get_guild(server_id).get_channel(text_id).send(content = "From: " + message.author.mention)
                await client.get_guild(server_id).get_channel(text_id).send(content = message.content)
                await message.delete()

# end - on_message

client.run('TOKEN')