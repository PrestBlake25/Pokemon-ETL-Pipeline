def transform(raw_poke_data):
    poke_rows = [] # holds id, name, experience, height, and weight of a pokemon
    unique_types = {} # holds the key-value pairs of {type_id : type}
    poke_type_rows= [] # holds id, type_id and slot (tells whethter one is a primary type(1) or a secondary type (2))


    for record in raw_poke_data:
        poke_rows.append({
            "id": record["id"],
            "name": record["name"],
            "height": record["height"],
            "weight": record["weight"],
            "base_experience": record.get("base_experience")
        })
        pass

    