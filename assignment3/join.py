import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: order_id
    # value: entire record 
    key = record[1]
    value = record
    mr.emit_intermediate(key, value)

def reducer(key, records):
    # key: order_id
    # value: list of record
    order_records = []
    item_records = []
    
    joined_records = [] #for given key order_id
    
    for record in records:
        if record[0] == "order":
            order_records.append(record)
        elif record[0] == "line_item":
            item_records.append(record)
    
    for order_rec in order_records:
        for item_rec in item_records:
            joined_records.append(order_rec + item_rec)

    for record in joined_records:
        mr.emit(record)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
