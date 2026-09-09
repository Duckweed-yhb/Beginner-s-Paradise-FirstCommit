<template>
  <div ref="chartRef" class="base-chart"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import * as echarts from "echarts";

// 可复用 ECharts 组件：父组件传入 option 即可（第 12 课）
const props = defineProps({
  option: { type: Object, required: true },
});

const chartRef = ref(null);
let chart = null;

function doResize() {
  chart && chart.resize();
}

onMounted(() => {
  chart = echarts.init(chartRef.value);
  chart.setOption(props.option);
  window.addEventListener("resize", doResize);
});

watch(
  () => props.option,
  (newOption) => {
    chart && chart.setOption(newOption, true);
  },
  { deep: true }
);

onUnmounted(() => {
  window.removeEventListener("resize", doResize);
  chart && chart.dispose();
});
</script>

<style scoped>
.base-chart {
  width: 100%;
  height: 320px;
}
</style>
