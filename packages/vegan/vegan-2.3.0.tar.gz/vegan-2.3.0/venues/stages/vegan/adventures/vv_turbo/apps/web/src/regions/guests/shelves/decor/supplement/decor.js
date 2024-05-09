

import _get from 'lodash/get'

import { find_name } from '@/grid/struct_2/product/find_name'
import { find_stats_link } from '@/grid/struct_2/product/find_stats_link'

import s_curtain from '@/scenery/curtain/decor.vue'

import { climate } from '@/regions/guests/shelves/climate'
import router_link_scenery from '@/scenery/router_link/decor.vue'
import quantity_chooser from '@/scenery/quantity_chooser/decor.vue'


export const decor = {
	components: { s_curtain, quantity_chooser, router_link_scenery },
	props: {
		product: {
			default () {
				return {}
			},
			type: Object
		}
	},
	
	data () {
		return {
			CLIMATE: climate,
		}		
	},
	methods: {
		_get,
		find_name,
		find_stats_link
	}
}
