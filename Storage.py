from __future__ import annotations
import csv
from typing import Any, Optional, Union


class Tree:
    """A recursive tree data structure.

          Note the relationship between this class and RecursiveList; the only major
          difference is that _rest has been replaced by _subtrees to handle multiple
          recursive sub-parts.

          Representation Invariants:
                  - self._root is not None or self._subtrees == []
                  - all(not subtree.is_empty() for subtree in self._subtrees)
          """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this attribute
    #       may be empty when self._root is not None, which represents a tree consisting
    #       of just one item.
    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """
        Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
                - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """
        Return whether this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            size = 1  # count the root
            for subtree in self._subtrees:
                size += subtree.__len__()  # could also write len(subtree)
            return size

    def __contains__(self, item: Any) -> bool:
        """
        Return whether the given is in this tree.

        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> t.__contains__(1)
        True
        >>> t.__contains__(5)
        True
        >>> t.__contains__(4)
        False
        """
        if self.is_empty():
            return False
        elif self._root == item:
            return True
        else:
            for subtree in self._subtrees:
                if subtree.__contains__(item):
                    return True
            return False

    def insert_sequence(self, items: list) -> None:
        """
        function from exercise 2

        The inserted items form a chain of descendants, where:
        - items[0] is a child of this tree's root
        - items[1] is a child of items[0]
        - items[2] is a child of items[1]
        - etc.

        Preconditions:
                - not self.is_empty()
        """
        if items:
            in_subtrees = False
            for subtree in self._subtrees:
                if subtree._root == items[0] and not in_subtrees:
                    subtree.insert_sequence(items[1:])
                    in_subtrees = True

            if not in_subtrees:
                new_tree = Tree(items[0], [])
                new_tree.insert_sequence(items[1:])
                self._subtrees.append(new_tree)

    # Tree functions
    def top_n(self, n: int, target: str) -> list[tuple]:
        """
        This function takes in the tree itself, an int representing the number of top songs to return,
        and a target representing whether you want to find top songs from the world, continent, country, or city.
        Returns a list of tuple with the top n songs, their artists, and stream. Returns [] if the target is not found.

        Representation Invariants:
            - n >= 1
        """
        if self._root == target:
            return self._search_songs(n, {}, {}, {})
        elif self._subtrees == []:
            return []
        else:
            for subtree in self._subtrees:
                top = subtree.top_n(n, target)
                if top != []:
                    return top

            return []

    def _search_songs(self, n: int, songs: dict, s_and_artist: dict,
                      s_and_stream: dict) -> list[tuple]:
        """
        This is a helper function for top_n, it returns the name, artist,
        and streams of the top n songs in a list of tuples.
        """

        if isinstance(self._root, Song):
            if self._root.title in songs:
                songs[self._root.title] += 1
            else:
                songs[self._root.title] = 1

            s_and_artist[self._root.title] = self._root.artist
            s_and_stream[self._root.title] = self._root.streams
            return []

        else:
            for subtree in self._subtrees:
                subtree._search_songs(n, songs, s_and_artist, s_and_stream)

            songs = dict(sorted(songs.items(), key=lambda x: x[1], reverse=True))
            songs = list(songs)
            lst = []
            for i in range(n):
                if i >= len(songs):
                    return lst

                lst += [(songs[i], s_and_artist[songs[i]], s_and_stream[songs[i]])]

            return lst

    def common_artist(self, country1: str, country2: str) -> list[str]:
        """

              This function takes in two country names as inputs and compares the artists of the top songs from each country and outputs a list of the most commonly occurring artists between the two countries in descending order.

              """
        top_songs_1 = self.top_n(100, country1)
        top_songs_2 = self.top_n(100, country2)

        top_songs1_dict = {}
        for song1 in top_songs_1:
            if song1[1] in top_songs1_dict:
                top_songs1_dict[song1[1]] += 1
            else:
                top_songs1_dict[song1[1]] = 1

        top_songs2_dict = {}
        for song2 in top_songs_2:
            if song2[1] in top_songs2_dict:
                top_songs2_dict[song2[1]] += 1
            else:
                top_songs2_dict[song2[1]] = 1

        common_artist = {}
        for artist in top_songs1_dict:
            if artist in top_songs2_dict:
                if top_songs1_dict[artist] <= top_songs2_dict[artist]:
                    common_artist[artist] = top_songs1_dict[artist]

        common_artist = dict(
            sorted(common_artist.items(), key=lambda x: x[1], reverse=True))
        common_artist = list(common_artist)
        return common_artist

    def common_song(self, country1: str, country2: str) -> list[str]:
        """
        This function takes in two country names as inputs and compares the top songs from both and outputs a list of
        the most commonly occurring songs between them in descending order.
        """
        top_songs_1 = self.top_n(100, country1)
        top_songs_2 = self.top_n(100, country2)

        top_songs1_dict = {}
        for song1 in top_songs_1:
            if song1[0] in top_songs1_dict:
                top_songs1_dict[song1[0]] += 1
            else:
                top_songs1_dict[song1[0]] = 1

        top_songs2_dict = {}
        for song2 in top_songs_2:
            if song2[0] in top_songs2_dict:
                top_songs2_dict[song2[0]] += 1
            else:
                top_songs2_dict[song2[0]] = 1

        common_song = {}
        for song in top_songs1_dict:
            if song in top_songs2_dict:
                if top_songs1_dict[song] <= top_songs2_dict[song]:
                    common_song[song] = top_songs1_dict[song]

        common_song = dict(
            sorted(common_song.items(), key=lambda x: x[1], reverse=True))
        common_song = list(common_song)
        return common_song

    def most_common_artist_country(self, country1: str, data: str) -> list[str]:
        """
        This function takes in a country name and data file as an input and compares the artists of the top songs from 
        this country to all other countries in data and outputs a list of the most common country
        """

        countries = set()
        with open(data, 'r') as file:
            info = csv.reader(file)
            for line in info:
                if line[1] not in countries and line[1] != country1:
                    countries.add(line[1])

        country_top_artist = self.common_song_artist_helper(country1, 'artist')
        most_similar = {}

        for country in countries:
            temp_country_list = self.common_song_artist_helper(country, 'artist')
            for artist in temp_country_list:
                if artist in country_top_artist:
                    if country in most_similar:
                        most_similar[country] += 1
                    else:
                        most_similar[country] = 1

        most_similar = dict(
            sorted(most_similar.items(), key=lambda x: x[1], reverse=True))
        most_similar = list(most_similar)

        return most_similar[:1]

    def most_common_song_country(self, country1: str, data: str) -> list[str]:
        """
        This function takes in a country name and data file as an input and compares the top songs from 
        this country to the top songs in all other countries in data and outputs a list of the most common country
        """

        countries = set()
        with open(data, 'r') as file:
            info = csv.reader(file)
            for line in info:
                if line[1] not in countries and line[1] != country1:
                    countries.add(line[1])

        country_top_songs = self.common_song_artist_helper(country1, 'song')
        most_similar = {}

        for country in countries:
            temp_country_list = self.common_song_artist_helper(country, 'song')
            for song in temp_country_list:
                if song in country_top_songs:
                    if country in most_similar:
                        most_similar[country] += 1
                    else:
                        most_similar[country] = 1

        most_similar = dict(
            sorted(most_similar.items(), key=lambda x: x[1], reverse=True))
        most_similar = list(most_similar)

        return most_similar[:1]

    def common_song_artist_helper(self, country: str, type: str) -> list[str]:
        """
              Returns the top 5 artists/songs in a particular country

              Representation Invariants:
                  - type in {'artist', 'song'}

              """
        top_songs = self.top_n(5, country)
        top = []

        if type == 'artist':
            for artist in top_songs:
                top.append(artist[1])
        else:
            for song in top_songs:
                top.append(song[0])

        return top

    def recommend_common_song(self, songs: list[str], region_range: str, ranked = False) -> Song:
        """Returns n number of new songs from the region who have the most common songs with the provided songs list.
        
        Preconditions:
            - n >= 1
            - all(song in self for song in songs)
            - region_range in {'continent', 'country', 'city'}
        """
        scores = []
        
        if region_range == 'continent':
            for continent in self._subtrees:
                scores.append(continent.get_comparison_score(songs, region_range, ranked))
        elif region_range == 'country':
            for continent in self._subtrees:
                for country in continent._subtrees:
                    scores.append(country.get_comparison_score(songs, region_range, ranked))
        else:
            for continent in self._subtrees:
                for country in continent._subtrees:
                    for city in country._subtrees:
                        scores.append(city.get_comparison_score(songs, region_range, ranked))

        scores.sort(reverse=True)
        has_song = False
        while not has_song and :
            

    def get_comparison_score(self, songs: list[str], region_range: str, ranked = False) -> tuple[float, str]:
        """Computes a comparison score of this region to the provided songs list on the following specifications:

        Preconditions:
            - self is a tree representing a region
            - self has >= 1 song
            - region_range in {'continent', 'country', 'city'}
            - isinstance(self._root, str)
        """
        scores = []
        num_occurance = 0
        num_songs = 0

        if region_range == 'continent':
            for country in self._subtrees:
                for city in country._subtrees:
                    for song in city._subtrees:
                        if isinstance(song._root, Song) and song._root.title in songs:
                            num_occurance += 1
                            num_songs += 1
                            
        elif region_range == 'country':
            for city in self._subtrees:
                for song in city._subtrees:
                    if isinstance(song._root, Song) and song._root.title in songs:
                        num_occurance += 1
                        num_songs += 1
                        
        else:
            for song in self._subtrees:
                if isinstance(song._root, Song) and song._root.title in songs:
                    num_occurance += 1
                    num_songs += 1

        if num_songs == 0:
            return (0, self._root)
        return (num_occurance/num_songs, self._root)

class Song:
    """A class storing metadata of a song.
        Instance Attributes:
          - title: the name of the song
          - artist: the name of the artist
          - streams: the number of streams of the song
          - rank: The rank of the song in the city/country
    """
    title: str
    artist: str
    streams: Union[int, str]
    rank: int

    def __init__(self, title: str, artist: str, streams: Union[int, str], rank: int) -> None:
        self.title = title
        self.artist = artist
        self.streams = streams
        self.rank = rank
  