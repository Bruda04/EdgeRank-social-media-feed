from datetime import datetime


def calcTimeDecay(graph, ulogovan, statuses):

    consts = {
        "timeDecay": 0.7
    }

    objaveDecay = {}

    for relacija in graph.neighbors(ulogovan):
        if not relacija in statuses:
            continue
        for objava in statuses[relacija]:
            tmpObjava = statuses[relacija][objava]

            tDelta = (datetime.now() - datetime.strptime(tmpObjava["status_published"], "%Y-%m-%d %H:%M:%S")).days

            t = consts["timeDecay"]**(2*tDelta)

            objaveDecay[objava] = t

    return objaveDecay

        

if __name__ == "__main__":
    pass