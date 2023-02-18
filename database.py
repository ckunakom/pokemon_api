from pathlib import Path
import sqlite3
import pandas as pd

# Create file for dataset
DB_FILENAME = "poke_db.db"

def init_db():
    # Create the dataset file if it's not there
    if not Path(DB_FILENAME).is_file():
        Path(DB_FILENAME).touch()

# Load the dataset to the database file
def load_csv_to_db():
    init_db()
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS Pokemons (idx int, name text,
        type1 text,type2 text, sum_stats int, hp int, attack int,
        special_attack int, defense int, special_defense int), speed int,
        generation int, is_legend boolean)''')
    poke_data = pd.read_csv('Pokemon.csv')
    poke_data.drop(['Speed', 'Generation', 'Legendary'], axis=1,
                    inplace=True)
    poke_data.columns = ['idx', 'name', 'type1', 'type2', 
                          'sum_stats', 'hp', 'attack',
                          'special_attack', 'defense',    
                          'special_defense', 'speed', 'generation',
                          'is_legend']
    poke_data.to_sql('Pokemons', conn, if_exists='append',
                      index=False)

# Table exists or not
def table_exists(cursor):
    c.execute('''
        SELECT count(name) FROM sqlite_master WHERE type='table' AND
        name='Pokemons' ''')
    if not c.fetchone()[0]:
        return False
    return True

# First API call: retrieve detail by pokemon name
def get_poke_by_name(poke_name):
    poke_name = poke_name.lower()
    poke_name = poke_name.capitalize()
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
     if not table_exists(c):
        load_csv_to_db()
    c.execute('''SELECT * FROM Pokemons WHERE name = ?''', 
                    (poke_name,))
    return c.fetchone()

# retrieve a list of pokemons based on their types
def get_poke_by_type(type1, type2=None):
    conn = sqlite3.connect(DB_FILENAME)
    type1 = type1.lower()
    type1 = type1.capitalize()
    c = conn.cursor()
    if not table_exists(c):
        load_csv_to_db()
    if type2:
        c.execute('''
        SELECT * FROM Pokemons WHERE type1 = ? AND type2 = ?''', 
        (type1, type2))
    else:
        c.execute('''
        SELECT * FROM Pokemons WHERE type1 = ?''', (type1,))
 
    return c.fetchall()

# adding pokemon
def add_poke_to_db(name, type1, type2, sum_stats, hp, attack, 
                   special_attack,defense, special_defense,
                   speed, generation, is_legend):  
  
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    if not table_exists(c):
        load_csv_to_db()
    c.execute('''
        INSERT INTO Pokemons ('name', 'type1', 'type2', 'sum_stats',  
                          'hp', 'attack', 'special_attack', 
                          'defense', 'special_defense', 'speed', 'generation,
                          'is_legend')
                           VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', 
                           (name, type1, type2, sum_stats, hp, 
                           attack, special_attack, defense, 
                           special_defense, speed, generation, is_legend))
    conn.commit()

# updating pokemon
def update_poke(name, type1=None, type2=None, sum_stats=None,  
                hp=None, attack=None, special_attack=None, 
                defense=None, special_defense=None,
                speed=None, generation=None, is_legend=None):
     conn = sqlite3.connect(DB_FILENAME)
     c = conn.cursor()
     if not table_exists(c):
        load_csv_to_db()
     params = [type1, type2, sum_stats, hp, attack, special_attack,
              defense, special_defense, speed, generation, is_legend]
     params_names = ['type1', 'type2', 'sum_stats', 'hp', 'attack',
                    'special_attack', 'defense', 'special_defense',
                    'speed', 'generation', 'is_legend']
     for param, param_name in zip(params, params_names):
        if param:
            query = '''
                    UPDATE Pokemons SET ''' + param_name + '''    
                    = ? WHERE name = ?''' 
            c.execute(query, (param, name))
     conn.commit()

# deleting pokemon
def delete_poke(name):
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
     if not table_exists(c):
        load_csv_to_db()
     c.execute('''DELETE FROM Pokemons WHERE name = ?''',  
                       (name,))
     conn.commit()