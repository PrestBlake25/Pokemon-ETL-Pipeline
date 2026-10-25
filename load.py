from sqlalchemy import create_engine, event, text

def load(poke_rows, type_rows, poke_type_rows, db_path="pokemon.db"):
    db_engine = create_engine("sqlite:///pokemon.db")

    @event.listens_for(db_engine, "connect")
    def enable_foreign_keys(dbapi_connect, connection_record):
        cursor = dbapi_connect.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.close()

