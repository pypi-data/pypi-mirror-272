







<script>

import { decor } from './decor.js'
export default decor

</script>


<template v-slot="slotProps" v-slot:default="slotProps">
	<lounge #default="{ palette, terrain }">
		<div
			:style="{
				padding: '.2in',
				maxWidth: '1000px',
				margin: '0 auto'
			}"
		>
			<!-- <header
				:style="{ textAlign: 'center' }"
			>
				<h1>moves</h1>
			</header> -->
			<div :style="{ height: '20px' }" />


			<custom_climate 
				:style="{
					padding: '.25in'
				}"
			/>
			<div :style="{ height: '20px' }" />
			
			
			
			<generic_climate 
				:style="{
					padding: '.25in'
				}"
			/>
			<div :style="{ height: '20px' }" />
		</div>
	</lounge>
</template>
