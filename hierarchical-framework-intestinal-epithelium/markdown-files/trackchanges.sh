#!/bin/bash
# NOTE: pretty hacky.

DATADIR=$HOME/Git-Working/open-manuscripts/hierarchical-framework-intestinal-epithelium/markdown-files

#changes
pandoc --filter pandoc-fignos --filter pandoc-eqnos --filter pandoc-citeproc --data-dir=$DATADIR --template plos2015.latex --latex-engine=xelatex old-hierarchical-intestinal.md -o orig.tex

pandoc --filter pandoc-fignos --filter pandoc-eqnos --filter pandoc-citeproc --data-dir=$DATADIR --template plos2015.latex --latex-engine=xelatex hierarchical-intestinal.md -o revised.tex

#requires latexdiff.
latexdiff  -t CFONT orig.tex revised.tex > diff.tex

latexdiff  -t CFONT revised.tex revised.tex > diff.tex

xelatex revised.tex -o revised.pdf
xelatex revised.tex -o revised.pdf
xelatex revised.tex -o revised.pdf

xelatex diff.tex -o diff.pdf
xelatex diff.tex -o diff.pdf
xelatex diff.tex -o diff.pdf

mv diff.pdf ../manuscript-pdf/diff.pdf

#The following is from 'latex-clean.sh' found at https://gist.github.com/dougalsutherland

arg=${1:-.}
exts="aux bbl blg brf idx ilg ind lof log lol lot out toc synctex.gz"

if [ -d $arg ]; then
    for ext in $exts; do
         rm -f $arg/*.$ext
    done
else
    for ext in $exts; do
         rm -f $arg.$ext
    done
fi

