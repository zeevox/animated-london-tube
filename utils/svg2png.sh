#!/bin/bash

find $1 -type f -name "*.svg" | xargs -n1 -P4 inkscape --export-type="png" --export-background="white"
mkdir $1/png
mv $1/*.png $1/png
