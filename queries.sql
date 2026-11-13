--Listing the names of all Pokemon with a height > 10, sorted tallest first
SELECT name, height
FROM pokemon
WHERE height > 10
ORDER BY height DESC;


-- Retrieving the 10 heaviest Pokemon with their weights
SELECT name, weight
FROM pokemon
ORDER BY weight DESC, name
LIMIT 10;


-- What is the average weight and height across all Pokemon?
SELECT
    AVG(height) AS avg_height,
    AVG(weight) AS avg_weight
FROM pokemon;

-- List all Pokemon along with their type name(s)

SELECT 
    p.name AS pokemon_name,
    t.name AS type_name
FROM pokemon p  
JOIN pokemon_types pt 
ON p.id = pt.pokemon_id
JOIN types t 
ON pt.type_id = t.id;

-- How many Pokemon does each type have?
SELECT 
    t.name AS type_name,
    COUNT(pt.pokemon_id) AS num_of_pokemon
FROM types t 
LEFT JOIN pokemon_types pt
ON pt.type_id = t.id
GROUP BY t.name
ORDER BY num_of_pokemon DESC, type_name;


-- Returning all Fire type Pokemon
SELECT 
    p.name AS pokemon_name
FROM pokemon p
JOIN pokemon_types pt 
ON p.id = pt.pokemon_id
JOIN types t
ON pt.type_id = t.id
WHERE t.name = 'Fire';