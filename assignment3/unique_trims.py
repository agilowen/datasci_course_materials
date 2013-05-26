import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: seq_id 
    # value: nucleotides
    nucleotides = record[1]
    seq_id = record[0]

    # remove last 10 characters
    nucleotides = nucleotides[:-10]
    mr.emit_intermediate(nucleotides, seq_id)

def reducer(key, list_of_seq_id):
    mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
