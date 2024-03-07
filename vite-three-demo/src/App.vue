<script setup>
import ArkHeader from './header/ArkHeader.vue';
import ArkFooter from './footer/ArkFooter.vue';
</script>

<template>
    <el-container>
        <el-header>
            <ArkHeader></ArkHeader>

        </el-header>
        <el-main>
            <div class="banner"></div>

            <router-view></router-view>

        </el-main>
        <el-footer>
            <ArkFooter></ArkFooter>

        </el-footer>
    </el-container>
    <!-- 路由出口 -->
    <!-- 路由匹配到的组件将渲染在这里 -->
</template>

<style scoped>
.el-container {
    display: flexbox;
    flex-direction: column;
}

.el-header {
    flex: 1;
    background-color: #cbd6ff;
    /* 采用黄土色作为页眉的背景色 */
    color: #fff;
    text-align: left;
    background-color: transparent;
    width: calc(70% - 20px);
    margin-left: 15%;
    flex-direction: column;
    height: 15vh;
}

.el-main {
    margin-top: 20px;
    width: calc(70% - 40px);
    margin-left: 15%;
    border: 10px solid #3d5168;
    border-top: 0px;
    padding: 0;
    margin-bottom: calc(40px);
    text-align: center;
    flex: 1;
}

.el-footer {
    bottom: 0;
    background-color: #435971;
    width: 100%;
    height: 60px;
    flex-shrink: 0;
}

.banner {
    background-image: url('/image/menu-bar.png');
    padding-top: 20px;
    padding-left: 10px;
    padding-right: 10px;
    background-size: cover;
    padding-bottom: 0;
}
</style>