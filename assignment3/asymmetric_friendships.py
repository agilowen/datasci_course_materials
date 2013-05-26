import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: person
    # value: friend

    # forming key from person+friend or friend+person
    # depending on alphabetical order to get unique key
    # for both (personA,personB) and (personB,personA)
    if record[0] <= record[1]:
        key = record[0] + " " + record[1]
    else:
        key = record[1] + " " + record[0]
    mr.emit_intermediate(key, 1)

def reducer(key, list_of_values):
    # key: personApersonB string
    # value: counts
    total = 0
    for v in list_of_values:
      total += v

    # if total = 1, then asymmetric
    if total == 1:
        A_B_list = key.split()
        B_A_list = []
        B_A_list.append(A_B_list[1])
        B_A_list.append(A_B_list[0])
        mr.emit(tuple(A_B_list))
        mr.emit(tuple(B_A_list))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
