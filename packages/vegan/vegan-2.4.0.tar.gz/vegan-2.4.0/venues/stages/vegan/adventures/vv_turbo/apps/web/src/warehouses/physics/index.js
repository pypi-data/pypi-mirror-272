


/*
	server address
*/

/*
	import { physics_system } from '@/warehouses/physics'
	
	physics_system.warehouse ("server") ["address"]
*/

import { make_store } from 'mercantile'
export let physics_system;

export const create_physics_system = async function () {
	physics_system = await make_store ({
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
	
	return physics_system
}