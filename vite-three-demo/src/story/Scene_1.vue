<script setup>
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader';
import { RGBELoader } from 'three/examples/jsm/loaders/RGBELoader';
import { onBeforeUnmount, onMounted, ref } from 'vue';
import houseData from './data/house_data';
import * as TWEEN from '@tweenjs/tween.js'

// 字幕
const captions = ref([
    "",  // 开屏缓冲空白
    "王三公名进，是历城县蒋家庄人，受雇于长清中店，在保六都耕种",
    "美里庄的西面有石佛露了顶",
    "他便停止耕种，掘出犁，申请搬运佛像",
    "他拖车，即使佛像重一千多斤，也能轻松地搬运",
    "到村里车停滞不动了，在停下的地方建了寺庙，于是这个村为被命名为石佛屯",
    "不久遇到大旱，村里人辱骂王进",
    "王进前往庙内，割肝哀求祈祷下雨",
    "不久乌云密布，下起了大雨",
    "村民被他的诚意所感动，用石头刻了他的像放在佛陀身边",
    "村民们称赞他的行为说：\"三公说，当时金天定十一年，辛卯年，后来遇上干旱，一起祈祷就下雨了\"",
    "其他村用王进的石像巡视祈求，雨水随即降临，到现在还是这样，石佛驻扎在县的东北五十多里",
    "感谢观看!"
])
const captionIndex = ref(0);
const startPlaying = ref(false);

// 模型哈希表
const modelMap = {};
// 动作播放器
const mixers = [];
// 时钟
const clock = new THREE.Clock();

// 创建场景
var scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

var renderer = new THREE.WebGLRenderer();
renderer.setSize(
    window.innerWidth, window.innerHeight,
);
// 添加控制器
const controls = new OrbitControls(camera, renderer.domElement);
// 滑动阻尼效果
// controls.enableDamping = true;

// 添加模型
const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('./draco/');
const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(dracoLoader);

// 加载地形
gltfLoader.load('./model/terrain/terrain_1.glb', (gltf) => {
    const model = gltf.scene;
    model.position.set(0, 0, 0);
    scene.add(model);
})

// 加载天空
const rgbeLoader = new RGBELoader();
rgbeLoader.load('./env/farm_field_puresky_1k.hdr', (texture) => {
    texture.mapping = THREE.EquirectangularReflectionMapping;
    scene.background = texture;
    scene.environment = texture;
})

// 加载建筑
for (let i = 0; i < houseData.length; i++) {
    const item = houseData[i];
    gltfLoader.load(item.url, (gltf) => {
        const model = gltf.scene;
        model.scale.set(item.scale.x, item.scale.y, item.scale.z);
        model.rotation.set(item.rotation.x, item.rotation.y, item.rotation.z);
        model.position.set(item.position.x, item.position.y, item.position.z);
        scene.add(model);
    })
}

// 加载耕地1-4
const coords = [
    { x: 0, y: -0.01, z: 5 },
    { x: -0.9, y: -0.01, z: 5 },
    { x: 0, y: -0.01, z: 4.5 },
    { x: -0.9, y: -0.01, z: 4.5 },
]
for (let i = 0; i < coords.length; i++) {
    let c = coords[i];
    gltfLoader.load('./model/terrain/field_streaks.glb', (gltf) => {
        const model = gltf.scene;
        let s = 1;
        model.scale.set(s, s, s);
        model.rotation.set(0, THREE.MathUtils.degToRad(9 + 90), 0);
        model.position.set(c.x, c.y, c.z);
        scene.add(model);
    })
}

// 加载王进模型
gltfLoader.load('./model/npc/sangong.glb', (gltf) => {
    const model = gltf.scene;
    modelMap['wangjin'] = model;
    let s = 0.003;
    model.scale.set(s, s, s);
    model.rotation.set(0, -Math.PI / 3, 0);
    model.position.set(0, -0.01, 5);
    // scene.add(model);
})

// 加载犁
gltfLoader.load('./model/plough.glb', (gltf) => {
    const model = gltf.scene;
    modelMap['li'] = model;
    let s = 0.002;
    model.scale.set(s, s, s);
    model.position.set(-0.12, 0.01, 5);
    // scene.add(model);
})

// 加载佛像
gltfLoader.load('./model/little_buddhist_statue.glb', (gltf) => {
    const model = gltf.scene;
    modelMap['foxiang'] = model;
    let s = 0.1;
    model.rotation.set(0, 0, Math.PI / 4);
    model.scale.set(s, s, s);
    model.position.set(-5.2, -0.05, 5);
    // scene.add(model);
})

// 加载牛
gltfLoader.load('./model/cattle.glb', (gltf) => {
    const model = gltf.scene;
    modelMap['niu'] = model;
    let s = 0.001;
    model.scale.set(s, s, s);
    model.position.set(-0.45, 0, 5.0);
    const mixer = new THREE.AnimationMixer(model);
    const action = mixer.clipAction(gltf.animations[0]);
    mixers.push(mixer);
    action.play();
    // scene.add(model);
})

// 加载其他村民
gltfLoader.load('./model/npc/village_2.glb', (gltf) => {
    const model = gltf.scene;
    let s = 0.13;
    model.scale.set(s, s, s);
    model.rotation.set(0, THREE.MathUtils.degToRad(30), 0);
    model.position.set(-1.1, -1, 4);
    modelMap['cunmin'] = model;
    // scene.add(model);
})

// 加载推车
gltfLoader.load('./model/wooden_cart_01.glb', (gltf) => {
    const model = gltf.scene;
    let s = 0.09;
    model.position.set(0, 0, 0);
    model.rotateOnAxis(new THREE.Vector3(0, 1, 0), -THREE.MathUtils.degToRad(90));
    model.rotateOnAxis(new THREE.Vector3(1, 0, 0), -THREE.MathUtils.degToRad(35));
    model.scale.set(s, s, s);
    model.position.set(-0.5, -1.0, 4.5);
    modelMap['cart'] = model;
    // scene.add(model);
})

// 加载寺庙
gltfLoader.load('./model/building/temple_1.glb', (gltf) => {
    const model = gltf.scene;
    let s = 0.5;
    model.scale.set(s, s, s);
    model.position.set(-0.9, -4, 2.1);
    model.rotateOnAxis(new THREE.Vector3(0, 1, 0), -THREE.MathUtils.degToRad(5));
    modelMap['simiao'] = model;
    // scene.add(model);
})


// 加载枯草
let data = [
    { x: -0.5, y: -5, z: 5.1 },
    { x: 0.3, y: -5, z: 4.3 },
    { x: -0.53, y: -5, z: 4.3 },
    { x: 0.15, y: -5, z: 4.56 },
    { x: -0.65, y: -5, z: 4.56 },
    { x: 0.3, y: -5, z: 4.6 },
    { x: 0.45, y: -5, z: 4.6 },
    { x: 0.25, y: -5, z: 4.76 },
    { x: -0.85, y: -5, z: 4.76 },
    { x: 0.2, y: -5, z: 5.0 }
];
for (let i = 0; i < 10; i++) {
    let item = data[i];
    gltfLoader.load('./model/dry_grass.glb', (gltf) => {
        const model = gltf.scene;
        let s = 0.2;
        model.scale.set(s, s, s);
        model.position.set(item.x, item.y, item.z);
        // scene.add(model);
        modelMap['cao' + i] = model;
    })
}

// 加载乌云
gltfLoader.load('./model/cloud.glb', (gltf) => {
    const model = gltf.scene;
    let s = 0.16;
    model.scale.set(s, s, s);
    model.rotateOnAxis(new THREE.Vector3(1, 0, 0), THREE.MathUtils.degToRad(-90));
    model.position.set(-0.6, -5, 5);
    modelMap['yun'] = model;
    // scene.add(model);
})

// 加载寺庙2
gltfLoader.load('./model/building/temple_2.glb', (gltf) => {
    const model = gltf.scene;
    let s = 0.06;
    model.scale.set(s, s, s);
    model.rotateOnAxis(new THREE.Vector3(0, 1, 0), -THREE.MathUtils.degToRad(93));
    model.position.set(-0.9, 0.02, 2.1);
    modelMap['simiao2'] = model;
    // scene.add(model);
})

// 加载石桌
gltfLoader.load('./model/stone_table.glb', (gltf) => {
    const model = gltf.scene;
    let s = 0.03;
    model.scale.set(s, s, s);
    model.rotateOnAxis(new THREE.Vector3(0, 1, 0), THREE.MathUtils.degToRad(90))
    model.position.set(-0.64, 0.02, 2.28);
    modelMap['shizhuo'] = model;
    // scene.add(model);
})

// 加载三公像
gltfLoader.load('./model/sangong-stone.glb', (gltf) => {
    const model = gltf.scene;
    let s = 0.001;
    model.scale.set(s, s, s);
    model.position.set(-0.60, 0.05, 2.28);
    modelMap['sangongxiang'] = model;
    // scene.add(model);
})

// move 0
function move_0() {
    // 相机由远处缓缓移动到王进
    var coords = { x: 0, y: 2, z: 15 };
    return [new TWEEN.Tween(coords)
        .delay(1000)
        .to({ x: 0, y: 0.3, z: 5.5 }, 5000) // 指定目标位置和耗时.
        .easing(TWEEN.Easing.Quadratic.Out) // 指定动画效果曲线.
        .onStart(() => {
            // 设置相机焦点
            camera.lookAt(0, 0, 5);
            // 设定相机初始位置
            // 字幕归位
            captionIndex.value = 1;
        })
        .onUpdate(() => {
            // 渲染时每一帧执行：设定相机位置
            camera.position.set(coords.x, coords.y, coords.z);
        })
        .onComplete(() => {
            // 动画结束后执行
        })];
}

// move 1
function move_1() {
    // 相机移动到王进视角
    // 相机缓缓转向佛像
    return [new TWEEN.Tween({ x: 0, y: 0.3, z: 5.5, r: 0, pos_x: 0, pos_y: 0.3, pos_z: 5.5 })
        .delay(2000)
        .to({ x: -5, y: -0.1, z: 5, pos_x: 0, pos_y: 0.3, pos_z: 5, r: THREE.MathUtils.degToRad(90) }, 3000)
        .onStart(() => {
            captionIndex.value = 2;
        })
        .onUpdate((coord) => {
            camera.lookAt(coord.x, coord.y, coord.z);
            camera.rotation.set(0, coord.r, 0);
            camera.position.set(coord.pos_x, coord.pos_y, coord.pos_z);
        })
        .onComplete(() => {
            scene.add(modelMap['foxiang']);
        })];
}

function move_2() {
    return [new TWEEN.Tween({ x: 0, y: -0.01, z: 5 })
        .delay(1500)
        .to({ x: -0.6, y: -0.01, z: 4.5 }, 5000)
        .onStart(() => {
            // 初始化上一步的视角
            camera.position.set(0, 0.3, 5);
            camera.lookAt(-0.9, -0.01, 4);
            captionIndex.value = 3;
            // 来了两个村民
            // 王进走上前申请搬运佛像
            modelMap['cunmin'].position.set(-0.9, -0.01, 4);
            modelMap['wangjin'].rotation.set(0, -THREE.MathUtils.degToRad(150), 0);
            scene.add(modelMap['cunmin']);
        })
        .onUpdate((coord) => {
            modelMap['wangjin'].position.set(coord.x, coord.y, coord.z);
        })
        .onComplete(() => {

        })];
}

function move_3() {
    // 王进转身(开始拖车
    const tween_1 = new TWEEN.Tween({ r: -THREE.MathUtils.degToRad(150) })
        .delay(1000)
        .to({ r: -THREE.MathUtils.degToRad(90) }, 1000)
        .onStart(() => {
            // 衔接上一步的状态
            camera.position.set(0, 0.3, 5);
            camera.lookAt(-5, -0.1, 5);
            captionIndex.value = 3;
            modelMap['cunmin'].position.set(-0.9, -0.01, 4);
            modelMap['wangjin'].rotation.set(0, -THREE.MathUtils.degToRad(150), 0);
            modelMap['wangjin'].position.set(-0.6, 0, 4.5);
            modelMap['cart'].position.set(-0.5, 0, 4.5);
            scene.add(modelMap['cart']);
        })
        .onUpdate((coord) => {
            modelMap['wangjin'].rotation.set(0, coord.r, 0);
        })
        .onComplete(() => {
            captionIndex.value = 4;
        });
    // 王进拖车到佛像旁(-5, -0.05, 5)
    const tween_2 = new TWEEN.Tween({ x1: -0.6, y1: 0, z1: 4.5, x2: -0.5, y2: 0, z2: 4.5 })
        .to({ x1: -5.2, y1: 0, z1: 4.5, x2: -5.1, y2: 0, z2: 4.5 }, 5000)
        .onUpdate((coord) => {
            modelMap['wangjin'].position.set(coord.x1, coord.y1, coord.z1);
            modelMap['cart'].position.set(coord.x2, coord.y2, coord.z2);
            camera.position.set(coord.x2 + 0.4, 0.2, coord.z2);
        });
    // 王进推车转身
    const tween_3 = new TWEEN.Tween({ x1: THREE.MathUtils.degToRad(0), r: -THREE.MathUtils.degToRad(90) })
        .to({ x1: THREE.MathUtils.degToRad(180), r: THREE.MathUtils.degToRad(90) }, 2000)
        .onUpdate((coord) => {
            modelMap['wangjin'].rotation.set(0, coord.r, 0);
            modelMap['wangjin'].position.set(-0.1 * Math.cos(coord.x1) - 5.1, 0, 0.1 * Math.sin(coord.x1) + 4.5);
            modelMap['cart'].rotation.set(0, coord.r, 0);
            modelMap['cart'].rotateOnAxis(new THREE.Vector3(1, 0, 0), -THREE.MathUtils.degToRad(35));
        })
        .onComplete(() => {
            setTimeout(() => {
                // 佛像搬上车 
                modelMap['foxiang'].rotateOnAxis(new THREE.Vector3(0, 1, 0), -THREE.MathUtils.degToRad(90));
                modelMap['foxiang'].rotateOnAxis(new THREE.Vector3(1, 0, 0), THREE.MathUtils.degToRad(58));
                modelMap['foxiang'].position.set(-5.0, 0.012, 4.55);
            }, 1000)
        });

    // 搬运回村口处停下
    const tween_4 = new TWEEN.Tween({ x: -5.0, y: 0, z: 4.5 })
        .delay(2000)
        .to({ x: -1, y: 0, z: 3.0 }, 5000)
        .onStart(() => {
            camera.position.set(-4.8, 0.2, 5.2);
        })
        .onUpdate((coord) => {
            modelMap['wangjin'].position.set(coord.x, coord.y, coord.z);
            modelMap['cart'].position.set(coord.x - 0.1, coord.y, coord.z);
            modelMap['foxiang'].position.set(coord.x, coord.y, coord.z + 0.05);
            camera.lookAt(coord.x, coord.y, coord.z);
        })
        .onComplete(() => {
            camera.position.set(-1.2, 0.1, 3.5);
            camera.lookAt(-1, 0.31, 3.0);
            captionIndex.value += 1;
            setTimeout(() => {
                modelMap['simiao'].position.y = 0.42;
                scene.add(modelMap['simiao']);
            }, 2000);
        });
    tween_1.chain(tween_2);
    tween_2.chain(tween_3);
    tween_3.chain(tween_4);
    return [tween_1, tween_4];

}

function move_4() {
    let startCoord = { x: 2, y: 0, z: 4.0 };
    let endCoord = { x: 0.6, y: 0, z: 4.2 };
    return [new TWEEN.Tween(startCoord)
        .delay(5000)
        .to(endCoord, 4000)
        .onStart(() => {
            scene.remove(modelMap['cart']);
            scene.remove(modelMap['foxiang']);
            captionIndex.value = 6;
            // 村里遭遇大旱(作物枯死)
            modelMap['simiao'].position.y = 0.42;
            modelMap['wangjin'].rotation.set(0, Math.PI * 3 / 4, 0);
            modelMap['wangjin'].position.set(0.3, -0.01, 4.3);
            modelMap['niu'].position.y = -2;
            modelMap['li'].position.y = -2;
            camera.position.set(0.1, 0.1, 5.0);
            for (let i = 0; i < 10; i++) {
                modelMap['cao' + i].position.y = 0;
                scene.add(modelMap['cao' + i]);
            }
            // 两个村民辱骂王进(村民走来
            modelMap['cunmin'].rotation.set(0, -THREE.MathUtils.degToRad(75), 0);
        })
        .onUpdate((coord) => {
            modelMap['cunmin'].position.set(coord.x, coord.y, coord.z);
        })
        .onComplete(() => {
        })];
}

function move_5() {
    let startCoord = { x: -0.54, y: 0, z: 3.7 }
    let endCoord = { x: -0.95, y: 0, z: 2.8 }
    // 王进走向庙
    const tween_1 = new TWEEN.Tween(startCoord)
        .delay(3000)
        .to(endCoord, 5000)
        .onStart(() => {
            // 王进在庙内割肝求雨
            captionIndex.value = 7;
            camera.position.set(-1.2, 0.2, 3.5);
            camera.lookAt(-1, 0.31, 3.0);
            modelMap['simiao'].position.y = 0.42;
            modelMap['niu'].position.y = -2;
            modelMap['li'].position.y = -2;
            modelMap['wangjin'].rotation.set(0, Math.PI, 0);
        })
        .onUpdate((coord) => {
            modelMap['wangjin'].position.set(coord.x, coord.y, coord.z);
        })
        .onComplete(() => {
            setTimeout(() => {
                modelMap['wangjin'].position.set(-0.92, 0.14, 2.33);
                camera.position.set(-1.2, 0.3, 2.5);
                camera.lookAt(-0.92, 0.16, 2.0);
            })
        });
    // 王进进庙
    const tween_2 = new TWEEN.Tween({ x: -0.92, y: 0.14, z: 2.33 })
        .to({ x: -0.92, y: 0.16, z: 2.2 }, 3000)
        .onUpdate((coord) => {
            modelMap['wangjin'].position.set(coord.x, coord.y, coord.z);
        })
        .onComplete(() => {
            scene.remove(modelMap['wangjin']);
        });
    tween_1.chain(tween_2);
    // 摄像机抬起
    const tween_3 = new TWEEN.Tween({ x: -0.92, y: 0.16, z: 2.0 })
        .to({ x: -0.5, y: 1, z: 2.7 }, 5000)
        .delay(2000)
        .onUpdate((coord) => {
            camera.lookAt(coord.x, coord.y, coord.z);
            scene.add(modelMap['yun']);
        });
    // 不久天空变暗，下起大雨
    const tween_4 = new TWEEN.Tween({ x: -0.6, y: 2, z: 5 })
        .to({ x: -0.6, y: 2, z: 3.12 }, 5000)
        .onStart(() => {
            captionIndex.value = 8;
        })
        .onUpdate((coord) => {
            modelMap['yun'].position.set(coord.x, coord.y, coord.z);
        });
    tween_2.chain(tween_3);
    tween_3.chain(tween_4);
    return [tween_1, tween_4];
}

function move_6() {
    // 庙内放置石像
    const tween_1 = new TWEEN.Tween({ x: -0.67, y: 0.3, z: 4.0 })
        .delay(1500)
        .to({ x: -0.67, y: 0.14, z: 2.43 }, 5000)
        .onStart(() => {
            captionIndex.value = 8;
            scene.remove(modelMap['yun']);
            scene.remove(modelMap['simiao']);
            scene.remove(modelMap['niu']);
            scene.remove(modelMap['li']);
            for (let i = 0; i < 10; i++) {
                scene.remove(modelMap['cao' + i]);
            }
            scene.add(modelMap['simiao2']);
            scene.add(modelMap['sangongxiang']);
            scene.add(modelMap['shizhuo']);
            scene.add(modelMap['foxiang']);
            camera.position.set(-1.2, 0.2, 3.5);
            camera.lookAt(-1, 0.31, 3.0);
            modelMap['foxiang'].rotation.set(0, 0, 0);
            let s = 0.08;
            modelMap['foxiang'].scale.set(s, s, s);
            modelMap['foxiang'].position.set(-0.62, 0.058, 2.37);
            let s2 = 0.062;
            modelMap['cunmin'].scale.set(s2, s2, s2);
            modelMap['cunmin'].rotation.set(0, 0, 0);
            modelMap['cunmin'].rotateOnAxis(new THREE.Vector3(0, 1, 0), -THREE.MathUtils.degToRad(186));
            modelMap['cunmin'].position.set(-0.67, 0, 3.0);
            captionIndex.value = 9;
        })
        .onUpdate((coord) => {
            camera.position.set(coord.x, coord.y, coord.z);
            camera.lookAt(-0.60, 0.05, 2.28);
        });
    // 庙外村民讲述故事
    const tween_2 = new TWEEN.Tween({ x: -0.60, y: 0.05, z: 2.28 })
        .to({ x: -0.67, y: 0.2, z: 3.0 }, 5000)
        .delay(2000)
        .onUpdate((coord) => {
            camera.lookAt(coord.x, coord.y, coord.z);
        })
        .onComplete(() => {
            captionIndex.value = 10;
        });
    const tween_3 = new TWEEN.Tween({ x: 0 })
        .to({ x: 10 }, 7000)
        .delay(5000)
        .onStart(() => {
            captionIndex.value = 11;
        })
        .onComplete(() => {
            setTimeout(() => {
                captionIndex.value = 12;
            }, 5000);
        });
    tween_1.chain(tween_2);
    tween_2.chain(tween_3);
    return [tween_1, tween_3];
}

function play() {
    // 归位
    startPlaying.value = true;
    captionIndex.value = 0;
    camera.position.set(0, 2, 15);
    camera.lookAt(0, 0, 5);
    scene.add(modelMap['wangjin']);
    scene.add(modelMap['niu']);
    scene.add(modelMap['li']);
    let m0 = move_0();
    let m1 = move_1();
    let m2 = move_2();
    let m3 = move_3();
    let m4 = move_4();
    let m5 = move_5();
    let m6 = move_6();
    m0.at(-1).chain(m1[0]);
    m1.at(-1).chain(m2[0]);
    m2.at(-1).chain(m3[0]);
    m3.at(-1).chain(m4[0]);
    m4.at(-1).chain(m5[0]);
    m5.at(-1).chain(m6[0]);
    m0[0].start();
}

function adaptSize() {
    const root = document.getElementsByClassName('root')[0];
    if (root == undefined) return;
    // 设置摄像机视锥体的长宽比（覆盖创建相机时的长宽比）
    let width = root.clientWidth;
    let height = root.clientHeight;
    camera.aspect = width / height;
    // 更新摄像机投影矩阵。在任何参数被改变以后必须被调用。
    camera.updateProjectionMatrix();
    // 设置渲染区尺寸
    renderer.setSize(width, height);
    // 设置设备像素比
    renderer.setPixelRatio(window.devicePixelRatio);
}

var mounted = false;

function render() {
    if (!mounted) return; 
    requestAnimationFrame(render);
    TWEEN.update();
    mixers.forEach(mixer => {
        mixer.update(clock.getDelta());
    });
    renderer.clear();
    renderer.clearDepth();
    renderer.render(scene, camera);
}

onMounted(() => {
    mounted = true;
    const gallery = document.getElementById('gallery');
    gallery.appendChild(renderer.domElement);
    window.onresize = window.onresize = function () {
        adaptSize();
    };
    adaptSize();
    render();
    camera.position.set(0, 2, 15);
    camera.lookAt(0, 0, 5);
})


// 销毁示例，释放内存
onBeforeUnmount(() => {
    mounted = false;
    renderer.dispose();
    scene.children.forEach((child, idx, arr) => {
        scene.remove(child);
    })
    for (let i in modelMap) {
        delete modelMap[i];
    }
    renderer = null;
    scene = null;
})
</script>

<template>
    <div class="root">
        <div id="gallery">
            <div class="play-container" :style="{
                display: `${startPlaying.valueOf(true) ? 'none' : 'block'}`
            }">
                <h1 class="play-title" style="font-size: 3rem; font-weight: bold;">王进割肝求雨</h1>
                <button class="play-button" @click="play()">查看故事</button>
            </div>
            <div class="caption-container" :style="{
                display: `${startPlaying == true ? 'block' : 'none'}`
            }">
                <div class="caption">
                    <transition name="fade" mode="out-in">
                        <h1 class="desc" :key="captionIndex" :style="{
                fontSize: `${captionIndex == captions.length - 1 ? '3rem' : '1.5rem'}`
            }">{{ captions[captionIndex] }}</h1>
                    </transition>
                </div>
            </div>
        </div>

    </div>
</template>

<style scoped>
.root {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    height: 77vh;
    margin: 0;
    padding: 0;
    background-color: #3d5168;
}


#gallery {
    position: relative;
    padding: 0;
    margin: 0;
}

canvas {
    padding: 0;
    margin: 0;
}

.play-button {
    border: 2px solid #8B4513;
    /* 棕色 */
    background-color: #FFE4B5;
    /* 米黄色 */
    color: #8B4513;
    /* 棕色 */
    border-radius: 10px;
    cursor: pointer;
    font-size: 1.2rem;
    font-family: '楷体';
    /* 使用中文字体 */
    text-align: center;
    line-height: 50px;
    padding-left: 15px;
    padding-right: 15px;
    font-weight: bold;
}

.play-button:hover {
    background-color: #FFDAB9;
    /* 深一点的米黄色 */
}

.play-title {
    font-family: '楷体';
    /* 使用传统的宋体或微软雅黑字体 */
    font-size: 3rem;
    /* 标题的字体大小 */
    font-weight: bold;
    /* 加粗 */
    color: #000000;
    /* 标题的颜色 */
    text-align: center;
    /* 居中对齐 */
    margin-top: 20px;
    /* 顶部外边距 */
    margin-bottom: 20px;
    /* 底部外边距 */
    text-shadow: 2px 2px 5px rgb(255, 255, 255, 0.7);
    /* 添加阴影效果 */
}

/* 如果需要悬停效果，可以添加如下代码 */
.play-title:hover {
    color: #ff0000;
    /* 鼠标悬停时的颜色 */
    transition: color 0.3s ease;
    /* 平滑过渡效果 */
}

.caption-container {
    position: absolute;
    flex: 1;
    margin: 0;
    padding: 10px;
    z-index: 10;
    pointer-events: none;
    transition: all 1s;
    vertical-align: top;
    display: flex;
    width: calc(100% - 20px);
}

.caption {
    text-align: center;
    font-family: '楷体';
    margin: 0;
    padding: 0;
    color: black;
    text-shadow: 0 0 5px white;
    /* 外部黑色阴影 */
    flex: 1;
}

.play-container {
    margin: 0;
    z-index: 10;
    top: 0;
    left: 0;
    transition: all 1s;
    text-align: center;
    font-family: '楷体';
    font-size: larger;
    /* flex: 1; */
    position: absolute;
    width: 100%;
    top: 35%;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.75s ease;
}

.fade-enter,
.fade-leave-active {
    opacity: 0;
}
</style>../js/house_data./data/house_data