
SHELL := /bin/bash


README.md : README.md.edit jinja2filter.py
	awk  'BEGIN { print("<!-- Automatically generated from README.md.edit. Please edit that file -->\n") }/<div data-cmdline/ {  print; print("```\n"); match($$0,/cmdline="(.+)">/,arr); system(arr[1]); print("\n```\n"); } /<div><\/div>/ {print}  /<div data-cmdline/,/<div><\/div>/{ next } { print }' \
	<README.md.edit >README.md
