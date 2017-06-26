#!/bin/bash
for f in *.tif; do  echo "Converting $f"; convert -compress lzw "$f"  "$f"; done
