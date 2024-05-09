

import { append_field } from '@/apps/fields/append'

import router_link_scenery from '@/scenery/router_link/decor.vue'
import mural from '@/scenery/name/mural.vue'

import s_button from '@/scenery/button/decor.vue'
	
import mascot from '@/scenery/mascot/craft.vue'
import { open_about } from '@/parcels/about/open.js'

// import vanta from 'vanta'
import JParticles from 'jparticles'

export const field = {
	components: {
		mascot,
		s_button,
		mural,
		router_link_scenery
	},
	
	props: [
		'open_options'
	],

	data () {
		return {	
			focused: false
		}
	},
	created () {},
	
	beforeUnmount () {		
		const element = this.$refs.nav;
		element.removeEventListener ('focus', this.focus)
		element.removeEventListener ('blur', this.blur)
	},
	mounted () {
		const element = this.$refs.nav;
		element.addEventListener ('focus', this.focus)
		element.addEventListener ('blur', this.blur)
		
		const canvas = this.$refs.canvas;
		new JParticles.Particle (canvas, {
			range: 0,
			num: 0.1,
			minSpeed: 0.01,
			maxSpeed: 0.05,
			minR: 0.2,
			maxR: 1.2,
		})
		
	},
	
	methods: {
		open_about,
		
		focus (event) {
			this.focused = true;
		},
		blur (event) {
			this.focused = false;
		}
	}
}