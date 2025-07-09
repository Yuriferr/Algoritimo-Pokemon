# genetic_algorithm.py
import random

def calculate_fitness(team, gym_leaders, db):
    """Calcula a aptidão de um time usando o banco de dados local."""
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
    """Cria um time com 6 Pokémon únicos."""
    return random.sample(pokemon_pool, 6)

def crossover(parent1, parent2):
    """Realiza o cruzamento entre dois pais para gerar um filho."""
    point = random.randint(1, 5)
    child = parent1[:point]
    remaining_pokemons = [p for p in parent2 if p not in child]
    child.extend(remaining_pokemons)
    return child[:6]

def mutate(individual, pokemon_pool, mutation_rate=0.1):
    """Aplica uma mutação em um indivíduo."""
    if random.random() < mutation_rate:
        gene_to_mutate = random.randint(0, 5)
        new_pokemon = random.choice(pokemon_pool)
        while new_pokemon in individual:
            new_pokemon = random.choice(pokemon_pool)
        individual[gene_to_mutate] = new_pokemon
    return individual

def evolve_population(population, gym_leaders, db, elitism_count, mutation_rate, pokemon_pool):
    """Executa uma geração completa: avaliação, seleção, cruzamento e mutação."""
    # Avaliação
    fitness_scores = [calculate_fitness(ind, gym_leaders, db) for ind in population]

    # Seleção e Elitismo
    new_population = []
    sorted_population = [x for _, x in sorted(zip(fitness_scores, population), key=lambda pair: pair[0], reverse=True)]
    new_population.extend(sorted_population[:elitism_count])

    # Cruzamento e Mutação
    while len(new_population) < len(population):
        parents = random.choices(sorted_population, k=2) # Seleção simples por ranking
        child = crossover(parents[0], parents[1])
        child = mutate(child, pokemon_pool, mutation_rate)
        new_population.append(child)
    
    best_fitness_current_gen = max(fitness_scores)
    
    return new_population, best_fitness_current_gen, sorted_population[0]
