SET DEFAULT_PARALLEL 50;

register /home/user/datasci_course_materials/cloud_quiz/pigtest/myudfs.jar

-- avoid java.lang.OutOfMemoryError: Java heap space (execmode: -x local)
set io.sort.mb 10;

raw = load 'cse344-test-file-100' using TextLoader as (line:chararray);

ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray, predicate:chararray, object:chararray);

subjects = group ntriples by (subject);

count_by_subject = foreach subjects generate flatten($0), COUNT($1) as sub_count ;

sub_counts = group count_by_subject by (sub_count);

count_by_sub_count = foreach sub_counts generate flatten($0), COUNT($1);

dump count_by_sub_count;
