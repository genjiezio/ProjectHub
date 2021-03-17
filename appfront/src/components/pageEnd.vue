<template>
  <div class="pageEnd">
    <el-main>
      <el-row>
        <el-col :span="10">
          <el-row style="margin-top: 6%">
            <el-col :span="8" :push="8">
              <div class="image">
                <el-image
                  style="width: 100px; height: 100px"
                  src="../../static/sup.jpg"
                ></el-image>
                <p style="font-size: 11px">扫一扫使用小程序</p>
              </div>
            </el-col>
            <el-col :span="8" :push="8">
              <el-row style="margin-top: 12%">
                <span class="subTitle"> ProjectHub SUSTech </span>
              </el-row>
            </el-col>
          </el-row>
        </el-col>
        <el-col :span="1">
          <el-divider
            direction="vertical"
            content-position="center"
          ></el-divider>
        </el-col>

        <el-col :span="12">
          <li style="list-style-type: none; margin: 4% auto; font-size: 12px">
            <h3>ProjectHub SUSTech</h3>
            <p>前端: 陈启龙 王照伟 颜秋阳</p>
            <p>后端: 张韶丰 张昌圳</p>
            <p>联系方式: 88010110</p>
            <p>感谢访问 平安顺遂</p>
          </li>
        </el-col>
      </el-row>
    </el-main>
  </div>
</template>

<script>
export default {
  name: `pageEnd`,
  data() {
    return {
      
    };
  },
};
</script>

<style scoped>
.subTitle {
  font-size: 20px;
  line-height: 1.5;
}

.image {
  text-align: center;
}

.el-divider--vertical {
  display: inline-block;
  width: 1px;
  height: 9em;
  margin: 0 8px;
  vertical-align: middle;
  position: relative;
}
</style>
