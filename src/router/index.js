// 导入组件
import Vue from 'vue';
import Router from 'vue-router';
// 登录
import login from '@/views/login';
// 首页
import index from '@/views/index';
/**
 * 基础菜单
 */

import news from "../views/news/index"
import comment from "../views/comment/index.vue";
import spider from "../views/spider/index.vue";
import dash from "../views/dash/index.vue";

// 启用路由
Vue.use(Router);

// 导出路由
export default new Router({
    routes: [{
        path: '/',
        name: '',
        component: login,
        hidden: true,
        meta: {
            requireAuth: false
        }
    }, {
        path: '/login',
        name: '登录',
        component: login,
        hidden: true,
        meta: {
            requireAuth: false
        }
    }, {
        path: '/index',
        name: '首页',
        component: index,
        iconCls: 'el-icon-tickets',
        children: [{
            path: '/spider',
            name: '爬虫',
            component: spider,
            meta: {
                requireAuth: true
            }
        },{
            path: '/news',
            name: '新闻',
            component: news,
            meta: {
                requireAuth: true
            }
        },{
          path: '/comment',
          name: '评论',
          component: comment,
          meta: {
            requireAuth: true
          }
        },{
          path: '/dash',
          name: '首页',
          component: dash,
          meta: {
            requireAuth: true
          }
        }
        ]
    }]
})
