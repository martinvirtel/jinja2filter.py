<!-- Automatically generated from README.md.edit. Please edit that file -->

# jinja2filter.py

Takes all the [Jinja2](https://jinja.pocoo.org) magic to the command line. 



## Commandline help:
<div data-cmdline="./jinja2filter.py --help"></div>

```

Usage: jinja2filter.py [OPTIONS]

      pipes JSON, CSV or plain text from STDIN using a jinja2 --template or
      --templatefile to STDOUT

  Example:

      echo '{ "name": "one", "value" : 1} ' | ./jinja2filter.py --template
      '{{data.name|title}} is written as {{data.value}}.'

      >> One is written as 1.

  Example with loop:

      echo '[ { "name": "two",  "value": 2 }, { "name" : "one", "value" : 1
      }]' |     ./jinja2filter.py --template '{% for n in data %}{{n.value}}
      is called "{{n.name|title}}". {%endfor%}'

      >> 2 is called "Two". 1 is called "One".

  Example with file (see test.jinja2 in the source code repository):

      echo '[ 1,2,3 ]' ./jinja2filter.py --templatefile test.jinja2

  See also

      https://jinja.pocoo.org



Options:
  --loglevel TEXT      python log level name
  --template TEXT      read jinja2 template string
  --templatefile TEXT  read jinja2 template file
  --templatevar TEXT   read jinja2 template from this environment variable
  --lineregex TEXT     each input line is regex-parsed into a JSON object, the
                       property names are set using using (?P<var>)
                       expressions. Use the data variable inside the jinja2
                       template to loop over the objects
  --csv                process STDIN as csv file with header row
  --help               Show this message and exit.


```


<div></div>
