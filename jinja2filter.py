#! /usr/bin/env python

import os
import sys
import json
from jinja2 import Environment,PackageLoader,FunctionLoader
import logging
import datetime
import re
import random
import click
import locale


locale.setlocale(locale.LC_ALL, 'de_DE.utf8')




logging.basicConfig(stream=sys.stderr,level=logging.DEBUG,format='%(asctime)s %(name)s %(filename)s:%(lineno)s %(message)s ')
logger=logging.getLogger(__name__)







def fileloader(filename) :
    with open(filename) as f :
        return "".join((a for a in f.read()))



env = Environment(loader=FunctionLoader(fileloader),
                  extensions=['jinja2.ext.with_','jinja2_slug.SlugExtension']
                  )

@click.command()
@click.option('--loglevel',default='INFO',help='python log level name')
@click.option('--template',default=None,help='jinja2 template string')
@click.option('--templatefile',default=None,help='jinja2 template file')
@click.option('--templatevar',default=None,help='jinja2 template environment variable')
def generate(loglevel='INFO',template=None,templatefile=None,templatevar=None) :
    """
    pipes JSON from STDIN using a jinja2 --template or --templatefile to STDOUT


Example:

    echo '{ "name": "one", "value" : 1} ' | ./jinja2filter.py --template '{{data.name|title}} is written as {{data.value}}.'

    >> One is written as 1.

Example with loop:

    echo '[ { "name": "two",  "value": 2 }, { "name" : "one", "value" : 1 }]' | \
    ./jinja2filter.py --template '{% for n in data %}{{n.value}} is called "{{n.name|title}}". {%endfor%}'

    >> 2 is called "Two". 1 is called "One".


Example with file (see test.jinja2 in the source code repository):

    echo '[ 1,2,3 ]' ./jinja2filter.py --templatefile test.jinja2

See also

    https://jinja.pocoo.org


    """
    try :
        logger.setLevel(getattr(logging,loglevel))
    except AttributeError :
        raise ValueError("Log level {} not defined. Possible values: CRITICAL, ERROR, WARNING, INFO, DEBUG".format(loglevel))
    objects=json.load(sys.stdin)
    if template is not None :
        content=env.from_string(template)
    elif templatefile is not None :
        content=env.get_template(templatefile)
    elif templatevar is not None :
        content=env.from_string(os.environ[templatevar])
    sys.stdout.write(content.render(data=objects))



if __name__=='__main__' :
    generate()
