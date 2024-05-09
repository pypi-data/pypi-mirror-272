

/*
	import { search_treasures } from '@/fleet/vegan_DB/treasures/search'
	const { 
		status,
		parsed,
		proceeds
	} = await search_treasures ({ 
		freight: {
			"filters": {
				"string": "lentils",
				"include": {
					"food": true,
					"supp": true
				},
				"limit": 10
			}
		}
	})
	if (status !== 200) { 
		
	}
	
*/

import { climate_system } from '@/warehouses/climate'
import { lap } from '@/fleet/syllabus/lap'	
	
export const search_treasures = async ({
	freight
}) => {
	console.log ('starting search treasures', freight)

	return await lap ({
		envelope: {
			"label": "search treasures",
			"freight": freight
		}
	});
}