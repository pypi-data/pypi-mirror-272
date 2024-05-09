


/*
	server address
*/

/*
	import { climate_system } from '@/warehouses/climate'
	
	climate_system.warehouse ("server") ["address"]
*/

import { make_store } from 'mercantile'
export let climate_system;

export const create_climate_system = async function () {
	climate_system = await make_store ({
		warehouse: async function () {				
			return {
				layout: {
					lines: "3px"
				},
				server: {
					address: "http://127.0.0.1:48938",
					
				}
			}
		},
		moves: {},
		once_at: {
			async start () {}
		}			
	})
	
	return climate_system
}