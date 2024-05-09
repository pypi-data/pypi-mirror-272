

#----
#
from vegan._essence import retrieve_essence
#
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
import sanic.response as sanic_response
from sanic_limiter import Limiter, get_remote_address
#from sanic.response import html
#
#
import json
from os.path import exists, dirname, normpath, join
from urllib.parse import unquote
#
#----

'''
from flask import Flask, request, send_file, request, make_response, send_from_directory, Response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO, emit
'''
#

'''
def vue_regions (
	app = {},
	cache = None,
	mode = "",
	vue_dist_inventory = []
):
'''

def vue_regions (vue_regions_packet):
	app = vue_regions_packet ["app"]
	front_inventory_paths = vue_regions_packet ["front_inventory_paths"]
	public_addresses = vue_regions_packet ["public_addresses"]
	
	#
	#	get?
	#
	#
	@public_addresses.route ("/")
	async def home (request):
		essence = retrieve_essence ()
		#return sanic_response.text ("home")
		
		#
		#	mimetype = vue_dist_inventory [ "index.html" ] ["mime"],
		#
		#
		
		return sanic_response.html (front_inventory_paths ["index.html"] ["content"])

	'''
	@app.route ("/at/grocery-list")
	async def at_address (request):
		print ("/at/address")
	
		essence = retrieve_essence ()
		return sanic_response.html (front_inventory_paths ["index.html"] ["content"])

	@app.route ("/#/grocery-list",  unquote=True)
	async def at_symbol_address (request):
		print ("/@/address")
	
		essence = retrieve_essence ()
		return sanic_response.html (front_inventory_paths ["index.html"] ["content"])
	'''
	
	@public_addresses.route("/front/<encoded_path:path>")
	async def handle_path (request, encoded_path):
		path = unquote (encoded_path)
		return sanic_response.html (front_inventory_paths ["index.html"] ["content"])

	''''
		objectives:
			caching
	
		headers = {
			"Cache-Control": "private, max-age=31536000",
			"Expires": "0"
		}
	'''#
	@public_addresses.route("/collection/<path:path>")
	async def public_route (request, path):	
		
		try:
			full_path = f"collection/{ path }"
			if (full_path in front_inventory_paths):
				content_type = front_inventory_paths [ full_path ] ["mime"]
				content = front_inventory_paths [ full_path ] ["content"]
					
				return sanic_response.raw (content, content_type = content_type)
				
			return sanic_response.text ("not found", status = 604)	
		except Exception as E:
			print ("E:", E)
	
		return sanic_response.text ("An anomaly occurred while processing.", status = 600)	
		
	@public_addresses.route("/assets/<path:path>")
	async def assets_route (request, path):
		#print (f"address: /assets/{ path }")
		try:
			full_path = f"assets/{ path }"	
			if (full_path in front_inventory_paths):
				content_type = front_inventory_paths [ full_path ] ["mime"]
				content = front_inventory_paths [ full_path ] ["content"]
			
				return sanic_response.raw (content, content_type=content_type)
		except Exception as E:
			print ("E:", E)
	
		return sanic_response.text ("An anomaly occurred while processing.", status = 600)
	