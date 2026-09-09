<template>
  <el-container class="layout">
    <!-- 顶栏：品牌 + 导航 -->
    <el-header class="header">
      <div class="brand">🍅 FocusStudy</div>
      <el-menu mode="horizontal" :default-active="activeMenu" router class="nav">
        <el-menu-item index="/tasks">
          <el-icon><List /></el-icon>
          <span>任务管理</span>
        </el-menu-item>
        <el-menu-item index="/timer">
          <el-icon><Timer /></el-icon>
          <span>专注计时</span>
        </el-menu-item>
        <el-menu-item index="/stats">
          <el-icon><DataAnalysis /></el-icon>
          <span>数据统计</span>
        </el-menu-item>
      </el-menu>
    </el-header>

    <!-- 内容区 -->
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const activeMenu = computed(() => route.path);
</script>

<style>
.layout { min-height: 100vh; }
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-bottom: 1px solid #eee;
}
.brand {
  font-size: 22px;
  font-weight: 700;
  color: #ff6b35;
  letter-spacing: 1px;
}
.nav { border-bottom: none !important; }
.el-main { padding: 24px; }
</style>
