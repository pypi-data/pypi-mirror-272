

#----
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
import sanic.response as sanic_response
#
#
from vegan._essence import retrieve_essence, build_essence
from vegan.adventures.sanique.utilities.check_key import check_key
#
#----

def addresses_staff (packet):
	staff_addresses = packet ["staff_addresses"]
	
	@staff_addresses.route ("/essence")
	@openapi.parameter ("opener", str, "header")
	async def address_essence (request):
		essence = retrieve_essence ()

		lock_status = check_key (request)
		if (lock_status != "unlocked"):
			return lock_status

		return sanic.json (essence)