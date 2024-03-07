import Map from '../map/Map.vue';
import Scene_1 from '../story/Scene_1.vue';
import Home from '../home/Home.vue';
import Article from '../article/Article.vue';
import Reader from '../article/Reader.vue';
import { createRouter, createWebHashHistory } from 'vue-router';

const routes = [
    { path: '/', component: Home },
    { path: '/story', component: Scene_1 },
    { path: '/map', component: Map },
    { path: '/article', component: Article },
    { path: '/reader', component: Reader }
];

const router = createRouter({
    // 4. 内部提供了 history 模式的实现。为了简单起见，我们在这里使用 hash 模式。
    history: createWebHashHistory(),
    routes, // `routes: routes` 的缩写
})

export default router;