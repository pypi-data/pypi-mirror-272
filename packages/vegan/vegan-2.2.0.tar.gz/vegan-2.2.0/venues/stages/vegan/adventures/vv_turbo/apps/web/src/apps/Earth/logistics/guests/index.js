

import { createRouter, createWebHistory } from 'vue-router'

import habitat from '@/regions/guests/habitat/decor.vue'

var chassis_s1 = "/@@/"
var chassis = "/@/"

export const guests_routes = [
	{
		name: 'habitat',
		path: '/',
		component: habitat
	},
	{
		name: 'shelves',
		path: chassis + 'shelves',
		component: () => import ('@/regions/guests/shelves/decor.vue')
	},
	{
		name: 'help',
		path: chassis + 'help',
		component: () => import ('@/parcels/help/decor.vue')
	},

	{
		name: 'food',
		path: chassis + 'food/:emblem',
		component: () => import ('@/regions/guests/food/decor.vue')
	},
	{
		name: 'supp',
		path: chassis + 'supp/:emblem',
		component: () => import ('@/regions/guests/supp/decor.vue')
	},	
	
	//--
	//
	//	customs
	//
	{
		name: 'goal',
		path: chassis + 'goal',
		component: () => import ('@/regions/guests/goal/room.vue'),
		children: []
	},
	{
		name: 'grocery list',
		path: chassis + 'grocery-list',
		component: () => import ('@/regions/guests/cart/decor.vue'),
		children: []
	},
	
	//--
	
	{
		name: 'recipes',
		path: chassis_s1 + 'recipes',
		component: () => import ('@/regions/guests/recipes/decor.vue')
	},	
	{
		name: 'map',
		path: chassis + 'map',
		component: () => import ('@/regions/guests/map/decor.vue')
	},
	
	//--
	
	{
		name: 'navigation lab',
		path: chassis_s1 + 'navigation-lab',
		component: () => import ('@/parcels/navigation-lab/field.vue')
	},
	{
		name: 'comparisons',
		path: chassis_s1 + 'comparisons',
		component: () => import ('@/regions/guests/comparisons/region.vue')
	},
	
	//--
	
	{
		name: 'emblem',
		path: chassis_s1 + 'emblem',
		component: () => import ('@/regions/guests/emblem/decor.vue')
	},	
]