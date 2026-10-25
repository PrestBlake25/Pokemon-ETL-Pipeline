# Pokémon ETL Pipeline

ETL pipeline that pulls Pokémon data from PokéAPI, reshapes it into a relational schema, validates it, and loads it into a SQLite database.

## Overview
The pipeline extracts the first 151 Pokémon from PokéAPI, flattens the nested JSON into three normalized tables, and loads them into SQLite with enforced primary and foreign keys. I built it to practice the full extract, transform, and load cycle, including data validation and safe reruns.

## Architecture
PokéAPI -> extract.py -> transform.py -> load.py -> SQLite (pokemon.db)

- **extract.py** fetches one record per Pokémon and caches the raw JSON in `raw_poke.json`.
- **transform.py** flattens each record into three row sets and runs validation checks.
- **load.py** creates the tables, writes the data, and verifies the result.

## Tech Stack
Python, Requests, Pandas, SQLAlchemy, SQLite

## Database Schema
- `pokemon`: id (PK), name, height, weight, base_experience
- `types`: id (PK), name
- `pokemon_types`: pokemon_id (PK, FK), type_id (PK, FK), slot

`pokemon_types` is a junction table for the many-to-many relationship between Pokémon and types. `slot` is 1 for a primary type and 2 for a secondary type.

## How to Run
```bash
git clone [your repo URL]
cd [your repo folder]
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
The pipeline creates `pokemon.db` in the project folder.

## Sample Output
[Paste the first 5 rows from your own database as a table.]

## Example Queries
```sql
-- Types of a single Pokémon, primary type first
SELECT pokemon.name, types.name AS type, pokemon_types.slot
FROM pokemon
JOIN pokemon_types ON pokemon.id = pokemon_types.pokemon_id
JOIN types ON types.id = pokemon_types.type_id
WHERE pokemon.name = 'Charizard'
ORDER BY pokemon_types.slot;
```

## Data Quality Checks
- No duplicate Pokémon ids
- Every `type_id` in `pokemon_types` exists in `types`
- Every Pokémon has one or two type rows
- Row counts in the database match the rows transformed
- SQLite foreign key check returns no violations

## Design Notes
- **Idempotent:** rerunning the pipeline clears the tables and reloads, so it never creates duplicates.
- **Keys enforced:** foreign keys are turned on for every connection, and tables are created with explicit primary and foreign keys.
- **Missing values:** a missing `base_experience` is stored as NULL instead of 0.
- **Cached raw data:** the raw API responses are saved so transform can be rerun without calling the API.

## Results
- Pokémon loaded: 151
- Types: 17
- Pokémon-type links: 218

## Future Improvements
- Add more generations
- Convert height and weight to meters and kilograms
- Add a summary view and a dashboard on top of the database
- Schedule runs with Airflow or GitHub Actions