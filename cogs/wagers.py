""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands


# Here we name the cog and create a new class for the cog.
class Wagers(commands.Cog, name="wagers"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_group(
        name="points",
        description="Manage points of a user on a server.",
    )
    async def points(self, context: Context) -> None:
        """
        Manage points of a user on a server.

        :param context: The hybrid command context.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Please specify a subcommand.\n\n**Subcommands:**\n`add` - Add a points to a user, requires **{User ID}, {Points}** \n`remove` - Remove a points from a user, requires **{User ID}, {Points}**\n`list` - List all points of a user, requires **{User ID}**",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @points.command(
        name="add",
        description="Adds a points to a user in the server.",
    )
    @app_commands.describe(
        user="The user that should have points.",
        points="The amount the user should have points",
    )
    async def points_add(
        self, context: Context, user: discord.User, points: int = 0
    ) -> None:
        """
        points added to user in his account.

        :param context: The hybrid command context.
        :param user: The user that should have points
        :param reason: The reason for the points. Default is "Not specified".
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        total_points = await self.bot.database.add_points(
            user.id, context.guild.id, points
        )
        embed = discord.Embed(
            description=f"**{member}** has received **{points}** from **{context.author}**!\nTotal points for this user: {total_points}",
            color=0xBEBEFE,
        )
        embed.add_field(name="Points:", value=points)
        await context.send(embed=embed)
        try:
            await member.send(
                f"You were given points by **{context.author}** in **{context.guild.name}**!\nPoints: +{points}"
            )
        except:
            # Couldn't send a message in the private messages of the user
            await context.send(
                f"{member.mention}, you were given points by **{context.author}**!\nPoints: +{points}"
            )

    @points.command(
        name="remove",
        description="Removes points from a user in the server.",
    )
    @app_commands.describe(
        user="The user that should get their points removed.",
    )
    async def points_remove(
        self, context: Context, user: discord.User, points: int
    ) -> None:
        """
        Warns a user in his private messages.

        :param context: The hybrid command context.
        :param user: The user that should get their points removed.
        :param points: The number of points that should be removed.
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        total = await self.bot.database.remove_points(user.id, context.guild.id,points)
        embed = discord.Embed(
            description=f"I've removed **{points}** points from **{member}**!\nTotal points for this user: {total}",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)

    @points.command(
        name="list",
        description="Shows the points of a user in the server.",
    )
    @app_commands.describe(user="The user you want to get the points of.")
    async def points_list(self, context: Context, user: discord.User) -> None:
        """
        Shows the points of a user in the server.

        :param context: The hybrid command context.
        :param user: The user you want to get the points of.
        """
        user_points = await self.bot.database.get_points(user.id, context.guild.id)
        embed = discord.Embed(title=f"Points for {user}", color=0xBEBEFE)
        description = ""
        if user_points <= 0:
            description = "This user is broke and has no points."
        else:
            description += f"• {user_points}\n"
        embed.description = description
        await context.send(embed=embed)

    @commands.hybrid_group(
        name="wagers",
        description="Manage wagers of a user on a server.",
    )
    async def wagers(self, context: Context) -> None:
        """
        Manage wagers of a user on a server.

        :param context: The hybrid command context.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Please specify a subcommand.\n\n**Subcommands:**\n`create_bet` - create a bet to a user, requires **{User ID}, {Points}** \n`confirm` - confirm a bet from a user, requires **{User ID}, {Points}**",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @wagers.command(name='create_bet')
    async def create_bet(self, context: Context, member: discord.Member, points: int, *, wager: str):
        # # Sending a message to the channel
        await context.send(f'Creating a bet between {context.author.mention} and {member.mention} with {points} points on "{wager}".')
        
        print(member)


        # Interacting with the database
 
        #     if user1_points and user2_points and user1_points[0] >= points and user2_points[0] >= points:
        #         await cursor.execute('INSERT INTO bets (user1_id, user2_id, wager, points) VALUES (?, ?, ?, ?)',
        #                             (str(ctx.author.id), str(member.id), wager, points))
        #         await db.commit()
        #         await ctx.send(f'Bet created between {ctx.author.mention} and {member.mention} with {points} points on "{wager}".')
        #     else:
        #         await ctx.send(f'Both users must have at least {points} points to place this bet.')




# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Wagers(bot))
