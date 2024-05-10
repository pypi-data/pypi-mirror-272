



/*
	import { append_field } from '@/apps/fields/append'
	await append_field ({
		field_title: "navigation",
		field: import ('@/parcels/navigation/field.vue')
	})
*/



import panel_scenery from '@/scenery/panel/decor.vue'
import hw_button from "@/scenery/hw_button/decor.vue"	

import custom_physics from "./decor/custom/decor.vue"	
import generic_physics from "./decor/generic/decor.vue"	
import references from "./decor/references/decor.vue"	

import physics from "@/parcels/physics/field.vue"	


export const decor = {
	components: { 
		physics,
		
		panel_scenery, 
		hw_button,
		
		custom_physics,
		generic_physics,
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