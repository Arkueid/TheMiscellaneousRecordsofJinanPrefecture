<script setup>
import { onMounted, reactive, ref } from 'vue';
import axios from 'axios';
import { Search } from '@element-plus/icons-vue';
import { RouterLink } from 'vue-router';

const input = ref('')
var dataList = ref([])
function fetchData(query) {
    axios.get('http://localhost:8081/app1/info/', {
        params: {
            query: query
        }
    }).then((res) => {
        dataList.value.length = 0;
        dataList.value = res.data.hits.hits;
        // console.log(dataList.value);
    })
}
onMounted(() => {
    fetchData('');
})

function handleChange(params) {
    fetchData(params);
}
</script>

<template>
    <div class="content">
        <div>
            <span style="font-size: 1.5rem; font-weight: bold; color: white;">杂记检索</span>
            <el-input v-model="input" placeholder="输入关键词" :prefix-icon="Search" @input="handleChange" />
            <span style="color: white; font-size: 0.75rem;">匹配数量：{{ dataList.length }}</span>
        </div>
        <div class="list">
            <div class="search-result-item" v-for="(item, index) in dataList" :key="item._id">
                <div v-if="item.highlight.src">
                    <div>
                        原文
                    </div>
                    <div class="search-result-item-src">
                        <div v-for="text in item.highlight.src">
                            <span v-html="text"></span>
                        </div>
                    </div>
                </div>
                <div v-if="item.highlight.trans">
                    <div>
                        译文
                    </div>
                    <div class="search-result-item-trans">
                        <div v-for="text in item.highlight.trans">
                            <span v-html="text"></span>
                        </div>
                    </div>
                </div>

                <div style="width: calc(100% - 40px); text-align: right; padding: 20px;">
                    <span class="search-result-item-info">ID：{{ item._source.belong }}-{{ item._id }}</span>

                    <RouterLink class="custom-link" :to="'/reader?id=' + item._id">查看原文</RouterLink>
                </div>
            </div>
        </div>
    </div>

</template>

<style scoped>
.content {
    background-color: #3d5168;
}
.el-input {
    width: 80%;
    padding: 20px;
    height: 90px;
    font-size: 1rem;
}

.search-result-item {
    width: calc(100% - 80px);
    background-color: white;
    border-bottom: 2px solid whitesmoke;
    padding: 10px 20px 10px 20px;
    margin: 10px 20px 10px 20px;
    text-align: justify;
}

.search-result-item-src,
.search-result-item-trans {
    background-color: whitesmoke;
    margin: 10px;
    padding: 20px;
}

.search-result-item-info {
    font-size: 0.75rem;
    color: gray;
    font-style: italic;
    margin-right: 20px;
}

.custom-link {
  color: #007bff; /* 设置链接的文本颜色为蓝色 */
  text-decoration: none; /* 给链接添加下划线 */
  cursor: pointer; /* 修改鼠标指针样式为手型 */
}

.custom-link:hover {
  color: #56a8ff; /* 在悬停时修改文本颜色为红色 */
  text-decoration: underline; /* 在悬停时添加下划线 */
}

</style>