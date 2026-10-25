import requests, json

base_url = 'https://pokeapi.co/api/v2/pokemon/'

def fetch_one_pokemon(id):
    poke_info = f'{base_url}/{id}'
    response = requests.get(poke_info)

    if response.status_code == 200:
        print(response.json()["name"], " retrieval sucessful!")
        return response.json()
    else:
        print(f"Failure to retrieve pokemon. Status code: {response.status_code}")


def extract(count):
    poke_list = []

    for id in range(1, count + 1):
        poke = fetch_one_pokemon(id)
        poke_list.append(poke)

    raw_poke_json = json.dumps(poke_list, indent = 4)
    with open('raw_poke.json', "w") as file:
        file.write(raw_poke_json)
    print(f"{len(poke_list)} Pokemon returned!")

    return poke_list
    



