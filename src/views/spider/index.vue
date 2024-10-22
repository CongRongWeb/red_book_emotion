<template>
  <div>
    <el-row :gutter="0" style="width: 50%">
      <el-form ref="elForm2" :model="formData2"  label-width="85px" size="small">
        <el-col :span="24">
          <el-row>
            <el-col :span="24">
              <el-form-item label="链接">
                <a href="https://m.weibo.cn" target="_blank">微博</a>
              </el-form-item>
            </el-col>
          </el-row>
        </el-col>



        <el-col :span="24">
          <el-row>
            <el-col :span="24">
              <el-form-item label="Cookie" prop="cookie">
                <el-input type="textarea" v-model="formData2.cookie"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-col>

        <el-col :span="24">
          <el-row>
            <el-col :span="24">
              <el-form-item label="新闻ID" prop="news_id">
                <el-input v-model="formData2.news_id" :style="{width: '100%'}" clearable placeholder="请输入新闻ID">
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-col>
        <el-col :span="24">
          <el-row>
            <el-col :span="24">
              <el-form-item label="新闻标题" prop="news_title">
                <el-input v-model="formData2.news_title" :style="{width: '100%'}" clearable placeholder="请输入新闻标题">
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-col>
        <el-col :span="24">
          <el-form-item size="large">
            <el-button type="primary" size="small" @click="search">开始爬虫</el-button>
            <el-button @click="resetForm" size="small" >重置</el-button>
          </el-form-item>
        </el-col>
      </el-form>
    </el-row>

  </div>
</template>

<script>

import {makeSpider} from "../../api";

export default {
  name: "index",
  data(){
    return{
      formData2: {
        news_id: "",
        news_title:"",
        cookie:""
      },
    }
  },
  methods:{
    resetForm() {
      this.$refs['elForm2'].resetFields()
      this.formData2.news_id=''
      this.formData2.news_title=''
      this.formData2.cookie=''
    },
    search() {
      makeSpider(this.formData2)
    },
  }
}
</script>

<style scoped>

</style>
