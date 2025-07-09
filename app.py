# app.py
# Para executar: salve este código como app.py e no terminal digite: streamlit run app.py

import streamlit as st
import requests
import random
import pandas as pd
import time
import json
import os
from regions_data import REGIONS # Importa os dados do arquivo separado

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Otimizador de Times Pokémon",
    page_icon="🧬",
    layout="wide"
)

# --- CONSTANTES E DADOS GLOBAIS ---
DATA_FILE = 'pokemon_database.json'

# --- FUNÇÕES DE GERENCIAMENTO DO BANCO DE DADOS LOCAL ---

def setup_database():
    """
    Busca todos os dados necessários da PokeAPI e os salva em um arquivo JSON local.
    Isso é executado apenas uma vez para evitar múltiplas chamadas de API.
    """
    database = {'pokemons': {}, 'types': {}}
    
    with st.spinner("Criando banco de dados local... Isso pode levar alguns minutos, mas só será feito uma vez."):
        # 1. Obter todos os nomes de Pokémon das gerações relevantes
        all_pokemon_names = set()
        progress_text = "Buscando gerações... 0/{}"
        gen_progress = st.text(progress_text.format(len(REGIONS)))
        
        for i, region in enumerate(REGIONS.values()):
            try:
                res = requests.get(f"https://pokeapi.co/api/v2/generation/{region['generation_id']}")
                res.raise_for_status()
                data = res.json()
                for p in data['pokemon_species']:
                    all_pokemon_names.add(p['name'])
                gen_progress.text(progress_text.format(i + 1))
            except requests.RequestException as e:
                st.error(f"Falha ao buscar a Geração {region['generation_id']}: {e}")
                continue
        
        # 2. Obter dados para cada Pokémon
        total_names = len(all_pokemon_names)
        st.write(f"Buscando dados de {total_names} Pokémon...")
        poke_progress = st.progress(0)
        for i, name in enumerate(list(all_pokemon_names)):
            try:
                # Usamos uma aproximação para a geração do Pokémon, pode não ser 100% precisa para todos
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

        # 3. Obter dados de todos os tipos
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

        # 4. Salvar o arquivo JSON
        with open(DATA_FILE, 'w') as f:
            json.dump(database, f, indent=4)
    
    st.success(f"Banco de dados local '{DATA_FILE}' criado com sucesso!")
    return database

def load_database():
    """Carrega o banco de dados do arquivo JSON local."""
    if not os.path.exists(DATA_FILE):
        return setup_database()
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# --- LÓGICA DO ALGORITMO GENÉTICO ---

def calculate_fitness(team, gym_leaders, db):
    """Calcula a aptidão usando o banco de dados local."""
    total_score = 0
    
    for leader, leader_team in gym_leaders.items():
        for leader_pokemon_name in leader_team:
            leader_pokemon = db['pokemons'].get(leader_pokemon_name)
            if not leader_pokemon:
                continue
            
            leader_types = leader_pokemon['types']
            best_matchup_score = -10

            for team_pokemon_name in team:
                team_pokemon = db['pokemons'].get(team_pokemon_name)
                if not team_pokemon:
                    continue
                
                team_types = team_pokemon['types']
                current_matchup_score = 0
                
                for team_type in team_types:
                    relations = db['types'].get(team_type)
                    if relations:
                        for leader_type in leader_types:
                            if any(t['name'] == leader_type for t in relations['double_damage_to']):
                                current_matchup_score += 2
                            elif any(t['name'] == leader_type for t in relations['half_damage_to']):
                                current_matchup_score -= 1
                            elif any(t['name'] == leader_type for t in relations['no_damage_to']):
                                current_matchup_score -= 2
                
                if current_matchup_score > best_matchup_score:
                    best_matchup_score = current_matchup_score
            
            total_score += best_matchup_score
    return total_score

def create_individual(pokemon_pool):
    return random.sample(pokemon_pool, 6)

def crossover(parent1, parent2):
    point = random.randint(1, 5)
    child = parent1[:point]
    remaining_pokemons = [p for p in parent2 if p not in child]
    child.extend(remaining_pokemons)
    return child[:6]

def mutate(individual, pokemon_pool, mutation_rate=0.1):
    if random.random() < mutation_rate:
        gene_to_mutate = random.randint(0, 5)
        new_pokemon = random.choice(pokemon_pool)
        while new_pokemon in individual:
            new_pokemon = random.choice(pokemon_pool)
        individual[gene_to_mutate] = new_pokemon
    return individual

# --- INTERFACE GRÁFICA (STREAMLIT) ---

st.title("🧬 Otimizador de Times Pokémon com Algoritmo Genético")
st.markdown("Este app usa um banco de dados local (`pokemon_database.json`) para acelerar os cálculos. Se o arquivo não existir, ele será criado na primeira execução.")

# Inicializa o estado da sessão
if 'running' not in st.session_state:
    st.session_state.running = False
if 'best_team' not in st.session_state:
    st.session_state.best_team = None
if 'best_fitness' not in st.session_state:
    st.session_state.best_fitness = -float('inf')
if 'fitness_history' not in st.session_state:
    st.session_state.fitness_history = []
if 'generation_count' not in st.session_state:
    st.session_state.generation_count = 0


with st.sidebar:
    st.header("⚙️ Configurações")
    region_name = st.selectbox("Escolha a Região:", list(REGIONS.keys()), disabled=st.session_state.running)
    
    st.subheader("Parâmetros do Algoritmo Genético")
    population_size = st.slider("Tamanho da População", 50, 500, 100, 10, disabled=st.session_state.running)
    mutation_rate = st.slider("Taxa de Mutação", 0.01, 0.5, 0.1, 0.01, disabled=st.session_state.running)
    elitism_count = st.slider("Elitismo", 1, 10, 2, 1, disabled=st.session_state.running)

    col1, col2 = st.columns(2)
    with col1:
        if not st.session_state.running:
            if st.button("🚀 Iniciar", use_container_width=True):
                st.session_state.running = True
                st.session_state.best_team = None
                st.session_state.best_fitness = -float('inf')
                st.session_state.fitness_history = []
                st.session_state.generation_count = 0
                st.rerun()
    with col2:
        if st.session_state.running:
            if st.button("⏹️ Parar", type="primary", use_container_width=True):
                st.session_state.running = False
                st.rerun()
    
    st.divider()
    if st.button("Forçar Atualização da Base de Dados"):
        setup_database()

st.header("🏆 Resultados")
info_placeholder = st.empty()
team_placeholder = st.empty()
chart_placeholder = st.empty()


if not st.session_state.running and not st.session_state.best_team:
     st.info("Ajuste os parâmetros na barra lateral e clique em 'Iniciar' para começar.")

if st.session_state.running:
    db = load_database()
    region_data = REGIONS[region_name]
    gym_leaders = region_data['gym_leaders']
    
    # Filtra o pool de pokemons para a geração selecionada
    target_gen_id = region_data['generation_id']
    pokemon_pool_names = [
        name for name, data in db['pokemons'].items()
        if data.get('generation_id', 99) <= target_gen_id
    ]
    if len(pokemon_pool_names) < 6:
        st.error(f"Não há Pokémon suficientes ({len(pokemon_pool_names)}) na base de dados para a Geração {target_gen_id}. Tente atualizar a base de dados.")
        st.session_state.running = False
        st.stop()

    # Inicializa a população se for a primeira geração
    if st.session_state.generation_count == 0:
        with st.spinner("Criando população inicial..."):
            st.session_state.population = [create_individual(pokemon_pool_names) for _ in range(population_size)]

    # Loop de gerações
    while st.session_state.running:
        st.session_state.generation_count += 1
        
        fitness_scores = [calculate_fitness(ind, gym_leaders, db) for ind in st.session_state.population]
        best_gen_fitness = max(fitness_scores)

        if best_gen_fitness > st.session_state.best_fitness:
            st.session_state.best_fitness = best_gen_fitness
            best_gen_idx = fitness_scores.index(best_gen_fitness)
            st.session_state.best_team = st.session_state.population[best_gen_idx]
        
        st.session_state.fitness_history.append({
            'Geração': st.session_state.generation_count, 
            'Melhor Aptidão': st.session_state.best_fitness, # Plota o melhor geral
            'Média da Aptidão': sum(fitness_scores) / len(fitness_scores)
        })

        # Evolução
        new_population = []
        sorted_population = [x for _, x in sorted(zip(fitness_scores, st.session_state.population), key=lambda pair: pair[0], reverse=True)]
        new_population.extend(sorted_population[:elitism_count])

        while len(new_population) < population_size:
            parents = random.choices(sorted_population, k=2) # Seleção simples por ranking
            child = crossover(parents[0], parents[1])
            child = mutate(child, pokemon_pool_names, mutation_rate)
            new_population.append(child)
        
        st.session_state.population = new_population

        # Atualiza UI
        info_placeholder.metric(
            label=f"Melhor Aptidão (Geração {st.session_state.generation_count})",
            value=f"{st.session_state.best_fitness:.2f}"
        )

        with team_placeholder.container():
            st.subheader(f"Melhor Time Encontrado (Aptidão: {st.session_state.best_fitness:.2f})")
            cols = st.columns(6)
            if st.session_state.best_team:
                for i, pokemon_name in enumerate(st.session_state.best_team):
                    with cols[i]:
                        sprite_url = db['pokemons'].get(pokemon_name, {}).get('sprite')
                        if sprite_url:
                            st.image(sprite_url, caption=pokemon_name.capitalize(), use_container_width=True)
                        else:
                            st.write(pokemon_name.capitalize())
        
        chart_df = pd.DataFrame(st.session_state.fitness_history).rename(columns={'Geração':'index'}).set_index('index')
        chart_placeholder.line_chart(chart_df)
        
        # Pausa para o Streamlit atualizar a UI
        time.sleep(0.1)

# Exibe o resultado final se a otimização foi parada
if not st.session_state.running and st.session_state.best_team:
    st.success(f"Otimização parada na geração {st.session_state.generation_count}. Este foi o melhor time encontrado.")
    info_placeholder.metric(
            label=f"Melhor Aptidão Final (Geração {st.session_state.generation_count})",
            value=f"{st.session_state.best_fitness:.2f}"
    )
    with team_placeholder.container():
        st.subheader(f"Melhor Time Encontrado (Aptidão: {st.session_state.best_fitness:.2f})")
        cols = st.columns(6)
        db = load_database()
        for i, pokemon_name in enumerate(st.session_state.best_team):
            with cols[i]:
                sprite_url = db['pokemons'].get(pokemon_name, {}).get('sprite')
                if sprite_url:
                    st.image(sprite_url, caption=pokemon_name.capitalize(), use_container_width=True)
                else:
                    st.write(pokemon_name.capitalize())
    chart_df = pd.DataFrame(st.session_state.fitness_history).rename(columns={'Geração':'index'}).set_index('index')
    chart_placeholder.line_chart(chart_df)
