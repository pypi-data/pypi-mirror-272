 
# Bcdr_pokemon
Bcdr_pokemon es una biblioteca de Python que te permite trabajar con datos sobre pokemones.

## Instalación
Puedes instalar la biblioteca usando `pip install Bcdr_pokemon`

## Uso
Aquí hay un ejemplo de cómo puedes usar la biblioteca para obtener información sobre 
Pokémon aleatorios:

```python
from Bcdr_pokemon import SelectPokemon

# Crear una instancia de RandomPokemon
pok = Bcdr_pokemon()
# Generar un Pokemón aleatorio
pok.generate_pokemon()
# Obtener el nombre del Pokemón generado
pok_name = pokemon.getName()
# Imprimir el nombre del Pokemón
print("Nombre del Pokemón:", pok_name)
```

## Archivo CSV de Pokémon
La biblioteca utiliza un archivo CSV llamado pokemon.csv que contiene datos 
de los Pokémones. Este archivo se incluye en el paquete y se utiliza para generar
Pokémon aleatorios. Si necesitas acceder al archivo pokemon.csv directamente, puedes 
encontrarlo en el directorio Bcdr_pokemon .

## Autor
Milton Alejandro Angel Cardenas

miltronse20@gmail.com