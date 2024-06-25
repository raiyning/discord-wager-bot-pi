""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

import random

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context


class Choice(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.value = None

    @discord.ui.button(label="Heads", style=discord.ButtonStyle.blurple)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        self.value = "heads"
        self.stop()

    @discord.ui.button(label="Tails", style=discord.ButtonStyle.blurple)
    async def cancel(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        self.value = "tails"
        self.stop()


class RockPaperScissors(discord.ui.Select):
    def __init__(self,context: Context,bot) -> None:
        self.bot = bot
        self.context = context
        options = [
            discord.SelectOption(
                label="Scissors", description="You choose scissors.", emoji="✂"
            ),
            discord.SelectOption(
                label="Rock", description="You choose rock.", emoji="🪨"
            ),
            discord.SelectOption(
                label="Paper", description="You choose paper.", emoji="🧻"
            ),
        ]
        super().__init__(
            placeholder="Choose...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        choices = {
            "rock": 0,
            "paper": 1,
            "scissors": 2,
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]

        bot_choice = random.choice(list(choices.keys()))
        bot_choice_index = choices[bot_choice]

        result_embed = discord.Embed(color=0xBEBEFE)
        result_embed.set_author(
            name=interaction.user.name, icon_url=interaction.user.display_avatar.url
        )

        winner = (3 + user_choice_index - bot_choice_index) % 3
        if winner == 0:
            result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice} and I've chosen {bot_choice}.`"
            result_embed.colour = 0xF59E42
            print(self.context.author.id)
        elif winner == 1:
            points = 60
            total_points = await self.bot.database.add_points( self.context.author.id, self.context.guild.id, points)
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}.\n Your balance: `{total_points}`"
            result_embed.colour = 0x57F287
        else:
            points= 30
            total_points = await self.bot.database.remove_points(self.context.author.id, self.context.guild.id,points)
            result_embed.description = f"**You lost!**\nYou've chosen {user_choice} and I've chosen {bot_choice}.\n Your balance: `{total_points}`"
            result_embed.colour = 0xE02B2B
            print(self.context.author.id)

        await interaction.response.edit_message(
            embed=result_embed, content=None, view=None
        )


class RockPaperScissorsView(discord.ui.View):
    def __init__(self,context: Context, bot) -> None:
        super().__init__()
        self.add_item(RockPaperScissors(context,bot))


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="randomfact", description="Get a random fact.")
    async def randomfact(self, context: Context) -> None:
        """
        Get a random fact.

        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://uselessfacts.jsph.pl/random.json?language=en"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0xD75BF4)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="coinflip", description="Make a coin flip, but give your bet before."
    )
    async def coinflip(self, context: Context) -> None:
        """
        Make a coin flip, but give your bet before.

        :param context: The hybrid command context.
        """
        buttons = Choice()
        embed = discord.Embed(description="What is your bet?", color=0xBEBEFE)
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.
        result = random.choice([ "tails"])
        points =15
        if buttons.value == result:
            total_points = await self.bot.database.add_points(
            context.author.id, context.guild.id, points
        )
            embed = discord.Embed(
                description=f"Correct! You guessed `{buttons.value}` and I flipped the coin to `{result}`.\n Your balance: `{total_points}`",
                color=0xBEBEFE,
            )
        else:  
            total_points = await self.bot.database.remove_points(context.author.id, context.guild.id,points)       
            embed = discord.Embed(
                description=f"Woops! You guessed `{buttons.value}` and I flipped the coin to `{result}`, better luck next time!\n Your balance: `{total_points}`",
                color=0xE02B2B,
            )
        await message.edit(embed=embed, view=None, content=None)

    @commands.hybrid_command(
        name="rps", description="Play the rock paper scissors game against the bot."
    )
    async def rock_paper_scissors(self, context: Context) -> None:
        """
        Play the rock paper scissors game against the bot.

        :param context: The hybrid command context.
        """
        view = RockPaperScissorsView(context, self.bot)
        await context.send("Please make your choice", view=view)

    @commands.hybrid_command(
        name="steal", description="you have a chance to steal points from another user."
    )
    async def steal(self, context: Context, user: discord.User) -> None:
        """
        you have a chance to steal points from another user. the less points you own, the higher the chance to steal. 5 percent chance for points upto 1000

        :param context: The hybrid command context. 
        :param user: The user that you are stealing points from.
        
        """
        # chance to 
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        stolen_points = random.randint(0,1000)

        if random.randint(0,100) < 50: 
            user_points = await self.bot.database.add_points(
                context.author.id, context.guild.id, stolen_points
            )
            removed_total = await self.bot.database.remove_points(user.id, context.guild.id,stolen_points)
            embed = discord.Embed(
                description=f"**{context.author}** has stolen **{stolen_points}** points from **{member}**!\nYour total points are now: {user_points}",
                color=0xBEBEFE,
            )
            embed.add_field(name="Points:", value=user_points)
        else:
            removed_total = await self.bot.database.remove_points(context.author.id, context.guild.id,stolen_points)
            embed = discord.Embed(
                description=f"**You did not manage to find anything, better luck next time** \nYour total points are now: {removed_total}",
                color=0xE02B2B,
            )
            embed.add_field(name="Points:", value=removed_total)
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Fun(bot))
