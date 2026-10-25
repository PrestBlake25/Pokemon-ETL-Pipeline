from extract import extract
from transform import transform
from load import load

def etl():
    for attempt in range(0, 3):
        print(f"\n\nThis is Attempt #{attempt}")
        raw_data = extract(151)
        pokemon_rows, types_rows, pokemon_type_rows = transform(raw_data)
        print("Number Of Pokemon: ",len(pokemon_rows), "\nNumber Of Types: ", len(types_rows), "\nNumber of Pokemon Link Rows: ",len(pokemon_type_rows))
        print(list(type["name"] for type in types_rows))
        load(pokemon_rows, types_rows, pokemon_type_rows)

etl()
