from __future__ import annotations
from typing import Any, Optional

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
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.

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
        """Return whether the given is in this tree.

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

    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        return self._str_indented(0).rstrip()

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            str_so_far = '  ' * depth + f'{self._root}\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                str_so_far += subtree._str_indented(depth + 1)
            return str_so_far

    def insert_sequence(self, items: list) -> None:
        """function from exercise 2

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
          
    #Tree functions
    def top_n(self, n: int, target: str) -> list[str]:
      """
      Returns the top n songs of a specific country. Returns [] if the country is not found.  
      """
      if self._root == target:
        return self._search_songs(n, {})
      elif self._subtrees == []:
        return []
      else:
        for subtree in self._subtrees:
          top = subtree.top_n(n, target)
          if top != []:
            return top

        return []
        
      
      # if not self.__contains__(country):
      #   return []
      
      # for subtree_conti in self._subtrees:
      #   for subtree_country in subtree_conti._subtrees:
      #     if self._root == country:
      #       return subtree_country._search_songs(n)
            

    def _search_songs(self, n: int, songs: dict) -> dict:
      """
      This is a helper function for top_n, it returns the name of the top n songs. 
      """
      
      if isinstance(self._root, Song):
        if self._root.title in songs:
          songs[self._root.title] += 1
        else:
          songs[self._root.title] = 1

        return songs
      else:
        for subtree in self._subtrees:
          subtree._search_songs(n, songs)

        songs = dict(sorted(songs.items(), key=lambda x: x[1], reverse=True))
        songs = list(songs)
        if len(songs) >= n:
          return songs[:n]
        else:
          return list(songs)

        return songs
      
        
      
      # for city in self._subtrees:
      #   for song in city._subtrees:
      #     if song._root.title in songs:
      #       songs[song._root.title] += 1
      #     else:
      #       songs[song._root.title] = 1



class Song:
    """A class storing metadata of a song.

    Instance Attributes:
        - title: the name of the song
        - artist: the name of the artist
        - streams: the number of streams of the song
    """
    title: str
    artist: str
    streams: int

    def __init__(self, title: str, artist: str, streams: int) -> None:
      self.title = title
      self.artist = artist
      self.streams = streams

# change streams to a dict?

if __name__ == '__main__':
  tree = Tree('World', [Tree('Can', [Tree('Canada', [Tree(Song('Richard', 'R', 5), [])])]), Tree('Stat', [Tree('US', [Tree(Song('Mina', 'M', 4), [])])])])
  print(tree._search_songs(4, {}))