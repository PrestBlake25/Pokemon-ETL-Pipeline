from sqlalchemy import create_engine, event, text
import pandas as pd


def load(poke_rows, type_rows, poke_type_rows, db_path="pokemon.db"):
    
    # Creating the database engine and foreign keys
    db_engine = create_engine("sqlite:///pokemon.db")

    @event.listens_for(db_engine, "connect")
    def enable_foreign_keys(dbapi_connect, connection_record):
        cursor = dbapi_connect.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.close()

    # Creating the tables

    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS types (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS pokemon (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                height INTEGER,
                weight INTEGER,
                base_experience INTEGER
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS pokemon_types (
                pokemon_id INTEGER NOT NULL,
                type_id INTEGER NOT NULL,
                slot INTEGER NOT NULL,
                PRIMARY KEY (pokemon_id, type_id),
                FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
                FOREIGN KEY (type_id) REFERENCES types(id)
            )
        """))

