SET DEFAULT_PARALLEL 50;

register /home/user/datasci_course_materials/cloud_quiz/pigtest/myudfs.jar

-- avoid java.lang.OutOfMemoryError: Java heap space (execmode: -x local)
set io.sort.mb 10;

raw = load 'cse344-test-file-10' using TextLoader as (line:chararray);

ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray, predicate:chararray, object:chararray);

filtered_ntriples = filter ntriples by subject matches '.*business.*';

filtered_ntriples_2 = foreach filtered_ntriples generate $0 as subject2,$1 as predicate2,$2 as object2;


join_result = join filtered_ntriples by subject, filtered_ntriples_2 by subject2;


distinct_results = DISTINCT join_result;

dump distinct_results;

-- join_grouped = group join_result ALL;
-- count_join = foreach join_grouped generate COUNT($1);

-- join_distinct_grouped = group distinct_results ALL;
-- count_join_distinct = foreach join_distinct_grouped generate COUNT($1);

-- dump count_join;
-- dump count_join_distinct;

