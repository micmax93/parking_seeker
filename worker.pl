#!/usr/bin/perl

$start=$ARGV[0];
$end=$ARGV[1];

use strict;
use warnings;

$file = 'names.txt';
open $info, $file or die "Could not open $file: $!";

$count = 1;
while(  $line = <$info>)  {
    if($count>=$start && $count<=end){
    `python find_plot.py $line`;
    }
    ++$count;
}

