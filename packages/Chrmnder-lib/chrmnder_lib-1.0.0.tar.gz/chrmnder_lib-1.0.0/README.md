# charzr_lib
charzr_lib es una biblioteca de Python que te permite trabajar con datos de Pokémon.
## Instalación
Puedes instalar la biblioteca usando `pip install charzr_lib==1.0.0`
## Uso
Aquí hay un ejemplo de cómo puedes usar la biblioteca para obtener información sobre Pokémon aleatorios:

```python
from Chrmnder_Lib import RandomPokemon

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
necesitas acceder al archivo pokemon.csv directamente, puedes encontrarlo en el directorio charzr_lib.
## Autor
Missael Angel Cardenas