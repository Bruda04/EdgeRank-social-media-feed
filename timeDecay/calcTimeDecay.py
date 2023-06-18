from Parsers.myParser import load_friends, load_comments, load_shares, load_reactions, load_statuses
from datetime import datetime


def calcTimeDecay(graph, ulogovan, statuses):
    statuses = load_statuses("dataset/test_statuses.csv")

    consts = {
        "timeDecay": 0.9
    }

    objaveDecay = {}

    for relacija in graph.neighbors(ulogovan):
        if not relacija in statuses:
            continue
        for objava in statuses[relacija]:
            tmpObjava = statuses[relacija][objava]

            tDelta = (datetime.now() - datetime.strptime(tmpObjava["status_published"], "%Y-%m-%d %H:%M:%S")).days

            t = consts["timeDecay"]**tDelta

            objaveDecay[objava] = t

    return objaveDecay



        

if __name__ == "__main__":
    pass