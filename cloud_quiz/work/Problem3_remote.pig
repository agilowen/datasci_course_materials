SET DEFAULT_PARALLEL 50;

register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray);

ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray, predicate:chararray, object:chararray);

filtered_ntriples = filter ntriples by subject matches '.*rdfabout\\.com.*';

filtered_ntriples_2 = foreach filtered_ntriples generate $0 as subject2,$1 as predicate2,$2 as object2;


join_result = join filtered_ntriples by object, filtered_ntriples_2 by subject2;

distinct_results = DISTINCT join_result;

-- dump distinct_results;

join_grouped = group distinct_results ALL;
count_join = foreach join_grouped generate COUNT($1);

dump count_join;



