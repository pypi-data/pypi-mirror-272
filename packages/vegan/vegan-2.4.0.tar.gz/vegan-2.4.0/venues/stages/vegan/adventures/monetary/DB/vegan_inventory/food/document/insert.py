


'''
	import vegan.adventures.monetary.DB.vegan_inventory.food.document as insert_food
	insert_food ({
		"FDC_ID": "",
		"affiliates": [],
		"goodness_certifications": []
	})
'''



from vegan._essence import retrieve_essence
from vegan.adventures.monetary.DB.vegan_inventory.connect import connect_to_vegan_inventory
from vegan.besties.food_USDA.nature_v2._ops.retrieve import retrieve_parsed_USDA_food
import vegan.clouds.supp_NIH.deliveries.one as retrieve_1_supp
import vegan.clouds.supp_NIH.nature as supp_NIH_nature	
	
	
'''
	FDC_ID = "",
	affiliates = [],
	goodness_certifications = []
'''
def insert_food (packet):
	try:
		[ driver, vegan_inventory_DB ] = connect_to_vegan_inventory ()
		food_collection = vegan_inventory_DB ["food"]
	except Exception as E:
		print ("food collection connect:", E)
		
	
	try:	
		essence = retrieve_essence ()
		USDA_food_pass = essence ['USDA'] ['food']

		out_packet = retrieve_parsed_USDA_food ({
			"FDC_ID": FDC_ID,
			"USDA API Pass": USDA_food_pass
		})


		'''
			This is actually two operations.
				1. find the previous emblem
			
			Multi step insert?
		'''
		inserted = collection.insert_one ({
			'emblem': collection.find ().sort ({ 
				"emblem": -1
			}).limit (1).next () ["emblem"] + 1,
			'nature': out_packet,
			"affiliates": affiliates,
			"goodness certifications": goodness_certifications
		})
		
		inserted_document = collection.find_one ({"_id": inserted.inserted_id })
		
		print ()
		print ("inserted:", inserted_document ["emblem"])

	except Exception as E:
		raise Exception (E)
		
		#print ("exception:", E)
		pass;
		
	try:
		food_collection.disconnect ()
	except Exception as E:
		print ("food collection disconnect exception:", E)	
		
	return None;








