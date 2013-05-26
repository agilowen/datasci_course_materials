import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = value.split()
    for w in words:
      mr.emit_intermediate(w, key)

def reducer(key, list_of_docs):
    # key: word
    # value: list of document_ids
    unique_list_of_docs=[]
    for doc in list_of_docs:
        if doc not in unique_list_of_docs:
            unique_list_of_docs.append(doc)
    mr.emit((key, unique_list_of_docs))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
