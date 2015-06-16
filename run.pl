#!/usr/bin/perl

$linie
while($line = <>)
{

	$linie++;

}

$ile=$linie/100
for($i = 0; $i < 100; $i++) {
	`perl worker.pl $i*$ile+1 ($i+1)*$ile &`;
}

	//`python find_plot.py $line &`;
