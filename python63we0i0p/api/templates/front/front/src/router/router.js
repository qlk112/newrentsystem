import VueRouter from 'vue-router'

//引入组件
import Index from '../pages'
import Home from '../pages/home/home'
import Login from '../pages/login/login'
import Register from '../pages/register/register'
import Center from '../pages/center/center'
import Storeup from '../pages/storeup/list'
import News from '../pages/news/news-list'
import NewsDetail from '../pages/news/news-detail'
import payList from '../pages/pay'

import yonghuList from '../pages/yonghu/list'
import yonghuDetail from '../pages/yonghu/detail'
import yonghuAdd from '../pages/yonghu/add'
import fangwuxinxiList from '../pages/fangwuxinxi/list'
import fangwuxinxiDetail from '../pages/fangwuxinxi/detail'
import fangwuxinxiAdd from '../pages/fangwuxinxi/add'
import zufangList from '../pages/zufang/list'
import zufangDetail from '../pages/zufang/detail'
import zufangAdd from '../pages/zufang/add'
import newstypeList from '../pages/newstype/list'
import newstypeDetail from '../pages/newstype/detail'
import newstypeAdd from '../pages/newstype/add'
import aboutusList from '../pages/aboutus/list'
import aboutusDetail from '../pages/aboutus/detail'
import aboutusAdd from '../pages/aboutus/add'
import systemintroList from '../pages/systemintro/list'
import systemintroDetail from '../pages/systemintro/detail'
import systemintroAdd from '../pages/systemintro/add'
import discussfangwuxinxiList from '../pages/discussfangwuxinxi/list'
import discussfangwuxinxiDetail from '../pages/discussfangwuxinxi/detail'
import discussfangwuxinxiAdd from '../pages/discussfangwuxinxi/add'

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
	return originalPush.call(this, location).catch(err => err)
}

//配置路由
export default new VueRouter({
	routes:[
		{
      path: '/',
      redirect: '/index/home'
    },
		{
			path: '/index',
			component: Index,
			children:[
				{
					path: 'home',
					component: Home
				},
				{
					path: 'center',
					component: Center,
				},
				{
					path: 'pay',
					component: payList,
				},
				{
					path: 'storeup',
					component: Storeup
				},
				{
					path: 'news',
					component: News
				},
				{
					path: 'newsDetail',
					component: NewsDetail
				},
				{
					path: 'yonghu',
					component: yonghuList
				},
				{
					path: 'yonghuDetail',
					component: yonghuDetail
				},
				{
					path: 'yonghuAdd',
					component: yonghuAdd
				},
				{
					path: 'fangwuxinxi',
					component: fangwuxinxiList
				},
				{
					path: 'fangwuxinxiDetail',
					component: fangwuxinxiDetail
				},
				{
					path: 'fangwuxinxiAdd',
					component: fangwuxinxiAdd
				},
				{
					path: 'zufang',
					component: zufangList
				},
				{
					path: 'zufangDetail',
					component: zufangDetail
				},
				{
					path: 'zufangAdd',
					component: zufangAdd
				},
				{
					path: 'newstype',
					component: newstypeList
				},
				{
					path: 'newstypeDetail',
					component: newstypeDetail
				},
				{
					path: 'newstypeAdd',
					component: newstypeAdd
				},
				{
					path: 'aboutus',
					component: aboutusList
				},
				{
					path: 'aboutusDetail',
					component: aboutusDetail
				},
				{
					path: 'aboutusAdd',
					component: aboutusAdd
				},
				{
					path: 'systemintro',
					component: systemintroList
				},
				{
					path: 'systemintroDetail',
					component: systemintroDetail
				},
				{
					path: 'systemintroAdd',
					component: systemintroAdd
				},
				{
					path: 'discussfangwuxinxi',
					component: discussfangwuxinxiList
				},
				{
					path: 'discussfangwuxinxiDetail',
					component: discussfangwuxinxiDetail
				},
				{
					path: 'discussfangwuxinxiAdd',
					component: discussfangwuxinxiAdd
				},
			]
		},
		{
			path: '/login',
			component: Login
		},
		{
			path: '/register',
			component: Register
		},
	]
})
