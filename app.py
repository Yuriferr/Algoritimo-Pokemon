# app.py
import streamlit as st
import pandas as pd
import time

# Importando os módulos separados
from regions_data import REGIONS
from database_manager import load_database, setup_database
from genetic_algorithm import create_individual, evolve_population, calculate_fitness

def initialize_session_state():
    """Inicializa as variáveis de estado da sessão se não existirem."""
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

def render_sidebar():
    """Renderiza a barra lateral com todas as configurações."""
    with st.sidebar:
        st.header("⚙️ Configurações")
        region_name = st.selectbox("Escolha a Região:", list(REGIONS.keys()), disabled=st.session_state.running)
        
        st.subheader("Parâmetros do Algoritmo Genético")
        pop_size = st.slider("Tamanho da População", 50, 500, 100, 10, disabled=st.session_state.running)
        mutation_rate = st.slider("Taxa de Mutação", 0.01, 0.5, 0.1, 0.01, disabled=st.session_state.running)
        elitism_count = st.slider("Elitismo", 1, 10, 2, 1, disabled=st.session_state.running)

        col1, col2 = st.columns(2)
        with col1:
            if not st.session_state.running and st.button("🚀 Iniciar", use_container_width=True):
                st.session_state.running = True
                st.session_state.best_team = None
                st.session_state.best_fitness = -float('inf')
                st.session_state.fitness_history = []
                st.session_state.generation_count = 0
                st.rerun()
        with col2:
            if st.session_state.running and st.button("⏹️ Parar", type="primary", use_container_width=True):
                st.session_state.running = False
                st.rerun()
        
        st.divider()
        if st.button("Forçar Atualização da Base de Dados"):
            setup_database()
            
    return region_name, pop_size, mutation_rate, elitism_count

def render_results_placeholders():
    """Cria os placeholders para os resultados dinâmicos."""
    st.header("🏆 Resultados")
    info_placeholder = st.empty()
    team_placeholder = st.empty()
    chart_placeholder = st.empty()
    return info_placeholder, team_placeholder, chart_placeholder

def update_ui(info_ph, team_ph, chart_ph, db):
    """Atualiza a interface do usuário com os dados mais recentes da sessão."""
    info_ph.metric(
        label=f"Melhor Aptidão (Geração {st.session_state.generation_count})",
        value=f"{st.session_state.best_fitness:.2f}"
    )
    with team_ph.container():
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
    chart_ph.line_chart(chart_df)

def main():
    """Função principal que executa a aplicação Streamlit."""
    st.title("� Otimizador de Times Pokémon com Algoritmo Genético")
    
    initialize_session_state()
    region_name, pop_size, mutation_rate, elitism_count = render_sidebar()
    info_ph, team_ph, chart_ph = render_results_placeholders()

    if not st.session_state.running and not st.session_state.best_team:
        st.info("Ajuste os parâmetros na barra lateral e clique em 'Iniciar' para começar.")
    
    db = load_database()

    if st.session_state.running:
        region_data = REGIONS[region_name]
        gym_leaders = region_data['gym_leaders']
        target_gen_id = region_data['generation_id']
        
        pokemon_pool = [name for name, data in db['pokemons'].items() if data.get('generation_id', 99) <= target_gen_id]
        if len(pokemon_pool) < 6:
            st.error(f"Não há Pokémon suficientes na base de dados para a Geração {target_gen_id}.")
            st.session_state.running = False
            st.stop()

        if st.session_state.generation_count == 0:
            st.session_state.population = [create_individual(pokemon_pool) for _ in range(pop_size)]

        while st.session_state.running:
            st.session_state.generation_count += 1
            
            new_pop, best_gen_fitness, best_gen_team = evolve_population(
                st.session_state.population, gym_leaders, db, elitism_count, mutation_rate, pokemon_pool
            )
            st.session_state.population = new_pop

            if best_gen_fitness > st.session_state.best_fitness:
                st.session_state.best_fitness = best_gen_fitness
                st.session_state.best_team = best_gen_team
            
            # Recalcula a média da aptidão da nova população
            avg_fitness = sum(calculate_fitness(ind, gym_leaders, db) for ind in new_pop) / len(new_pop)
            st.session_state.fitness_history.append({
                'Geração': st.session_state.generation_count, 
                'Melhor Aptidão': st.session_state.best_fitness,
                'Média da Aptidão': avg_fitness
            })

            update_ui(info_ph, team_ph, chart_ph, db)
            time.sleep(0.1)

    if not st.session_state.running and st.session_state.best_team:
        st.success(f"Otimização parada na geração {st.session_state.generation_count}. Este foi o melhor time encontrado.")
        update_ui(info_ph, team_ph, chart_ph, db)

if __name__ == "__main__":
    main()