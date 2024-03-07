<script setup>
import { RouterLink } from 'vue-router';
import ArkFooter from '../footer/ArkFooter.vue';
import ArkHeader from '../header/ArkHeader.vue';
</script>

<template>
  <div class="common-layout">
    <div>
      <p class="introduction" type="default">
        各地方志中，最后一卷往往是杂记（或者称为杂传、杂志、补遗、遗缀等），在杂记中记载了本地的各种于史难以稽考的神话传说、名人轶事。本项目立足于项目组感兴趣的道光《济南府志》，对这一方志中的“杂记”进行整理研究，系统梳理故事类型，通过田园调查方式，寻访故事现今的流传和遗址遗迹的留存。通过系列整理研究寻访，形成本地历史文化中的神话传说故事言说体系，丰富本地地方历史文化的挖掘和阐释。同时借助现代技术，在本地三维地图上进行三维的空间展示和线性的历时展示。展示内容包括故事原文和项目团队的现代文转化。
      </p>
    </div>
    <img class="banner-img" src="/image/banner.jpg">
    <div class="content">
      <div class="module-intro">
        <RouterLink to="/story" class="module">
          <h3>三维视角故事呈现</h3>
          <p>3D故事呈现模块利用Three.js技术，以全新的3D视角讲述传说逸闻趣事和史实。通过交互式的体验，用户可以沉浸于绚丽多彩的3D场景中，深入了解各种故事背后的历史和文化。</p>
        </RouterLink>
        <RouterLink to="/map" class="module">
          <h3>三维地图呈现</h3>
          <p>三维地图呈现模块利用Three.js技术，以全新的3D视角再现杂记中提到的地点、建筑和场景。通过交互式的体验，用户可以沉浸于栩栩如生的3D地图中，探索历史文化和地理风貌。</p>
        </RouterLink>
        <RouterLink to="/article" class="module">
          <h3>杂记检索</h3>
          <p>杂记检索模块旨在为用户提供方便的查阅方式，包括译文、原文和繁体文本。用户可以根据关键词搜索杂记内容，并在界面上轻松浏览相关条目。</p>
        </RouterLink>
      </div>
    </div>

  </div>
</template>

<style scoped>
.introduction {
  margin-left: 20px;
  color: white;
  font-size: 20px;
  background-color: #3d5168;
  line-height: 30px;
  font-family: '楷体';
  padding-bottom: 10px;
  padding-left: 20px;
  padding-right: 20px;
  padding-top: 10px;
  margin: 0;
}

.content {
  box-shadow: #666;
  background-color: white;
  padding: 20px;
  margin-top: 0;
}

.banner-img {
  object-fit: fill;
  max-height: 300px;
  width: 100%;
}

.module-intro {
  margin-top: 0;
  display: flex;
}

.module {
  margin-bottom: 30px;
  margin-right: 5px;
  margin-left: 5px;
  flex: 1;
  transition: background-color 0.3s;
  /* 添加过渡效果 */
  padding: 20px;
  border-radius: 5px;
}

.module:hover {
  background-color: #f0f0f0;
  /* 鼠标悬停时的背景颜色 */
  cursor: pointer;
  /* 鼠标样式设置为手指形状 */
}

.module h3 {
  font-size: 24px;
  margin-bottom: 10px;
  color: #8b4513;
  /* 采用棕色作为标题的颜色 */
  font-family: 'simkai';
}

.module p {
  font-size: 18px;
  color: #535353;
  line-height: 30px;
}

a {
  text-decoration: none;
}
</style>