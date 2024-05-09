

'''
	itinerary:
		[ ] pass the current python path to this procedure
'''


'''
	https://sanic.dev/en/guide/running/manager.html#dynamic-applications
'''

'''
	worker manager:
		https://sanic.dev/en/guide/running/manager.html
'''

'''
	Asynchronous Server Gateway Interface, ASGI:
		https://sanic.dev/en/guide/running/running.html#asgi
		
		uvicorn harbor:create
'''

'''
	Robyn, rust
		https://robyn.tech/
'''

'''
	--factory
'''

#----
#
#
from .addresses_protected.besties__food_USDA__nature_v2__FDC_ID import besties__food_USDA__nature_v2__FDC_ID
from .addresses_protected.besties__supp_NIH__nature_v2__DSLD_ID import besties__supp_NIH__nature_v2__DSLD_ID
#
from .addresses_public.vue import vue_regions
from .addresses_protected import addresses_protected
from .addresses_bits import addresses_bits
#
from vegan.adventures.sanique.utilities.generate_inventory_paths import generate_inventory_paths
	
#
from vegan._essence import retrieve_essence, build_essence
from vegan.adventures.alerting import activate_alert
from vegan.adventures.alerting.parse_exception import parse_exception
#
from vegan.adventures.monetary.DB.vegan_tract.goals.retrieve_one import retrieve_one_goal

from vegan.besties.supp_NIH.nature_v2._ops.retrieve import retrieve_parsed_NIH_supp
from vegan.shows_v2.recipe._ops.retrieve import retrieve_recipe
from vegan.shows_v2.recipe_with_goals._ops.formulate import formulate_recipe_with_goals	
#
#
from biotech.topics.show.variable import show_variable
#
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
#from sanic_openapi import swagger_blueprint, openapi_metadata
#from sanic_openapi import swagger_blueprint, doc
import sanic.response as sanic_response
#
#
import json
import os
import traceback
#
#----

'''
	https://sanic.dev/en/guide/running/running.html#using-a-factory
'''
def create ():
	USDA_food_ellipse = os.environ.get ('USDA_food')
	NIH_supp_ellipse = os.environ.get ('NIH_supp')
	inspector_port = os.environ.get ('inspector_port')
	env_vars = os.environ.copy ()
	
	#essence = os.environ.get ('essence')
	
	essence = retrieve_essence ()
	
	
	#print ("env_vars:", env_vars)
	#show_variable () 
	
	'''
		#
		#	https://sanic.dev/en/guide/running/configuration.html#inspector
		#
		INSPECTOR_PORT
	'''
	app = Sanic (__name__)
	app.extend (config = {
		"oas_url_prefix": "/docs",
		"swagger_ui_configuration": {
			"docExpansion": "list" # "none"
		}
	})
	
	#app.blueprint(swagger_blueprint)
	app.config.INSPECTOR = True
	app.config.INSPECTOR_HOST = "0.0.0.0"
	app.config.INSPECTOR_PORT = int (inspector_port)
	
	#
	#	opener
	#
	#
	#app.ext.openapi.add_security_scheme ("api_key", "apiKey")
	app.ext.openapi.add_security_scheme ("api_key", "http")
	
	front_inventory_paths = generate_inventory_paths (
		essence ["vv_turbo"] ["dist_path"]
	)
	bits_inventory_paths = generate_inventory_paths (
		essence ["bits"] ["sequences_path"]
	)

	public_addresses = sanic.Blueprint ("public", url_prefix = "/")
	bits_addresses = sanic.Blueprint ("bits", url_prefix = "/bits")
	protected_addresses = sanic.Blueprint ("protected", url_prefix = "/protected")
	

	
	@public_addresses.websocket ('/ws')
	async def address_ws_handler(request, ws):
		while True:
			data = await ws.recv ()  # Receive data from the client
			await ws.send (f"Echo: {data}")  # Send the received data back to the client

	
	@protected_addresses.get ('/goals/<region>')
	@openapi.summary ("goals")
	@openapi.description ("goals")
	async def goals_by_region (request, region):
		try:
			ingredient_doc = retrieve_one_goal ({
				"region": region
			})
			
			return sanic_response.json (ingredient_doc)
			
		except Exception as E:
			show_variable (str (E))
			
		return sanic_response.json ({
			"anomaly": "An unaccounted for anomaly occurred."
		}, status = 600)
	
	
	'''
		 https://sanic.dev/en/plugins/sanic-ext/openapi/decorators.html#ui
	'''
	@protected_addresses.patch ('/shows_v2/recipe')
	@openapi.summary ("recipe")
	@openapi.description ("""
	
		{ 
			"IDs_with_amounts": [
				{
					"DSLD_ID": "276336",
					"packets": 10
				},
				{
					"DSLD_ID": "214893",
					"packets": 20
				},
				{
					"FDC_ID": "2412474",
					"packets": 20
				}
			] 
		}
		
	""")
	@openapi.body({
		"application/json": {
			"properties": {
				"IDs_with_amounts": { "type": "list" }
			}
		}
	})
	#@doc.produces ({'message': str})
	#@doc.response (200, {"message": "Hello, {name}!"})
	async def recipe (request):
		data = request.json
	
		show_variable ({
			"data": data
		}, mode = "pprint")
	
		try:
			recipe_packet = retrieve_recipe ({
				"IDs_with_amounts": data ["IDs_with_amounts"]
			})
			if (len (recipe_packet ["not_added"]) >= 1):
				not_found_len = len (recipe_packet ["not_added"]);
				assert (type (not_found_len) == int)
			
				not_found_len = str (not_found_len)
			
				return sanic_response.json ({
					"anomaly": f"{ not_found_len } could not be found."
				}, status = 600)
			
			assert (len (recipe_packet ["not_added"]) == 0)
			
			recipe_with_goals_packet = formulate_recipe_with_goals ({
				"recipe": recipe_packet ["recipe"],
				"goal_region": "2"
			})
			
			recipe = recipe_with_goals_packet ["recipe"]	
			
			return sanic_response.json (recipe_with_goals_packet ["recipe"])
			
		except Exception as E:
			print (str (E))
			
		return sanic_response.json ({
			"anomaly": "An unaccounted for anomaly occurred."
		}, status = 600)
	
	
	vue_regions ({
		"app": app,
		"front_inventory_paths": front_inventory_paths,
		"public_addresses": public_addresses
	})
	
	addresses_bits ({
		"app": app,
		"bits_inventory_paths": bits_inventory_paths,
		"bits_addresses": bits_addresses
	})
	
	addresses_protected ({
		"app": app,
		"protected_addresses": protected_addresses
	})
	
	
	
	'''
		 https://sanic.dev/en/plugins/sanic-ext/openapi/decorators.html#ui
	'''
	besties__food_USDA__nature_v2__FDC_ID ({
		"app": app,
		"openapi": openapi,
		"USDA_food_ellipse": USDA_food_ellipse,
		"protected_addresses": protected_addresses
	})
	
	besties__supp_NIH__nature_v2__DSLD_ID ({
		"app": app,
		"openapi": openapi,
		"NIH_supp_ellipse": NIH_supp_ellipse,
		"protected_addresses": protected_addresses
	})
	
	
	app.blueprint (public_addresses)
	app.blueprint (protected_addresses)
	app.blueprint (bits_addresses)

		
	return app

