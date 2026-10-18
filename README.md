# Pokémon ETL Pipeline

Automated ETL pipeline that pulls Pokémon data from PokéAPI, cleans it, and loads it into a SQLite database.

## Overview
[2 to 3 sentences: what the pipeline does and why you built it.]

## Architecture
PokéAPI -> extract.py -> transform.py -> load.py -> SQLite (pokemon.db)

Data quality checks run between transform and load. [Add a diagram image here if you make one.]

## Tech Stack
Python, Requests, Pandas, SQLite

## Database Schema
- `pokemon`: id, name, height_m, weight_kg
- `types`: id, name
- `pokemon_types`: pokemon_id, type_id, slot
- `pokemon_summary` (view): name, height_m, weight_kg, types

## How to Run
```bash
git clone [your repo URL]
cd pokemon-etl-pipeline
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run_pipeline.py
```
The pipeline creates `pokemon.db` in the project folder.

## Sample Output
[Paste the first 5 rows of pokemon_summary as a table.]

Full sample: [sample_output.csv](sample_output.csv)

## Example Queries
```sql
-- [Describe the query]
[your SQL]
```

## Data Quality Checks
- [No duplicate or null IDs]
- [Every Pokémon has at least one type]
- [Height and weight are positive]
- [Foreign keys match parent tables]

## Design Notes
- **Idempotent:** rerunning the pipeline replaces the data instead of duplicating it.
- **Resilient:** failed API requests are retried before being skipped.
- **Unit cleanup:** height and weight are converted from the API's raw units to meters and kilograms.

## Results
- Records loaded: [N]
- Tables: 3 plus 1 view
- Checks passed: [N]
- Run time: [N seconds]

## Future Improvements
- Schedule runs with Airflow or GitHub Actions
- Add more generations
- Build a dashboard on top of the database
