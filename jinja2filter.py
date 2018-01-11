#! /home/martin/.virtualenvs/lambdascraper/bin/python3


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
@click.option('--template',default=None,help='read jinja2 template string')
@click.option('--templatefile',default=None,help='read jinja2 template file')
@click.option('--templatevar',default=None,help='read jinja2 template from this environment variable')
@click.option('--lineregex',default=None,help='each input line is regex-parsed into a JSON object, the property names are set using using (?P<var>) expressions. Use the data variable inside the jinja2 template to loop over the objects')
@click.option('--csv',is_flag=True,default=None,help='process STDIN as csv file with header row')
def generate(loglevel='INFO',template=None,templatefile=None,templatevar=None,lineregex=None,csv=None) :
    """
    pipes JSON, CSV or plain text from STDIN using a jinja2 --template or --templatefile to STDOUT


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
    if lineregex is not None :
        r=re.compile(lineregex)
        objects=[ a.groupdict() for a in (r.search(l) for l in sys.stdin.readlines()) if a is not None ]
    elif csv is not None :
        import csv
        rd=csv.DictReader(sys.stdin)
        objects=[a for a in rd]

    else :
        obs=sys.stdin.read()
        try :
            objects=json.loads(obs)
        except Exception as e:
            print(obs)
            raise
    if template is not None :
        content=env.from_string(template)
    elif templatefile is not None :
        content=env.get_template(templatefile)
    elif templatevar is not None :
        content=env.from_string(os.environ[templatevar])
    sys.stdout.write(content.render(data=objects))



if __name__=='__main__' :
    generate()
