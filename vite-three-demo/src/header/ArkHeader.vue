<template>
    <div class="header-content">
        <RouterLink to="/" underline="false">
            <h1 class="main-title">《济南府志·杂记》整理与可视化</h1>
        </RouterLink>
    </div>

</template>

<style scoped>
.header-content {
    padding: 20px;
    flex: 1;
    display: flex;
}

.main-title {
    font-family: "华文行楷", cursive;
    /* 使用华文行楷字体 */
    font-size: 32px;
    /* 设置较大的字体大小 */
    color: #8b4513;
    /* 使用棕色作为标题颜色 */
    margin: 2px;
    /* 上下留出一些间距 */
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    /* 添加文字阴影 */
    font-weight: bold;
    vertical-align: middle;
}

a {
    text-decoration: none;
}
</style>