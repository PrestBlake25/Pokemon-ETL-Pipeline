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

    with db_engine.begin() as conn:
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

        # Creating the Dataframes
         
        pokemon_df = pd.Dataframe(poke_rows)
        types_df = pd.Dataframe(type_rows)
        poke_types_df = pd.Dataframe(poke_type_rows)



        # Writing to the tables
        with db_engine.begin() as conn:
            # Clearing the old rows so reruns won't have duplicate data

            conn.execute(text("""DELETE FROM pokemon_types"""))
            conn.execute(text("""DELETE FROM pokemon"""))
            conn.execute(text("""DELETE FROM types"""))

            types_df.to_sql("types", conn, if_exists="append", index=False)
            pokemon_df.to_sql("pokemon", conn, if_exists="append", index=False)
            poke_types_df.to_sql("pokemon_types", conn, if_exists="append", index=False)

            # ---- Step 5: verify ----
    try:
        with db_engine.connect() as conn:
            # 1. Row counts
            counts = {
                "pokemon": len(poke_rows),
                "types": len(type_rows),
                "pokemon_types": len(poke_type_rows),
            }
            for table, expected in counts.items():
                actual = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                if actual != expected:
                    raise ValueError(f"{table}: expected {expected} rows, found {actual}")

            # Foreign keys
            violations = conn.execute(text("PRAGMA foreign_key_check")).fetchall()
            if violations:
                raise ValueError(f"Foreign key violations: {violations}")

            # NULL base_experience count
            nulls = conn.execute(text(
                "SELECT COUNT(*) FROM pokemon WHERE base_experience IS NULL"
            )).scalar()
            print(f"Pokémon with NULL base_experience: {nulls}")

            #Spot-check join
            result = conn.execute(text("""
                SELECT pokemon.name, types.name AS type, pokemon_types.slot
                FROM pokemon
                JOIN pokemon_types ON pokemon.id = pokemon_types.pokemon_id
                JOIN types ON types.id = pokemon_types.type_id
                WHERE pokemon.name = 'Charizard'
                ORDER BY pokemon_types.slot
            """)).fetchall()
            print(result)

        print("Load verified!")

    except ValueError as error:
        print(f"Verification failed: {error}")
        raise



