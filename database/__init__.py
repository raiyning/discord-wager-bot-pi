""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""


import aiosqlite


class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def add_warn(
        self, user_id: int, server_id: int, moderator_id: int, reason: str
    ) -> int:
        """
        This function will add a warn to the database.

        :param user_id: The ID of the user that should be warned.
        :param reason: The reason why the user should be warned.
        """
        rows = await self.connection.execute(
            "SELECT id FROM warns WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            print(result)
            warn_id = result[0] + 1 if result is not None else 1
            await self.connection.execute(
                "INSERT INTO warns(id, user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?, ?)",
                (
                    warn_id,
                    user_id,
                    server_id,
                    moderator_id,
                    reason,
                ),
            )
            await self.connection.commit()
            return warn_id

    async def remove_warn(self, warn_id: int, user_id: int, server_id: int) -> int:
        """
        This function will remove a warn from the database.

        :param warn_id: The ID of the warn.
        :param user_id: The ID of the user that was warned.
        :param server_id: The ID of the server where the user has been warned
        """
        await self.connection.execute(
            "DELETE FROM warns WHERE id=? AND user_id=? AND server_id=?",
            (
                warn_id,
                user_id,
                server_id,
            ),
        )
        await self.connection.commit()
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0

    async def get_warnings(self, user_id: int, server_id: int) -> list:
        """
        This function will get all the warnings of a user.

        :param user_id: The ID of the user that should be checked.
        :param server_id: The ID of the server that should be checked.
        :return: A list of all the warnings of the user.
        """
        rows = await self.connection.execute(
            "SELECT user_id, server_id, moderator_id, reason, strftime('%s', created_at), id FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list

    async def add_points( self, user_id, server_id: int, points: int)-> int:
            """
            Warns a user in his private messages.

            :param context: The hybrid command context.
            :param user_id: The user that should have points.
            :param server_id: The server the user is in
            :param points: The points to be added
            """

            rows = await self.connection.execute('SELECT points FROM users WHERE user_id = ? AND server_id = ?', (str(user_id),str(server_id)))
            async with rows as cursor:
                result = await cursor.fetchone()
            if result:
                new_points = result[0] + points
                await self.connection.execute('UPDATE users SET points = ? WHERE user_id = ? AND server_id = ?', (new_points, str(user_id),str(server_id)))
            else:
                new_points = points
                await self.connection.execute('INSERT INTO users (user_id, server_id, points) VALUES (?, ?, ?)', (str(user_id),str(server_id), points))
            await self.connection.commit()
            return new_points

    async def get_points(self, user_id: int, server_id: int) -> list:
        """
        This function will get all the warnings of a user.

        :param user_id: The ID of the user that should be checked.
        :param server_id: The ID of the server that should be checked.
        :return: A list of all the warnings of the user.
        """
        rows = await self.connection.execute(
            "SELECT user_id, server_id, points FROM users WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        result = await rows.fetchone()
        return result[2]

    async def remove_points(self, user_id: int, server_id: int, lost_points: int) -> int:
        """
        This function will remove points from a user in the database.

        :param points: The amount of points
        :param user_id: The ID of the user that has lost points.
        :param server_id: The ID of the server where the user has lost points
        """
        rows = await self.connection.execute(
            "SELECT user_id, server_id, points FROM users WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        result = await rows.fetchone()
        new_points = result[2] - lost_points if result is not None else 1
        if result:
            await self.connection.execute('UPDATE users SET points = ? WHERE user_id = ? AND server_id = ?', (new_points, str(user_id),str(server_id)))
        else:
            await self.connection.execute('INSERT INTO users (user_id, server_id, points) VALUES (?, ?, ?)', (str(user_id),str(server_id), new_points))
        await self.connection.commit()
        return new_points
