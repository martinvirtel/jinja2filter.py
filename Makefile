
SHELL := /bin/bash


README.md : README.md.edit
	awk  'BEGIN { print("<!-- Automatically generated from README.md.edit. Please edit that file -->\n") }/<div data-cmdline/ {  print; match($$0,/cmdline="(.+)">/,arr); system(arr[1]);     } /<\/div>/ {print}  /<div data-cmdline/,/<\/div>/{ next } { print }' \
	<README.md.edit >README.md
