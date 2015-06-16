#!/usr/bin/perl

print "aaa";
$file = 'names.txt';
open $info, $file or die "Could not open $file: $!";

$linie=0;
while($line = <$info>){
        ++$linie;
}
{
use integer
$ile=$linie/10;
}
for($i = 0; $i < 10; $i++) {

$start= $i*$ile+1;
 $end= ($i+1)*$ile;
        `perl worker.pl $start $end &`;
}

        # `python find_plot.py $line &`;
