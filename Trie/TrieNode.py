class TrieNode(object):
    def __init__(self) -> None:
        self._children = {}
        self._count = 0

    def __bool__(self):
        return self._count > 0
    
    def __contains__(self, item):
        return item in self._children
    
    def __getitem__(self, char):
        return self._children[char]
    
    def __setitem__(self, char, node):
        self._children[char] = node
    
    def addCharacter(self, char, node):
        self._children[char] = node

    def __len__(self):
        return self._count
    
    def __add__(self, value):
        self._count += value

    def __iter__(self):
        return iter(self._children)

    def __next__(self):
        raise StopIteration
    
    def __str__(self):
        return f"Deca: {self._children.keys()}\nCount: {self._count}"
    

if __name__ == "__main__":
    pass
    
    