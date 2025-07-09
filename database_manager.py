# database_manager.py
import streamlit as st
import requests
import json
import os
from regions_data import REGIONS

DATA_FILE = 'pokemon_database.json'

def setup_database():
    """
    Busca todos os dados necessários da PokeAPI e os salva em um arquivo JSON local.
    """
    database = {'pokemons': {}, 'types': {}}
    
    with st.spinner("Criando banco de dados local... Isso pode levar alguns minutos, mas só será feito uma vez."):
        all_pokemon_names = set()
        progress_text = "Buscando gerações... {0}/{1}"
        gen_progress = st.text(progress_text.format(0, len(REGIONS)))
        
        for i, region in enumerate(REGIONS.values()):
            try:
                res = requests.get(f"https://pokeapi.co/api/v2/generation/{region['generation_id']}")
                res.raise_for_status()
                data = res.json()
                for p in data['pokemon_species']:
                    all_pokemon_names.add(p['name'])
                gen_progress.text(progress_text.format(i + 1, len(REGIONS)))
            except requests.RequestException as e:
                st.error(f"Falha ao buscar a Geração {region['generation_id']}: {e}")
                continue
        
        total_names = len(all_pokemon_names)
        st.write(f"Buscando dados de {total_names} Pokémon...")
        poke_progress = st.progress(0)
        for i, name in enumerate(list(all_pokemon_names)):
            try:
                res_species = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{name}")
                res_species.raise_for_status()
                species_data = res_species.json()
                gen_id_str = species_data['generation']['url'].split('/')[-2]

                res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
                res.raise_for_status()
                p_data = res.json()
                database['pokemons'][name] = {
                    'types': [t['type']['name'] for t in p_data['types']],
                    'sprite': p_data['sprites']['front_default'],
                    'generation_id': int(gen_id_str)
                }
            except requests.RequestException:
                st.warning(f"Não foi possível buscar dados para: {name}")
            poke_progress.progress((i + 1) / total_names)

        st.write("Buscando dados de efetividade de tipos...")
        try:
            res = requests.get("https://pokeapi.co/api/v2/type")
            res.raise_for_status()
            type_results = res.json()['results']
            for t in type_results:
                type_name = t['name']
                res_type = requests.get(t['url'])
                res_type.raise_for_status()
                database['types'][type_name] = res_type.json()['damage_relations']
        except requests.RequestException as e:
            st.error(f"Falha ao buscar dados de tipos: {e}")

        with open(DATA_FILE, 'w') as f:
            json.dump(database, f, indent=4)
    
    st.success(f"Banco de dados local '{DATA_FILE}' criado com sucesso!")
    return database

def load_database():
    """Carrega o banco de dados do arquivo JSON local."""
    if not os.path.exists(DATA_FILE):
        st.info(f"Arquivo '{DATA_FILE}' não encontrado. Criando um novo banco de dados.")
        return setup_database()
    with open(DATA_FILE, 'r') as f:
        return json.load(f)
