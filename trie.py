#!/usr/bin/env python
import collections

class _Node(object):

    def __init__(self, is_member=False, children=None):
        self.is_member = is_member
        self.children = children or {}

    def __repr__(self):
        return '_Node(is_member={0}, children={1})'.format(
            repr(self.is_member), repr(self.children))


class Trie(object):
    """"A data structure that can store a set of "dense" strings while
    using memory judiciously.

    A dense set of strings is defined as a set in which many strings
    share the same prefix (e.g., all words in a dictionary).
    """

    def __init__(self, initial_data=None):
        self.root = _Node()
        for word in initial_data or []:
            self.Add(word)

    def Add(self, value):
        """Adds an element to the set."""
        if not isinstance(value, basestring):
            raise TypeError(
                'only strings can be placed in the trie; received: {0}'
                .format(value))

        current = self.root
        for char in value:
            child = current.children.get(char)
            if child:
                current = child
            else:
                new_node = _Node()
                current.children[char] = new_node
                current = new_node
        current.is_member = True

    def GetMembers(self):
        """Returns a list containing all elements in the trie. The list
        elements are presented in sorted order."""
        def GetMembers(current):
            for letter, child in sorted(current.children.iteritems()):
                if child.is_member:
                    yield letter
                for res in GetMembers(child):
                    yield letter + res

        members = []
        if self.root.is_member:
            members.append('')
        members.extend(GetMembers(self.root))
        return members

    def __contains__(self, value):
        """Returns True if the given value is in the trie."""
        if not isinstance(value, basestring):
            return False

        current = self.root
        for char in value:
            child = current.children.get(char)
            if child:
                current = child
            else:
                return False

        return current.is_member

    def __nonzero__(self):
        """Returns True if at least one element is in the trie."""
        return self.root.is_member or bool(self.root.children)

    def __repr__(self):
        """Returns a representation of the state of the trie."""
        return 'Trie([{0}])'.format(repr(self.GetMembers()))


if __name__ == '__main__':
    t = Trie()
    t.Add('')
    t.Add('hello')
    t.Add('h')
    t.Add('he')
    t.Add('hee')
    t.Add('world')
    t.Add('www')
    assert repr(t) == "Trie([['', 'h', 'he', 'hee', 'hello', 'world', 'www']])"
    assert 'hello' in t
    assert 'hello world' not in t
    assert '' in t
    assert 'hel' not in t
    assert 1 not in t
    assert t
    assert not Trie()
