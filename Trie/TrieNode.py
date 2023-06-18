class TrieNode(object):
    def __init__(self, children = {}, isWord = False) -> None:
        self._children = children
        self._isWord = isWord

    def __bool__(self):
        return self._isWord
    
    def __contains__(self, item):
        return item in self._children
    
    def __getitem__(self, char):
        return self._children[char]
    
    def __setitem__(self, char, node):
        self._children[char] = node
    
    def addCharacter(self, char, node):
        self._children[char] = node
    
    @property
    def isWord(self):
        return self._isWord

    @isWord.setter
    def isWord(self, value):
        self._isWord = value
    
    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    def __str__(self):
        ret = ""
        for child in self.children:
            try:
                ret += str(self.children[child])
            except:
                ret += ""
                break
    
        return ret