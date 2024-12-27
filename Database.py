import aiosqlite
import json

from aiosqlite import Error
from datetime import date, datetime

from Global import Global

class Database:
    DB_FILE = "player_data.db"

    @staticmethod
    async def initialize():
        """
        初始化資料庫，創建玩家資料表。
        """
        async with aiosqlite.connect(Database.DB_FILE) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    player_id INTEGER PRIMARY KEY,
                    player_name TEXT,
                    coins INTEGER DEFAULT 0,
                    last_signed_time TEXT
                )
            ''')
            await db.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    player_id INTEGER PRIMARY KEY,
                    gamble_times INTEGER DEFAULT 0,
                    gamble_history TEXT,
                    FOREIGN KEY (player_id) REFERENCES players (player_id) ON DELETE CASCADE
                )
            ''')
            await db.commit()

    @staticmethod
    async def add_player(player_id: int, player_name: str):
        """
        新增玩家到資料庫。
        """
        async with aiosqlite.connect(Database.DB_FILE) as db:
            await db.execute('''
                INSERT INTO players (player_id, player_name, coins, last_signed_time)
                VALUES (?, ?, 0, NULL)
            ''', (player_id, player_name))

            await db.execute('''
                INSERT INTO history (player_id, gamble_times, gamble_history)
                VALUES (?, 0, NULL)
            ''', (player_id,))
            await db.commit()

    @staticmethod
    async def get_player(player_id: int):
        """
        根據 player_id 查詢玩家資料。
        """
        async with aiosqlite.connect(Database.DB_FILE) as db:
            async with db.execute("SELECT * FROM players WHERE player_id = ?", (player_id,)) as cursor:
                row = await cursor.fetchone()
                if row and row[0]:
                    return row
                else:
                    return None

    @staticmethod
    async def get_history( player_id: int ):
        async with aiosqlite.connect(Database.DB_FILE) as db:
            async with db.execute("SELECT * FROM history WHERE player_id = ?", (player_id,)) as cursor:
                row = await cursor.fetchone()
                if row and row[0]:
                    return row
                else:
                    return None

    @staticmethod
    async def get_signed_time(player_id: int):
        async with aiosqlite.connect(Database.DB_FILE) as db:
            async with db.execute("SELECT last_signed_time FROM players WHERE player_id = ?", (player_id,)) as cursor:
                row =  await cursor.fetchone()
                if row and row[0]:
                    return datetime.strptime( row[0], "%Y-%m-%d").date()
                else:
                    return None

    @staticmethod
    async def update_sign_time(player_id: int):
        """
        更新玩家的簽到時間為現在。
        """
        async with aiosqlite.connect(Database.DB_FILE) as db:
            current_time = date.today().strftime("%Y-%m-%d")
            await db.execute("UPDATE players SET last_signed_time = ? WHERE player_id = ?", (current_time, player_id))
            await db.commit()

    @staticmethod
    async def update_coins(player_id: int, coins: int):
        """
        更新玩家的點數。
        """
        async with aiosqlite.connect(Database.DB_FILE) as db:
            await db.execute("UPDATE players SET coins = coins + ? WHERE player_id = ?", (coins, player_id))
            await db.commit()

    @staticmethod
    async def get_coins( player_id: int ):
        async with aiosqlite.connect( Database.DB_FILE ) as db:
            async with db.execute( "SELECT coins FROM players WHERE player_id = ?", (player_id,) ) as cursor:
                row =  await cursor.fetchone()
                if row and row[0]:
                    return row[0]
                else:
                    return 0

    @staticmethod
    async def update_gamble_times( player_id: int, times: int ):
        async with aiosqlite.connect( Database.DB_FILE ) as db:
            await db.execute( "UPDATE history SET gamble_times = gamble_times + ? WHERE player_id = ?", ( times, player_id ) )
            await db.commit()

    @staticmethod
    async def get_gamble_times( player_id: int ):
        async with aiosqlite.connect( Database.DB_FILE ) as db:
            async with db.execute( "SELECT gamble_times FROM history WHERE player_id = ?", (player_id, ) ) as cursor:
                row =  await cursor.fetchone()
                if row and row[0]:
                    return row[0]
                else:
                    return 0

    @staticmethod
    async def update_gamble_history( player_id: int, results: list ):
        async with aiosqlite.connect( Database.DB_FILE ) as db:
            data = [0] * len( Global.chance )
            async with db.execute( "SELECT gamble_history FROM history WHERE player_id = ?", ( player_id, ) ) as cursor:
                row = await cursor.fetchone()
                if row and row[0]:
                    data = json.loads( row[0] )
                    for result in results:
                        data[ result ] += 1

            if data is None:
                for result in results:
                    data[ result ] += 1

            await db.execute( "UPDATE history SET gamble_history = ? WHERE player_id = ?", ( json.dumps( data ), player_id ) )
            await db.commit()

    @staticmethod
    async def manual_update_history( history: list, player_id: int ):
        async with aiosqlite.connect( Database.DB_FILE ) as db:
            try:
                await db.execute( "UPDATE history SET gamble_history = ? WHERE player_id = ?", ( json.dumps( history ), player_id ) )
                await db.commit()
                return "True"
            except Error as e:
                return f"資料庫錯誤: {str(e)}"
            except Exception as e:
                return f"一般錯誤: {str(e)}"

    @staticmethod
    async def get_gamble_history( player_id: int ):
        async with aiosqlite.connect( Database.DB_FILE ) as db:
            async with db.execute( "SELECT gamble_history FROM history WHERE player_id = ?", ( player_id, ) ) as cursor:
                row = await cursor.fetchone()
                if row and row[0]:
                    return json.loads( row[0] )
                else:
                    return None

    @staticmethod
    async def get_all_players():
        """
        獲取所有玩家資料。
        """
        async with aiosqlite.connect(Database.DB_FILE) as db:
            async with db.execute("SELECT * FROM players") as cursor:
                return await cursor.fetchall()

    @staticmethod
    async def execute_update(query: str, parameters: list):
        """
        執行 UPDATE 指令的函式。

        :param query: SQL UPDATE 指令的字串
        :param parameters: 傳入的參數 (tuple)
        :return: 成功回傳 True，失敗回傳錯誤訊息
        """
        async with aiosqlite.connect(Database.DB_FILE) as db:
            try:
                # 執行 UPDATE 指令
                await db.execute(query, parameters)
                await db.commit()
                return "True"  # 表示執行成功
            except Error as e:
                return f"資料庫錯誤: {str(e)}"
            except Exception as e:
                return f"一般錯誤: {str(e)}"

# 使用範例
async def main():
    # 初始化資料庫
    await Database.initialize()

    # 新增玩家
    await Database.add_player(1, "Player1")
    await Database.add_player(2, "Player2")

    # 獲取玩家資料
    player = await Database.get_player(1)
    print("玩家資料:", player)

    # 更新簽到時間
    await Database.update_sign_time(1)

    # 更新玩家點數
    await Database.update_coins(1, 10)

    # 獲取所有玩家資料
    all_players = await Database.get_all_players()
    print("所有玩家資料:", all_players)

# 測試程式
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
