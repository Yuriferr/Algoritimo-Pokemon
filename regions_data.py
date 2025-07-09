# regions_data.py
# Este arquivo contém os dados dos líderes de ginásio para cada região.

REGIONS = {
    "Kanto (Gen 1)": {
        "generation_id": 1,
        "gym_leaders": {
            'Brock': ['geodude', 'onix'],
            'Misty': ['staryu', 'starmie'],
            'Lt. Surge': ['voltorb', 'pikachu', 'raichu'],
            'Erika': ['victreebel', 'tangela', 'vileplume'],
            'Koga': ['koffing', 'muk', 'koffing', 'weezing'],
            'Sabrina': ['kadabra', 'mr-mime', 'venomoth', 'alakazam'],
            'Blaine': ['growlithe', 'ponyta', 'rapidash', 'arcanine'],
            'Giovanni': ['rhyhorn', 'dugtrio', 'nidoqueen', 'nidoking', 'rhydon']
        }
    },
    "Johto (Gen 2)": {
        "generation_id": 2,
        "gym_leaders": {
            'Falkner': ['pidgey', 'pidgeotto'],
            'Bugsy': ['metapod', 'kakuna', 'scyther'],
            'Whitney': ['clefairy', 'miltank'],
            'Morty': ['gastly', 'haunter', 'gengar', 'haunter'],
            'Chuck': ['primeape', 'poliwrath'],
            'Jasmine': ['magnemite', 'magnemite', 'steelix'],
            'Pryce': ['seel', 'dewgong', 'piloswine'],
            'Clair': ['dragonair', 'dragonair', 'dragonair', 'kingdra']
        }
    },
    "Hoenn (Gen 3)": {
        "generation_id": 3,
        "gym_leaders": {
            'Roxanne': ['geodude', 'nosepass'],
            'Brawly': ['machop', 'makuhita'],
            'Wattson': ['magnemite', 'voltorb', 'magneton'],
            'Flannery': ['slugma', 'numel', 'torkoal'],
            'Norman': ['spinda', 'vigoroth', 'slaking'],
            'Winona': ['swablu', 'tropicus', 'pelipper', 'skarmory', 'altaria'],
            'Tate & Liza': ['solrock', 'lunatone'],
            'Wallace': ['luvdisc', 'whiscash', 'sealeo', 'seaking', 'milotic']
        }
    },
    "Sinnoh (Gen 4)": {
        "generation_id": 4,
        "gym_leaders": {
            'Roark': ['geodude', 'onix', 'cranidos'],
            'Gardenia': ['turtwig', 'cherubi', 'roserade'],
            'Maylene': ['meditite', 'machoke', 'lucario'],
            'Crasher Wake': ['gyarados', 'quagsire', 'floatzel'],
            'Fantina': ['duskull', 'haunter', 'mismagius'],
            'Byron': ['bronzor', 'steelix', 'bastiodon'],
            'Candice': ['snover', 'sneasel', 'medicham', 'abomasnow'],
            'Volkner': ['raichu', 'ambipom', 'octillery', 'luxray']
        }
    },
    "Unova (Gen 5)": {
        "generation_id": 5,
        "gym_leaders": {
            'Cilan/Chili/Cress': ['pansage', 'pansear', 'panpour'], # Simplified
            'Lenora': ['herdier', 'watchog'],
            'Burgh': ['dwebble', 'whirlipede', 'leavanny'],
            'Elesa': ['emolga', 'emolga', 'zebstrika'],
            'Clay': ['krokorok', 'palpitoad', 'excadrill'],
            'Skyla': ['swoobat', 'unfezant', 'swanna'],
            'Brycen': ['vanillish', 'cryogonal', 'beartic'],
            'Drayden': ['fraxure', 'druddigon', 'haxorus']
        }
    },
    "Kalos (Gen 6)": {
        "generation_id": 6,
        "gym_leaders": {
            'Viola': ['surskit', 'vivillon'],
            'Grant': ['amaura', 'tyrunt'],
            'Korrina': ['mienfoo', 'machoke', 'hawlucha'],
            'Ramos': ['jumpluff', 'gogoat', 'weepinbell'],
            'Clemont': ['emolga', 'magneton', 'heliolisk'],
            'Valerie': ['mawile', 'mr-mime', 'sylveon'],
            'Olympia': ['sigilyph', 'slowking', 'meowstic'],
            'Wulfric': ['abomasnow', 'cryogonal', 'avalugg']
        }
    },
    "Alola (Gen 7 - Trials)": {
        "generation_id": 7,
        "gym_leaders": { # Simplified as trials, using totem Pokémon
            'Ilima': ['gumshoos-totem', 'raticate-totem-alola'],
            'Lana': ['wishiwashi-totem'],
            'Kiawe': ['marowak-totem'],
            'Mallow': ['lurantis-totem'],
            'Sophocles': ['vikavolt-totem'],
            'Acerola': ['mimikyu-totem'],
            'Mina': ['ribombee-totem']
        }
    },
    "Galar (Gen 8)": {
        "generation_id": 8,
        "gym_leaders": {
            'Milo': ['gossifleur', 'flapple', 'appletun'],
            'Nessa': ['goldeen', 'arrokuda', 'drednaw'],
            'Kabu': ['ninetales', 'arcanine', 'centiskorch'],
            'Bea': ['hitmontop', 'pangoro', 'sirfetchd', 'machamp'],
            'Allister': ['yamask-galar', 'mimikyu', 'cursola', 'gengar'],
            'Opal': ['weezing-galar', 'mawile', 'togekiss', 'alcremie'],
            'Gordie': ['shuckle', 'stonjourner', 'tyranitar', 'coalossal'],
            'Melony': ['frosmoth', 'darmanitan-galar', 'eiscue', 'lapras'],
            'Piers': ['scrafty', 'malamar', 'skuntank', 'obstagoon'],
            'Raihan': ['torkoal', 'turtonator', 'flygon', 'duraludon']
        }
    },
    "Paldea (Gen 9)": {
        "generation_id": 9,
        "gym_leaders": {
            'Katy': ['naclstack', 'tarountula', 'teddiursa'],
            'Brassius': ['petilil', 'smoliv', 'sudowoodo'],
            'Iono': ['wattrel', 'bellibolt', 'luxio', 'mismagius'],
            'Kofu': ['veluza', 'wugtrio', 'crabominable'],
            'Larry': ['komala', 'dudunsparce', 'staraptor'],
            'Ryme': ['banette', 'mimikyu', 'houndstone', 'toxtricity'],
            'Tulip': ['farigiraf', 'gardevoir', 'espathra', 'florges'],
            'Grusha': ['frosmoth', 'beartic', 'cetitan', 'altaria']
        }
    }
}
