#!/bin/bash
pandoc --filter pandoc-fignos --filter pandoc-eqnos --filter pandoc-citeproc --data-dir=$DATADIR --template plos2015.latex --latex-engine=xelatex hierarchical-intestinal.md -o revised.tex

sed 's/\\includegraphics{..\/figures\/figures_to_include\//\\includegraphics[draft]{..\/figures\/figures_to_include\//' revised.tex > revised_submit_formatted.tex

#sed 's/\.pdf//' revised_no_fig.tex > revised_submit_formated.tex

sed -i.bak '65i\
\\renewcommand{\\includegraphics}[2][]{}\
' revised_submit_formatted.tex

#\renewcommand{\includegraphics}[2][]{} /

#sed 's/figures_to_include\//eps_figures_to_include\//' hierarchical-intestinal.md > hierarchical-intestinal-eps.md

#sed 's/.pdf/./' hierarchical-intestinal-eps.md > hierarchical-intestinal-draft-version.md

#DATADIR=$HOME/Git-Working/open-manuscripts/hierarchical-framework-intestinal-epithelium/markdown-files

#pandoc --filter pandoc-fignos --filter pandoc-eqnos --filter pandoc-citeproc --data-dir=$DATADIR --template plos2015.latex --latex-engine=xelatex hierarchical-intestinal-draft-version.md -o draft.tex

xelatex revised_submit_formatted.tex -o revised_submit_formatted.pdf
xelatex revised_submit_formatted.tex -o revised_submit_formatted.pdf
xelatex revised_submit_formatted.tex -o revised_submit_formatted.pdf

mv revised_submit_formatted.pdf ../manuscript-pdf/revised_submit_formatted.pdf

#xelatex draft.tex -o draft.pdf
#xelatex draft.tex -o draft.pdf
#xelatex draft.tex -o draft.pdf

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
