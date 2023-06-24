def weightCalc(graph, ulogovan, statuses):
    consts = {
        "shares": 10,
        "comments": 5,
        "likes": 1,
    }    

    objaveWeight = {}

    for relacija in graph.neighbors(ulogovan):
        if not relacija in statuses:
            continue
        for objava in statuses[relacija]:
            tmpObjava = statuses[relacija][objava]

            s = int(tmpObjava["num_shares"]) * consts["shares"]

            c = int(tmpObjava["num_comments"]) * consts["comments"]

            l = int(tmpObjava["num_likes"]) * consts["likes"]

            objaveWeight[objava] = s + c + l

    return objaveWeight

if __name__ == "__main__":
    pass