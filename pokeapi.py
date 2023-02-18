from typing import Optional
from fastapi import FastAPI, Path, HTTPException, status
from pydantic import BaseModel
from database import get_poke_by_name, get_poke_by_type, 
                     add_poke_to_db, update_poke, delete_poke

app = FastAPI()
@app.get("/")

# Welcoming page
def root():
    raise HTTPException(status_code=status.HTTP_200_OK,  
                        detail="Welcome to PokeAPI")

################# GET #################
# First API call - get a pokemon by name
@app.get("/poke/{pokemon_name}")
def get_pokemon_by_name(pokemon_name: str = Path(None,  
                       description="Name of the pokemon you'd like to retrieve")):
    pokemon = get_poke_by_name(pokemon_name)
    if not pokemon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail="Pokemon not found")
    return {"Pokemon": pokemon[0],
            "Types": [pokemon[1], pokemon[2]],
            "HP": pokemon[4],
            "Attack": pokemon[5],
            "Special Attack": pokemon[6],
            "Defense": pokemon[7],
            "Special Defense": pokemon[8],
            "Speed": pokemon[9],
            "Generation": pokemon[10],
            "Legenday": pokemon[11]
            }

# get multiple pokemon based on primary and secondary type
@app.get("/poketype/{poke_type}")
def get_pokemon_by_type(poke_type: str = Path(None,
                        description="Primary type of the pokemons you want to query"),
                        type2: Optional[str] = None):
    pokemons = get_poke_by_type(poke_type, type2)
    if not pokemons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No pokemon with this type")
    result = {}
    for idx, pokemon in enumerate(pokemons):
        result[idx] = {"Pokemon": pokemon[0],
                       "Types": [pokemon[1], pokemon[2]],
                       "HP": pokemon[4],
                       "Attack": pokemon[5],
                       "Special Attack": pokemon[6],
                       "Defense": pokemon[7],
                       "Special Defense": pokemon[8],
                       "Speed": pokemon[9],
                       "Generation": pokemon[10],
                       "Legenday": pokemon[11]
                       }
    return result

################# POST, PUT and, DELETE #################
# add a class that defines a pokemon with its attributes and attribute types
class Pokemon(BaseModel):
    name: str
    primary_type: str
    secondary_type: str
    sum_stats: int
    hit_points: int
    attack_strength: int
    defensive_strength: int
    special_attack_strength: int
    special_defensive_strength: int
    speed_strength: int
    generation_type: int
    is_legendary: bool

# use class in requests
@app.post("/newPoke/{pokemon_name}")
def create_pokemon(pokemon_name: str, pokemon: Pokemon):
    if get_poke_by_name(pokemon_name):
        raise HTTPException(
              status_code=status.HTTP_406_NOT_ACCEPTABLE, 
              detail="Pokemon already exists") 
   add_poke_to_db(pokemon.name, pokemon.primary_type, 
                   pokemon.secondary_type,
                   pokemon.sum_stats, pokemon.hit_points,
                   pokemon.attack_strength,
                   pokemon.special_attack_strength,
                   pokemon.defensive_strength,
                   pokemon.special_defensive_strength)
   raise HTTPException(
         status_code=status.HTTP_201_CREATED,  
         detail="Pokemon created successfully")