<script setup>
import * as Cesium from "cesium";
import "cesium/Build/Cesium/Widgets/widgets.css";
import { onMounted } from "vue";
import ACCESS_TOKEN from './js/token.js';

const style = `
font-size: 1rem;
font-family: '宋体';
margin: 0;
padding: 15px;
text-align: justify;
`;

function addAreaLabel(viewer, url) {
    Cesium.GeoJsonDataSource.load(url).then(function (dataSource) {
        viewer.dataSources.add(dataSource);
        var entities = dataSource.entities.values;
        for (var i = 0; i < entities.length; i++) {
            var entity = entities[i];
            var color = Cesium.Color.fromRandom({ alpha: 0.3 });
            entity.polygon.outline = true;
            entity.polygon.outlineColor = Cesium.Color.fromCssColorString('#6dcdeb');
            entity.polygon.outlineWidth = 20;
            entity.polygon.material = color;
            // entity.polygon.fill = false;

            // 添加标签
            var polyPositions = entity.polygon.hierarchy.getValue(Cesium.JulianDate.now()).positions;
            // 根据坐标集合构造BoundingSphere获取中心点坐标
            var polyCenter = Cesium.BoundingSphere.fromPoints(polyPositions).center;
            // 将中心点拉回到地球表面
            polyCenter = Cesium.Ellipsoid.WGS84.scaleToGeodeticSurface(polyCenter);
            viewer.entities.add({
                position: polyCenter,
                label: {
                    font: '24px 宋体',
                    text: entity.properties.name,
                    showBackground: true,
                    scale: 0.6,
                    horizontalOrigin: Cesium.HorizontalOrigin.CENTER,
                    verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
                }
            })
        }
    });

}

onMounted(async () => {
    Cesium.Ion.defaultAccessToken = ACCESS_TOKEN;
    // 创建 Cesium 场景

    const viewer = new Cesium.Viewer('cesiumContainer', {
        terrainProvider: await Cesium.CesiumTerrainProvider.fromUrl('./terrain/shandong/'),
        geocoder: true,
        homeButton: false,
        sceneModePicker: true,
        baseLayerPicker: false,
        navigationHelpButton: false,
        animation: false,
        timeline: false,
        fullscreenButton: false,
        vrButton: false,
    });

    viewer.scene.globe.enableLighting = true;
    viewer.scene.primitives.add(new Cesium.CloudCollection({
        noiseDetail: 16.0,
        noiseOffset: Cesium.Cartesian3.ZERO,
    }))
    viewer.scene.globe.depthTestAgainstTerrain = false;
    viewer.scene.skyAtmosphere.show = false; //关闭大气层阴影

    viewer.scene.skyBox.show = false; //去掉天空盒子
    viewer.scene.backgroundColor = new Cesium.Color(0, 0, 0, 0); //设置场景背景色透明，便于显示自定的背景
    viewer.scene.globe.baseColor = new Cesium.Color(0, 0, 0, 0); //修改地邱球体背景透明

    // addAreaLabel(viewer, './geojson/shandong.json');
    addAreaLabel(viewer, './geojson/济南市.json');
    addAreaLabel(viewer, './geojson/德州市.json');
    addAreaLabel(viewer, './geojson/滨州市.json');
    addAreaLabel(viewer, './geojson/淄博市.json');
    addAreaLabel(viewer, './geojson/泰安市.json');


    Cesium.GeoJsonDataSource.load('./geojson/jinanfu.json').then(function (dataSource) {
        viewer.dataSources.add(dataSource);
        var entities = dataSource.entities.values;
        var entity = entities[0];
        // // 构造随机颜色
        entity.polygon.outline = true;
        entity.polygon.outlineColor = Cesium.Color.YELLOW;
        entity.polygon.outlineWidth = 10;
        // 添加标签
        var polyPositions = entity.polygon.hierarchy.getValue(Cesium.JulianDate.now()).positions;
        // 根据坐标集合构造BoundingSphere获取中心点坐标
        var polyCenter = Cesium.BoundingSphere.fromPoints(polyPositions).center;
        // 将中心点拉回到地球表面
        polyCenter = Cesium.Ellipsoid.WGS84.scaleToGeodeticSurface(polyCenter);
        viewer.entities.add({
            position: polyCenter,
            label: {
                font: '24px sans-serif',
                text: '清代济南府',
                showBackground: true,
                scale: 0.6,
                horizontalOrigin: Cesium.HorizontalOrigin.CENTER,
                verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
                backgroundColor: Cesium.Color.YELLOW,
                fillColor: Cesium.Color.BLACK,
            },
            description: "<div class='wow'>早上好</div>"
        });
        viewer.flyTo(entity);
    });

    Cesium.GeoJsonDataSource.load('./geojson/story-1.json').then(function (dataSource) {
        // viewer.dataSources.add(dataSource);
        var entities = dataSource.entities.values;
        var entity = entities[0];
        for (var i = 0; i < entities.length; i++) {
            var entity = entities[i];
            viewer.entities.add({
                position: Cesium.Cartesian3.fromDegrees(entity.properties.longitude._value, entity.properties.latitude._value),
                label: {
                    font: '24px 宋体',
                    text: entity.properties.relative_story,
                    showBackground: true,
                    backgroundColor: Cesium.Color.fromCssColorString("#ff9000"),
                    scale: 0.6,
                    horizontalOrigin: Cesium.HorizontalOrigin.CENTER,
                    fillColor: Cesium.Color.fromCssColorString("#ffffff"),
                    verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
                },
                description: `<div class="description" style="${style}">
                    <div style="width: 100%; text-align: 'center'; font-family: '宋体'; font-weight: bold; font-size: 1.1rem; padding: 5px;">${entity.properties.relative_story}</div>
                    ${entity.properties.detail}
                    </div>`,
                billboard: {
                    image: '/image/mark.png',
                    width: 30,
                    height: 30
                }
            })
        }
    });
})

</script>

<template>
    <div id="cesiumContainer"></div>
</template>

<style scoped>
canvas {
    height: 80vh;
}
</style>