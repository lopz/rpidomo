#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sin título.py
#  
#  Copyright 2013 JJ Lopez <lopz@brandy>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import subprocess
import json

from bottle import route, run, template, debug, static_file, post
from bottle import request, response


TOKENS = ["1234"]

atonos = ["me", "nos", "te", "lo", "le", "los", "la", "las", "les", "se"]

resp = {"status": {"lights": {"living": "ON", "bed": "OFF"},
					"cameras": {"cam1": "OFF", "cam2": "ON"}
					},
                                    	"error": {"msg": "OK"}
		}

GPIOS = [9, 10, 11]

things = ["luz", "aire"]
places = {"dormitorio": 9, "sala": 10, "cocina": 11}

config = {"dormitorio": {
						"luz": {"intensidad": 2},
						"aire":	{"temperatura": 3}
						}, 
			"sala": {
					"luz": {"intensidad": 3}, 
					"aire": {"temperatura": 4}, 
					"television": {"canal": 5}
					}, 
			"cocina": {
					"luz": {"intensidad": 2},
					}
		}

accions = []

def clear_cmd(cmd):
	for atono in atonos:
		cmd = cmd.replace(atono, "")
	return cmd

def select_verb(phrase):
	for v in verbs:
		if v in phrase:
			return verbs[v]

def select_thing(phrase):
	for thing in things:
		if thing in phrase:
			return thing

def select_place(phrase):
	for place in places:
		if place in phrase:
			return place	

def action(phrase):
	verb = select_verb(phrase)
	thing = select_thing(phrase)
	place = select_place(phrase)
	if (verb and thing and place):
		return verb(place, thing)
	else:
		return "No pude entender la orden"

def turn_on(place, thing):
	gpio = places[place]
	print "Encender", place, thing
	try:
		#std = subprocess.check_output(["rpio", "--set", "%d:1" % gpio])
		return "%s de %s encendido" % (thing, place)	
	except:
		return "Ocurrio un error"	

	
def turn_off(place, thing):
	gpio = places[place]
	print "Apagar", place, thing
	try:
		#std = subprocess.check_output(["rpio", "--set", "%d:0" % gpio])
		return "%s de %s apagado" % (thing, place)
	except:
		return "Ocurrio un error"	

	
verbs = {"encender": turn_on,
		"activar": turn_on,
		"prender": turn_on,
		"apagar": turn_off, 
		#"bajar": bajar, 
		#"subir": subir
		}



def init_gpios():
	#if not init_flag:
	for i in GPIOS:
		print subprocess.check_output(["rpio", "--setoutput", "%d:0" % i])
	init_flag = True

init_flag = False
#init_gpios()

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static/')

@route('/status/')
def index():
	response.content_type = "application/json"
	return json.dumps(resp)

@route('/message', method='GET')
def command():
	phrase = request.params.q
	#phrase = clear_cmd(cmd)
	resp = action(phrase)
	return resp
	
@route('/gpio/<pin:int>/<state:int>', method='GET')
def get_gpio(pin, state):
	print pin, state

@route('/gpio/', method='POST')
def set_gpio():
    pin = request.params.pin
    state = request.params.state
    cmd = "%s:%s" % (pin, state)
    subprocess.check_output(["rpio", "--set", cmd])
    print cmd


run(reloader=True, host='192.168.1.100', port=8000, debug=True)

