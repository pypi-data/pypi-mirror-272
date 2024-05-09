





import { append_field } from '@/apps/fields/append'

import router_link_scenery from '@/scenery/router_link/decor.vue'

import { layout_system } from '@/apps/Earth/warehouses/layout'

import mascot from '@/scenery/mascot/craft.vue'
import { open_about } from '@/parcels/about/open.js'
import { open_climate } from '@/parcels/climate/open.js'

export const decor = {
	prop: [ 'close_menu' ],
	components: {
		router_link_scenery,
		mascot
	},
	methods: {
		open_about,
		open_climate,
		
		link_clicked () {
			layout_system.moves.change_current ({ 
				location: [ 0, 0 ] 
			})
		}
	}
}

