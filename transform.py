from collections import Counter

def transform(raw_poke_data):
    poke_rows = [] # holds id, name, experience, height, and weight of a pokemon
    unique_types = {} # holds the key-value pairs of {type_id : type}
    poke_type_rows= [] # holds id, type_id and slot (tells whethter one is a primary type(1) or a secondary type (2))


    for record in raw_poke_data:
        poke_rows.append({
            "id": record["id"],
            "name": record["name"].title(),
            "height": record["height"],
            "weight": record["weight"],
            "base_experience": record.get("base_experience")
        })
        for type_entry in record["types"]:
            slot = type_entry["slot"]
            type_name = type_entry["type"]["name"].title()
            type_url = type_entry["type"]["url"]
            
            type_id = int(type_url.rstrip("/").split("/")[-1])

            unique_types.update({type_id : type_name})

            poke_type_rows.append(
                {
                    "pokemon_id" : record["id"],
                    "type_id" : type_id,
                    "slot" : slot
                }
            )


        # 1. No duplicate Pokémon ids
    pokemon_ids = [row["id"] for row in poke_rows]
    assert len(pokemon_ids) == len(set(pokemon_ids)), "Duplicate Pokémon ids found"

    # 2. Every type_id in the links exists in unique_types
    for link in poke_type_rows:
        assert link["type_id"] in unique_types, f"Unknown type_id: {link['type_id']}"

    # 3. Each Pokémon has one or two type rows
    type_counts = Counter(link["pokemon_id"] for link in poke_type_rows)
    for pokemon_id in pokemon_ids:
        assert type_counts[pokemon_id] in (1, 2), f"Pokémon {pokemon_id} has {type_counts[pokemon_id]} types"

    # ---- Step 8: return the three row sets ----

    types_rows = [
        {"id": type_id, "name": type_name}
        for type_id, type_name in unique_types.items()
    ]






    return poke_rows, types_rows, poke_type_rows

    