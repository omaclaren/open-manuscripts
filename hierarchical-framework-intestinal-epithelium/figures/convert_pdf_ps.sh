#!/bin/bash
# batch convert pdf to tiff files
# takes one argument, resolution in dpi
# use: pdf2tiff.sh 150
# will convert all pdfs in the current
# directory to tiff files at 150dpi

cd ./figures_to_include
files=`ls *.pdf`

for i in $files;do
	# get the filename without the extension
	noextension=`echo $i | sed 's/\(.*\)\..*/\1/'`
	filename=`echo $noextension.eps`
	echo $filename
    pdf2ps -sOutputFile=../eps_figures_to_include/$filename $i

done

exit 1
