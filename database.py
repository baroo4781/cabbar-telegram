
import aiosqlite

DB_NAME = "cabbar.sqlite3"


async def veritabani_kur():
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            user_id INTEGER,
            reason TEXT
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS levels (
            chat_id INTEGER,
            user_id INTEGER,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 0,
            PRIMARY KEY(chat_id, user_id)
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            chat_id INTEGER PRIMARY KEY,
            log_channel INTEGER,
            welcome_message TEXT
        )
        """)

        await db.commit()


async def uyari_ekle(chat_id, user_id, reason):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO warnings(chat_id,user_id,reason) VALUES(?,?,?)",
            (chat_id, user_id, reason)
        )
        await db.commit()


async def uyari_sayisi(chat_id, user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM warnings WHERE chat_id=? AND user_id=?",
            (chat_id, user_id)
        )
        result = await cursor.fetchone()
        return result[0]


async def xp_ekle(chat_id, user_id, miktar=5):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        INSERT INTO levels(chat_id,user_id,xp,level)
        VALUES(?,?,?,0)
        ON CONFLICT(chat_id,user_id)
        DO UPDATE SET xp = xp + ?
        """, (chat_id, user_id, miktar, miktar))

        cursor = await db.execute(
            "SELECT xp FROM levels WHERE chat_id=? AND user_id=?",
            (chat_id, user_id)
        )
        xp = (await cursor.fetchone())[0]

        level = int((xp / 100) ** 0.5)

        await db.execute(
            "UPDATE levels SET level=? WHERE chat_id=? AND user_id=?",
            (level, chat_id, user_id)
        )

        await db.commit()
        return xp, level
