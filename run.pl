#!/usr/bin/perl
while($line = <>)
{
	`python find_plot.py $line &`;
}