#! /usr/bin/env python

import os
import sys
import json
from jinja2 import Environment,PackageLoader
import logging
import datetime
import re
import random
import click
import locale


locale.setlocale(locale.LC_ALL, 'de_DE.utf8')




logging.basicConfig(stream=sys.stderr,level=logging.DEBUG,format='%(asctime)s %(name)s %(filename)s:%(lineno)s %(message)s ')
logger=logging.getLogger(__name__)



env = Environment(
                  extensions=['jinja2.ext.with_','jinja2_slug.SlugExtension']
                  )









@click.command()
@click.option('--loglevel',default='INFO',help='python log level name')
@click.option('--template',default=None,help='jinja2 template string')
def generate(loglevel='INFO',template=None) :
    """
    pipes JSON from STDIN using a jinja2 --template to STDOUT


    Example:

    echo '{ "name": "one", "value" : 1} ' | ./jinja2filter.py --template '{{data.name|title}} is written as {{data.value}}.'

    >> One is written as 1.

    Example with loop:

    echo '[ { "name": "two",  "value": 2 }, { "name" : "one", "value" : 1 }]' | \
    ./jinja2filter.py --template '{% for n in data %}{{n.value}} is called "{{n.name|title}}". {%endfor%}'

    >> 2 is called "Two". 1 is called "One".


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
    sys.stdout.write(content.render(data=objects))



if __name__=='__main__' :
    generate()
