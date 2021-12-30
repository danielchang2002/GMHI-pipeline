#!/bin/sh
grep -E "s__|clade" merged.txt | sed 's/^.*s__/s__/g'\
| cut -f1,3-8 | sed -e 's/clade_name/microbe/g' > abundance.txt
