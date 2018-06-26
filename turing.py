import csv
import sys

DIRECTION = {
    "R": 1,
    "L": -1,
    "C": 0
}

def printState(state,currentVals,prevState,strips,currentPointer):
    print("try find:",serializeKey(state,currentVals))
    print("prev state:",prevState)
    for i,s in enumerate(strips):
        print("".join(s))
        print(" "*currentPointer[i] + "^")
        print("")

def serializeKey(state,letters):
    return " ".join([state,",".join(letters)])

def readConfFile(path):
    rows = {}
    with open(path, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            rows[serializeKey(row[0],row[1].split(","))] = {
                'new-state': row[2],
                'new-letters': row[3].split(","),
                'move': row[4].split(",")
            }
        return rows
def main():
    conf = readConfFile(sys.argv[1])
    num_of_strips = int(sys.argv[2])
    startInput = sys.argv[3]
    strips = [list("#" * 20)] * num_of_strips
    strips[0] = ["#"] + list(startInput) + ["#"]
    currentPointer = [len(strips[0]) - 1] + [0] * (num_of_strips - 1)
    state = 's'
    stuck = False
    prevState = 'before-s'
    while state != 'h' and not stuck:
        currentVals = [ strips[i][p] for i,p in enumerate(currentPointer)]
        key = serializeKey(state,currentVals)
        if key in conf:
            #printState(state,currentVals,prevState,strips,currentPointer)
            line = conf[serializeKey(state,currentVals)]
            for i,p in enumerate(currentPointer):
                strips[i][p] = line["new-letters"][i]
                currentPointer[i] = p + DIRECTION[line["move"][i]]
            prevState = state
            state = line['new-state']
        else:
            print("Machine Stuck!")
            printState(state,currentVals,prevState,strips,currentPointer)
            stuck = True
    if not stuck:
        for i,s in enumerate(strips):
            printState(state,currentVals,prevState,strips,currentPointer)

main()

