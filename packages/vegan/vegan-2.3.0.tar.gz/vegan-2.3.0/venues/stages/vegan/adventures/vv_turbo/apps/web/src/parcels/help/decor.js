



/*
	import { append_field } from '@/apps/fields/append'
	await append_field ({
		field_title: "navigation",
		field: import ('@/parcels/navigation/field.vue')
	})
*/



import panel_scenery from '@/scenery/panel/decor.vue'
import hw_button from "@/scenery/hw_button/decor.vue"	

import custom_climate from "./decor/custom/decor.vue"	
import generic_climate from "./decor/generic/decor.vue"	
import references from "./decor/references/decor.vue"	

export const decor = {
	components: { 
		panel_scenery, 
		hw_button,
		
		custom_climate,
		generic_climate,
		references
	},
	

	methods: {},
	
	
	
	props: {},
	data () {
		return {}
	},
	created () {},
	beforeMount () {},
	mounted () {},
	beforeUnmount () {}
}