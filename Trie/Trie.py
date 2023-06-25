from .TrieNode import TrieNode
import re

class Trie(object):
    def __init__(self, statusId, objavljivac, text):
        self._statusId = statusId
        self._objavljivac = objavljivac
        self._rootNode = TrieNode()
        self._text = text

        listaReci = re.findall(r"[\w@#']+", text)

        self.lista = [rec.lower() for rec in listaReci]

        for rec in self.lista:
            tmpNode = self._rootNode

            for slovo in rec:
                if slovo in tmpNode:
                    tmpNode = tmpNode[slovo]
                else:
                    tmpNode[slovo] = TrieNode()
                    tmpNode = tmpNode[slovo]

            tmpNode + 1

    def __contains__(self, word):
        tmpNode = self._rootNode

        for slovo in word:
            if slovo in tmpNode:
                tmpNode = tmpNode[slovo]
            else:
                return False
            
        return tmpNode
    
    def occurrences(self, word):
        tmpNode = self._rootNode

        for slovo in word:
            if slovo in tmpNode:
                tmpNode = tmpNode[slovo]
            else:
                return False
              
        return len(tmpNode)
    
    def flexSearch(self, word):
        prefix = word.split("*")[0]

        tmpNode = self._rootNode

        for slovo in prefix:
            if slovo in tmpNode:
                tmpNode = tmpNode[slovo]
            else:
                return False
        
        return True
    
    def flexSearchOccurrances(self, word):
        prefix = word.split("*")[0]

        tmpNode = self._rootNode

        for slovo in prefix:
            if slovo in tmpNode:
                tmpNode = tmpNode[slovo]
            else:
                return False
            
        occurances = self._postorder(tmpNode, 0)

        return occurances

    def _postorder(self, node, occurrances):
        stanje = occurrances
        for child in node:
            stanje = self._postorder(node[child], stanje)

        if node:
            return stanje + len(node)
        else: 
            return stanje
        

    @property
    def statusId(self):
        return self._statusId
       
    @property
    def objavljivac(self):
        return self._objavljivac
                
if __name__ == "__main__":
    pass