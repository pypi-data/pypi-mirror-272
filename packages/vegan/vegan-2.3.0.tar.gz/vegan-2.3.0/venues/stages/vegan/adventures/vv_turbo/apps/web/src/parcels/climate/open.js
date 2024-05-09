
/*
	import { open_climate } from '@/parcels/climate/open.js'
*/

import { append_field } from '@/apps/fields/append'

export async function open_climate () {
	await append_field ({
		field_title: "climate",
		field: import ('@/parcels/climate/field.vue')
	})
}