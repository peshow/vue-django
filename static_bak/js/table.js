<div id="app">
<template>
  <el-table :data="tableData" border>
  <el-table-column prop="date" label="日期" width="180">
  </el-table-column>
  <el-table-column prop="email" label="邮箱" width="180">
  </el-table-column>
  <el-table-column prop="address" label="地址" width="180">
  </el-table-column>
  </el-table>
  <router-view></router-view>
</template>
</div>
<script>
  var Main = {
    data() {
      return {
        tableData: [{
          date: '2016-05-02',
          email: '526399002@qq.com',
          address: '上海普陀区1518弄'
        }]
      }
    }
  }
  var Ctor = Vue.extend(Main)
  new Ctor().$mount('#app')
</script>