# A hierarchical Bayesian framework for understanding the spatiotemporal dynamics of the intestinal epithelium
All of the files, code and data associated with the manuscript 'A hierarchical Bayesian framework for understanding the spatiotemporal dynamics of the intestinal epithelium' by Oliver J Maclaren (me), Aimee Parker, Carmen Pin, Simon R Carding, Alastair JM Watson, Alexander G Fletcher, Helen M Byrne, Philip K Maini.

The full manuscript, author information and copyright information can found here: http://biorxiv.org/content/early/2016/10/25/072561. (The copyright holder for this preprint is the author/funder. It is made available under a CC-BY-NC-ND 4.0 International license.)

I need to tidy some of this up a little, so let me know if you would like to re-use anything and need help.

I used markdown to write the paper and the build script 'buildpaper.sh' uses pandoc to compile the paper. This script can be found in the 'markdown-files' directory (where most of the action is). Note that I used 'xelatex' as the latex compiler. The output pdf file can be found in the 'manuscript-pdf' directory.

Assuming you have pandoc, xelatex etc installed, you *should* be able to build the manuscript using this - you just need to make sure the repo path is correct in this script (note in the script that I used a parent 'Git-Working' directory).  