import discord
import random
from discord.ext import commands
import io
import os
import aiohttp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

client = commands.Bot(command_prefix="?")

@client.event
async def on_ready():
    print("bot ready.")

@client.command()
async def h(ctx):
    await ctx.send(f"1. ?insta <insta photo link>\n2. ?dlink <direct photolink (Any)>\n<@{ctx.message.author.id}>")

@client.command()
async def dlink(ctx,arg):
    print(arg)
    async with aiohttp.ClientSession() as session:
        async with session.get(str(arg)) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, 'cool_image.png'))

@client.command()
async def insta(ctx,arg):
    #print(arg)
    #chrome_options = webdriver.ChromeOptions()
    #chrome_
    options = Options()
    options.headless = True
    options.binary_location = "/app/.apt/usr/bin/google-chrome"
    #options.add_argument("--window-size=1920,1200")
    #options.add_argument('--disable-gpu')
    #options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options,executable_path="/app/.chromedriver/bin/chromedriver")
    driver.get("https://bloodlink.mrrobi.tech/Welcome/?url="+arg)
    driver.execute_script("document.getElementsByClassName('ibutton')[0].click()")
    driver.implicitly_wait(45)
    elems = driver.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        print(elem.get_attribute("href"))
        async with aiohttp.ClientSession() as session:
            async with session.get(elem.get_attribute("href")) as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'cool_image.png'))

client.run("NzUxMTM0MTcwNDk5MjUyMjQ0.X1EqNQ.EtbOhO_S_mtD56nWpBNXmFMOKV0")