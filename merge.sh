#!/bin/bash
filename='list.txt'
resultfile_hdr='combined.h'
resultfile_src='combined.c'
rm -f $resultfile_src
rm -f $resultfile_hdr
rm -f $filename

#ls -l | awk -F' ' '{print $9}'  > $filename
find -type f -iname "*.h" > $filename
echo "starting merge : "
while read p; do
	echo "// $p" >> $resultfile_hdr
	echo "//-----------------------------------------"  >> $resultfile_hdr
	cat "$p" >> $resultfile_hdr
done < $filename
echo "Done"
rm -f $filename

#ls -l | awk -F' ' '{print $9}'  > $filename
find -type f -iname "*.c" > $filename
echo "starting merge : "
while read p; do
	echo "// $p" >> $resultfile_src
	echo "//-----------------------------------------"  >> $resultfile_src
	cat "$p" >> $resultfile_src
done < $filename
echo "Done"
rm -f $filename


