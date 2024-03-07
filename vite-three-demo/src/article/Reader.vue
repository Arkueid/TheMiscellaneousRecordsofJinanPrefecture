<script setup>
import { useRoute } from "vue-router";
import axios from 'axios';
import { ref, onMounted } from "vue";


const route = useRoute();
const data = ref()
const id = route.query.id;
onMounted(() => {
    axios.get('http://localhost:8081/app1/info2/', {
        params: {
            id: id
        }
    }).then((res) => {
        data.value = res.data.hits.hits[0];
        console.log(data.value);
    })
})
</script>

<template>
    <div class="container" v-if="data">

        <div class="ancient-text">
            <div class="id">
                <div style="color: gray; font-size: 0.75rem; font-style: italic;">ID：{{ data._source.belong }}-{{
        data._id }}</div>
            </div>
            <div class="section-title">古文</div>
            <div class="original-text">
                <p>{{ data._source.src }}</p>
            </div>
            <div class="section-title">译文</div>
            <div class="translation">
                <p>{{ data._source.trans }}</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.container {
    text-align: justify;
    background-color: #f0efe2;
}

.ancient-text {
    font-family: '宋体', Arial, sans-serif;
    /* 使用传统的宋体字体 */
    padding: 20px;
    margin: 0 auto;
    /* 水平居中 */
}

.id {
    font-size: 18px;
    /* 设置编号的字体大小 */
    margin-bottom: 10px;
    /* 添加一些下方间距 */
}

.original-text,
.translation {
    font-family: '微软雅黑';
    margin-bottom: 20px;
    /* 添加一些下方间距 */
    background-color: #e9e4d3;
    padding: 10px 20px 10px 20px;
    border-radius: 15px;
}

.section-title {
    font-family: '微软雅黑';
    margin-bottom: 10px;
    font-size: 20px;
    /* 添加一些下方间距 */
    padding: 10px 20px 10px 20px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 25px;
    color: #a38843;
}

.original-text p,
.translation p {
    font-size: 16px;
    /* 设置原文和译文的字体大小 */
    line-height: 1.6;
    /* 设置行高，提高可读性 */
}
</style>