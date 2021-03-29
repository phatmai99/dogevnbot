from datetime import datetime, timedelta
import pytz
import discord
import random
import time
import asyncio
from discord.ext import commands


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

prefix = 'd!'
guild = ''
congra_channel = ''
baodanh_channel = ''
welcome_channel = ''
noiquy_channel = ''
emoji_doge = ''
emoji_cate = ''
emoji_hamster = ''
role_cate = ''
role_doge = ''
role_hamster = ''
base_role = ''
myguild = ''
log_channel = ''
log_image_channel = None

bot = commands.Bot(command_prefix=prefix)


def timenow(location):
    if location.lower() == 'vn':
        return get_time(pytz.timezone('Asia/Ho_Chi_Minh'))
    elif location.lower() == 'usw':
        return get_time((pytz.timezone('US/Pacific')))
    elif location.lower() == 'use':
        return get_time((pytz.timezone('US/Eastern')))
    elif location.lower() == 'ausmel':
        return get_time((pytz.timezone('Australia/Melbourne')))


def get_time(timezone):
    thoigian = datetime.now(timezone)
    day = thoigian.day
    month = thoigian.month
    year = thoigian.year
    hour = thoigian.hour
    minute = thoigian.minute
    second = thoigian.second
    s = f"""{hour}:{minute}:{second} {day}/{month}/{year}"""
    return s


@bot.event
async def on_ready():
    global guild, congra_channel, baodanh_channel, welcome_channel, noiquy_channel, emoji_doge, emoji_cate, \
        emoji_hamster, role_cate, role_doge, role_hamster, base_role, prefix, myguild, log_channel, log_image_channel

    guild = bot.get_guild(732273364709933108)
    for channel in guild.channels:
        ten_channel = str(channel.name)
        if ten_channel == 'j-cong-vao':
            welcome_channel = channel
        elif ten_channel == 'layrole':
            baodanh_channel = channel
        elif ten_channel == 'j-cong-ra':
            congra_channel = channel
        elif ten_channel == 'noi-quy':
            noiquy_channel = channel

    for role in guild.roles:
        ten_role = str(role.name).lower()
        if ten_role == 'cho ngu':
            role_doge = role
        elif ten_role == 'meo ngu':
            role_cate = role
        elif ten_role == 'hamster ngu':
            role_hamster = role
        elif ten_role == 'cong dan luong thien':
            base_role = role

    emoji_doge = bot.get_emoji(732512784637493289)
    emoji_cate = bot.get_emoji(732512768132907119)
    emoji_hamster = bot.get_emoji(733308899259580467)
    prefix = 'd!'
    log_image_channel = bot.get_channel(826085577248997456)

    myguild = bot.get_guild(688502199168663553)
    log_channel = bot.get_channel(737780215459217528)
    await bot.change_presence(activity=discord.Game("with my master uwu"))
    print(f"""Logged in\nVersion: {discord.__version__}\n----------""")


@bot.event
async def on_member_join(member):
    await welcome_channel.send(
        f"""j xin chao toi discord cua group dogevn {member.mention}, doc noi quy tai {noiquy_channel.mention} va lay role tai {baodanh_channel.mention} nhe. Chuc ban zui ze""")

    await log_channel.send(f"""{member.name} joined at {timenow('vn')}""")


@bot.event
async def on_member_remove(member):
    await congra_channel.send(f"""{member.name} da bi exciter bat vao noi luc {timenow('vn')}""")
    await log_channel.send(f"""{member.name} aka {member.nick} left at {timenow('vn')}""")


@bot.event
async def on_message_delete(message):
    if message.guild == guild:
        if not message.author.bot:
            desc = message.content
            if len(message.attachments) != 0:
                for i in range(len(message.attachments)):
                    desc += f"""{message.attachments[i].url}\n"""
            embed = discord.Embed(
                description=f"""{desc} at {timenow('vn')}""",
                colour=discord.Colour.red()
            )
            author = message.author
            embed.set_author(name=f"""{author.name} in {message.channel.name}""", icon_url=author.avatar_url)
            await log_channel.send(f"""{message.author} deleted a message at {timenow('vn')}""")
            await log_channel.send(embed=embed)
            await log_channel.send(f"""----------------""")


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 734015494079774730:
        if payload.member.top_role.id == 732273364709933108:
            await payload.member.add_roles(base_role)
        if payload.emoji == emoji_cate:
            await payload.member.add_roles(role_cate)
        elif payload.emoji == emoji_doge:
            await payload.member.add_roles(role_doge)
        elif payload.emoji == emoji_hamster:
            await payload.member.add_roles(role_hamster)


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == 734015494079774730:
        mem = await guild.fetch_member(payload.user_id)
        if payload.emoji == emoji_cate:
            await mem.remove_roles(role_cate)
        elif payload.emoji == emoji_doge:
            await mem.remove_roles(role_doge)
        elif payload.emoji == emoji_hamster:
            await mem.remove_roles(role_hamster)


@bot.command()
async def sua(ctx, args):
    ctx.send(f"""{args}""")


@bot.command()
async def changeprefix(ctx, args):
    global prefix
    prefix = args
    await ctx.send(f"""server prefix is changed to "{args}""")


@bot.command()
async def help(ctx):
    global prefix
    await ctx.send(f"""Day la waifu cua Phatto-sama UwU, prefix cua server la {prefix}""")


@bot.command(aliases=['random'])
async def pick(ctx, *args):
    await ctx.send(f"""toi chon {random.choice(list(args))}""")


@bot.command()
async def say(ctx, args):
    await ctx.message.delete()
    await ctx.send(f"""{ctx.message.content[6:]}""")


@bot.command()
async def sua(ctx):
    i = random.randint(1, 10)
    s = ""
    for count in range(i):
        s += "gau "
    ctx.send(f"""{s}""")


@bot.event
async def on_message(ctx):
    # mk id: 609737193854074891
    # hi
    if ctx.author.id == 609737193854074891:
        if len(ctx.attachments) != 0:
            if not ctx.author.bot:
                img = await ctx.attachments[0].to_file()
                await log_image_channel.send(content=f"""{get_time()} in channel {ctx.channel}""", file=img)
        else:
            await log_image_channel.send(f"""{get_time()} in channel {ctx.channel}: {ctx.content}""")


bot.run(token)
