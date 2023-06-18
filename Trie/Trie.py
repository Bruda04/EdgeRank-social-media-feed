from .TrieNode import TrieNode
import re

class Trie(object):
    def __init__(self, statusId, text):
        self._statusId = statusId
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

                
