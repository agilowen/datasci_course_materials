SET DEFAULT_PARALLEL 50;

register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray); 

ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray, predicate:chararray, object:chararray);

subjects = group ntriples by (subject);

count_by_subject = foreach subjects generate flatten($0), COUNT($1) as sub_count ;

sub_counts = group count_by_subject by (sub_count);

count_by_sub_count = foreach sub_counts generate flatten($0), COUNT($1);

dump count_by_sub_count;

store count_by_object_ordered into '/user/hadoop/Problem2B-results' using PigStorage();
