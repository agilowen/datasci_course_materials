import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    matrix = record[0]
    i = record[1]
    j = record[2]
    value = record[3]
    inner_dimension = 5 # of A x B, found from json data

    if matrix == 'a':
        for k in range(0,inner_dimension):
            mr.emit_intermediate((i, k), (matrix, i, j, value))
    elif matrix == 'b':
        for k in range(0,inner_dimension):
            mr.emit_intermediate((k,j), (matrix, i, j, value))
        
def reducer(key, list_of_records):
    dot_product = 0
    list_of_a_records = []
    list_of_b_records = []

    for record in list_of_records:
        if record[0] == 'a':
            list_of_a_records.append(record)
        elif record[0] == 'b':
            list_of_b_records.append(record)

    for record_a in list_of_a_records:
        for record_b in list_of_b_records:
            if record_a[2] == record_b[1]:
                dot_product += (record_a[3] * record_b[3])

    mr.emit((key[0], key[1], dot_product))



# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
