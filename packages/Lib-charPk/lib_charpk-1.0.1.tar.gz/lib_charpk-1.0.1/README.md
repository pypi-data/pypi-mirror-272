# Lib_charPk
Pokemon_Library es una biblioteca de Python que te permite trabajar con datos de Pokémon.
## Instalación
Puedes instalar la biblioteca usando `pip install Lib_charPk`
## Uso
Aquí hay un ejemplo de cómo puedes usar la biblioteca para obtener información sobre Pokémon aleatorios:
```python
from Lib_charPk import RandomPokemon
# Crear una instancia de RandomPokemon
pokemon = RandomPokemon()
# Generar un Pokemón aleatorio
pokemon.generate_random()
# Obtener el nombre del Pokemón generado
pokemon_name = pokemon.getName()
# Imprimir el nombre del Pokemón
print("Nombre del Pokemón:", pokemon_name)
```
## Archivo CSV de Pokémon
La biblioteca utiliza un archivo CSV llamado pokemon.csv que contiene datos de Pokémon. Este archivo se incluye en el paquete y se utiliza para generar Pokémon aleatorios. Si
necesitas acceder al archivo pokemon.csv directamente, puedes encontrarlo en el directorio Lib_charPk.
## Autor
Missael Angel Cardenas 