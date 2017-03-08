#!/bin/bash
#NOTE: if you want to use this build script you will need to change --data-dir=$HOME/Git-Working/hierarchical-framework-intestinal-epithelium/markdown-files to point the appropriate location you clone the repo to. You also need to make sure the pandoc filters used below are installed.

pandoc --filter pandoc-fignos --filter pandoc-eqnos --filter pandoc-citeproc --data-dir=$HOME/Git-Working/hierarchical-framework-intestinal-epithelium/markdown-files --template plos2015.latex --latex-engine=xelatex hierarchical-intestinal.md -o ../manuscript-pdf/hierarchical-intestinal.pdf

pandoc --filter pandoc-fignos --filter pandoc-eqnos --filter pandoc-citeproc --data-dir=$HOME/Git-Working/hierarchical-framework-intestinal-epithelium/markdown-files --template plos2015_nologo.latex --latex-engine=xelatex hierarchical-intestinal.md -o ../manuscript-pdf/hierarchical-intestinal-nologo.pdf

pandoc --filter pandoc-fignos --filter pandoc-eqnos --filter pandoc-citeproc --data-dir=$HOME/Git-Working/manuscripts-and-notes/crypt-villus-hierarchical-paper/markdown-files --latex-engine=xelatex supplementary-information.md -o ../manuscript-pdf/supplementary-information.pdf

#
#--standalone --natbib --bibliography=../bibtex-files/crypt-villus-refs.bib