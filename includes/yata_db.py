# import standard modules
import json
import asyncio
import aiohttp
import re
import os
import asyncpg
import psycopg2


async def get_yata_user(tornId):
    # get YATA user
    db_cred = json.loads(os.environ.get("DB_CREDENTIALS"))
    dbname = db_cred["dbname"]
    del db_cred["dbname"]
    con = await asyncpg.connect(database=dbname, **db_cred)
    user = await con.fetch(f'SELECT "tId", "name", "botPerm" FROM player_player WHERE "tId" = {tornId};')
    # key = await con.fetch(f'SELECT "value" FROM player_key WHERE "tId" = {tornId};')
    await con.close()

    return user


async def get_yata_key(tornId):
    # get YATA user
    db_cred = json.loads(os.environ.get("DB_CREDENTIALS"))
    dbname = db_cred["dbname"]
    del db_cred["dbname"]
    con = await asyncpg.connect(database=dbname, **db_cred)
    key = await con.fetch(f'SELECT "value" FROM player_key WHERE "tId" = {tornId};')
    print("get_yata_key", key)
    await con.close()

    return key


async def push_guild_name(guild):
    """Writes the actual guild name in YATA database"""
    # get YATA user
    db_cred = json.loads(os.environ.get("DB_CREDENTIALS"))
    dbname = db_cred["dbname"]
    del db_cred["dbname"]
    con = await asyncpg.connect(database=dbname, **db_cred)
    await con.execute('UPDATE bot_guild SET "guildName"=$1, "guildOwnerId"=$2, "guildOwnerName"=$3 WHERE "guildId"=$4', guild.name, guild.owner_id, guild.owner.name, guild.id)
    await con.close()


def load_configurations(bot_id):
    db_cred = json.loads(os.environ.get("DB_CREDENTIALS"))
    con = psycopg2.connect(**db_cred)
    cur = con.cursor()
    cur.execute(f"SELECT token, variables FROM bot_discordapp WHERE id = {bot_id};")
    token, configs = cur.fetchone()
    cur.close()
    con.close()
    return token, configs
