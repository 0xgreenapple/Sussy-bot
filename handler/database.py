import contextlib
import json
import os
# database
import asyncpg
import dotenv




password = os.environ['DBPASSWORD']
host = os.environ['DBHOST']


@contextlib.asynccontextmanager
async def create_database_connection():
    print("conn happening")
    connection = await asyncpg.connect(
        user="hlzrnjfduekgap",
        password=password,
        database="dfcd7pseoj603e",
        host=host
    )
    await initialize_database_connection(connection)
    try:
        yield connection
    finally:
        print("database closed")
        await connection.close()

async def create_database_pool():
    print("happening")
    return await asyncpg.create_pool(
        user="hlzrnjfduekgap",
        password=password,
        database="dfcd7pseoj603e",
        host=host,
        init=initialize_database_connection
    )


async def initialize_database_connection(connection):
    print("happening inini")
    await connection.set_type_codec(
        "jsonb",
        encoder=json.dumps, decoder=json.loads,
        schema="pg_catalog"
    )