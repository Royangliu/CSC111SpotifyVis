"""
CSC111 Project 2
Group members: Colleen Chang, Richard Li, Roy Liu, Mina (Chieh-Yi) Wu

File Description
=============================================================================
This is the main file for running the program.
"""
import csv
import python_ta
from storage import Tree, Song


def initialize_spotify_file(file_name: str) -> Tree:
    """Intializes this tree according to the provided csv file of the top songs data.
    """
    new_tree = Tree('World', [])
    with open(file_name, encoding="utf8") as file:
        reader = csv.reader(file)
        for row in reader:
            city = row[0]
            country = row[1]
            continent = row[2]
            new_tree.insert_sequence([continent, country, city])

            # Note, this doesn't consider countries without cities (says the city name is "NAN")
            rank = 1
            for s in range(3, 8):
                song = create_song_object(row[s], rank)
                new_tree.insert_sequence([continent, country, city, song])
                rank += 1
    return new_tree


def create_song_object(string_data: str, rank: int) -> Song:
    """Creates a Song object from the given string data.

    The string should be in the following format:
            "<title>, <main_artist>, <streams>"
    """
    split_str = string_data.split(', ')
    title, artist, streams = split_str[0].lower(), split_str[1].lower(), int(split_str[2].strip())
    return Song(title, artist, streams, rank)


def get_all_countries(file_name: str) -> list[str]:
    """Returns a list of all countries in the given file.
    """
    countries_list = []
    with open(file_name, encoding="utf8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] not in countries_list:
                countries_list.append(row[1])
    return countries_list


def get_all_continents(file_name: str) -> list[str]:
    """Returns a list of all continents in the given file.
    """
    continents = []
    with open(file_name, encoding="utf8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] not in continents:
                continents.append(row[1])
    return continents


def get_all_cities(file_name: str) -> list[str]:
    """Returns a list of all cities in the given file.
    """
    cities = []
    with open(file_name, encoding="utf8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] not in cities:
                cities.append(row[1])
    return cities


# def get_personality_test(tree: Tree) -> None:
#     """
# 
#     """


if __name__ == "__main__":
    spotify_tree = initialize_spotify_file("main_data.csv")  # Make sure this is consistent with file names
    stop = False
    print("Welcome to the Spotify visualization program!")

    while stop:
        print("This is the main menu. Please select an option:\n")
        print("1. Get the top n songs for a continent/country/city\n2. Find the most common artists between two countries\n3. Find the most common songs between two countries\n4. Find the most common artist")

        print(spotify_tree.top_n(5, 'Canada'))
        # print(spotify_tree.most_common_song_country("Costa Rica"))






    
    songs = ['lovin on me', 'stick season', 'greedy', 'i remember everything', 'cruel summer']
    a = spotify_tree.region_personality(5, songs, 'city', True)
    print(a)
    b = spotify_tree.recommend_songs((5, 20), songs, 'city', True)
    for ah in b:
        print(ah.title)
    # visualization code
    import visualization

    visualization.visualize_world_song_data(spotify_tree)






    
    python_ta.check_all(config={
        # the names (strs) of imported modules
        'extra-imports': ['storage', 'csv'],

        # the names (strs) of functions that call print/open/input
        'allowed-io': ['get_all_cities', 'get_all_continents', 'get_all_countries', 'initialize_spotify_file'],
        'max-line-length': 120
    })
