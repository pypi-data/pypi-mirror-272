


import { RouterLink } 	from 'vue-router'

import { append_field } from '@/apps/fields/append'
import { open_climate } from '@/parcels/climate/open.js'

	
import mobile_top_nav from './navs/mobile_top/field.vue'
import top_nav from './navs/top/field.vue'


export const decor = {
	props: [ "open_menu" ],
	components: {		
		mobile_top_nav,
		top_nav,
		RouterLink
	},
	methods: {
		async open_options () {			
			await open_climate ()
		}
	},
	
	data () {
		return {	
			focused: false
		}
	}
}