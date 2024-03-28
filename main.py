import csv
from Storage import Tree, Song


def initialize_spotify_file(file_name: str) -> Tree:
    """Intializes this tree according to the provided csv file of the top songs data.
    """
    new_tree = Tree('World', [])

    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            city = row[0]
            country = row[1]
            continent = row[2]
            new_tree.insert_sequence(['World', continent, country, city])

            # Note, this doesn't consider countries without cities (says the city name is "NAN")
            for s in range(3, 8):
                song = create_song_object(row[s])
                new_tree.insert_sequence(['World', continent, country, city, song])

    return new_tree


def create_song_object(string_data: str) -> Song:
    """Creates a Song object from the given string data.

    The string should be in the following format:
        "<title>, <main_artist>, <streams>"
    """
    split_str = string_data.split(', ')
    title, artist, streams = split_str[0].lower(), split_str[1].lower(), int(split_str[2])
    return Song(title, artist, streams)


if __name__ == "__main__":
    spotify_tree = initialize_spotify_file("Test_set_main.csv")  # Make sure this is consistent with file names
    print(spotify_tree.top_n(5, 'Canada'))
    # print(spotify_tree.most_common_song_country("Costa Rica"))
