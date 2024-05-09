
/*
	priorities:
		add food?


*/


var chassis_company = "/@1/"

export const company_routes = [
	{
		name: 'company',
		path: chassis_company,
		component: () => import ('@/regions/company/habitat/decor.vue')
	}
]