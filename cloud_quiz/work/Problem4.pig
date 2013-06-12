SET DEFAULT_PARALLEL 50;

register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-*' USING TextLoader as (line:chararray); 

ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray, predicate:chararray, object:chararray);

subjects = group ntriples by (subject);

count_by_subject = foreach subjects generate flatten($0), COUNT($1) as sub_count ;

sub_counts = group count_by_subject by (sub_count);

count_by_sub_count = foreach sub_counts generate flatten($0), COUNT($1);

all_grouped = group count_by_sub_count ALL;
count_all = foreach all_grouped generate COUNT($1);
dump count_all;

store count_by_sub_count into '/user/hadoop/Problem4-results-2';
store count_all into  '/user/hadoop/Problem4-count-2';




