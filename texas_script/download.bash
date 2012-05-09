#!/bin/bash
wget 'http://records.texastribune.org/dataapps/salaries.csv' -O - | bzip2 > "Texas state employees$( date --utc --rfc-3339=seconds ).csv.bz2"
