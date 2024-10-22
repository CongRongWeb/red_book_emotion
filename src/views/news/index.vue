<template>
  <div>
    <div>
      <el-row :gutter="0">
        <el-form ref="elForm2" :model="formData2"  label-width="85px" size="small">
          <el-col :span="6">
            <el-row>
              <el-col :span="24">
                <el-form-item label="新闻标题" prop="name">
                  <el-input v-model="formData2.name" :style="{width: '100%'}" clearable placeholder="请输入新闻标题">
                  </el-input>
                </el-form-item>
              </el-col>
            </el-row>
          </el-col>
          <el-col :span="6">
            <el-form-item size="large">
              <el-button type="primary" size="small" @click="search">搜索</el-button>
              <el-button @click="resetForm" size="small" >重置</el-button>
            </el-form-item>
          </el-col>
        </el-form>
      </el-row>

    </div>

    <div class="container">
      <el-table
        stripe
        border
        :data="tableData"
        style="width: 100%">
        <el-table-column
          prop="1"
          label="新闻标题"
          align="center">
        </el-table-column>
        <el-table-column
          label="词云"
          align="center"
          width="280">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="primary"
              plain
              @click="getCiyun( scope.row)">查看详情</el-button>
          </template>
        </el-table-column>
        <el-table-column
          width="200"
          align="center"
          label="情感分析">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="primary"
              plain
              @click="getEmotions( scope.row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div style="display: flex;flex-direction: row-reverse;padding: 40px 0">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="page"
        :page-sizes="[10,20,30]"
        background
        :page-size="limit"
        layout="total, sizes, prev, pager, next"
        :total="total"
      >
      </el-pagination>

    </div>
    <el-dialog
      title="词云"
      :visible.sync="addDialog"
      width="50%"
    >
      <div style="width: 100%;display: flex;align-items: center;justify-content: center">
        <img :src="imgSrc" style="width:700px;height: 700px" />
      </div>
      <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="addDialog = false">关 闭</el-button>
  </span>
    </el-dialog>

    <el-dialog
      title="情绪分析"
      :visible.sync="emotionDialog"
      width="50%"
    >
      <div style="width: 100%;display: flex;align-items: center;justify-content: center;flex-direction: column">
        <echart-dialog v-if="emotionDialog" :chart-data="echartsData" ></echart-dialog>
        <echart-second  v-if="emotionDialog" :chart-data="echartsData2"  ></echart-second>
      </div>
      <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="emotionDialog = false;">关 闭</el-button>
  </span>
    </el-dialog>
  </div>
</template>

<script>
import {getCloudImgOrSaveAll, getEmotionAll, getEmotionAllComment, getNews,getZhu} from "../../api/index"
import echartDialog from "./components";
import echartSecond from "./components/echartSecond.vue";

export default {
  name: "index",
  components:{
    echartDialog,
    echartSecond
  },
  data() {
    return {
      addDialog: false,
      emotionDialog:false,
      formData2: {
        name: ""
      },
      tableData: [],
      disabled:false,
      tableList:[],
      page:1,
      total:0,
      limit:10,
      imgSrc:'',
      echartsData:[],
      echartsData2:[],
      percent:0
    }
  },
  mounted() {
    this.refreshView()
  },
  methods: {
    //处理切换页码
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
      this.limit = val;
      this.pageList();
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.page = val;
      this.pageList();
    },

    // 具体分页操作
    pageList() {
      this.tableData = this.tableList.filter(
        (item, index) =>
          index < this.page * this.limit &&
          index >= this.limit * (this.page - 1)
      );
      this.total = this.tableList.length;
    },
    refreshView(){
      const DATA={
        name:this.formData2.name
      }
      getNews(DATA).then(res=>{
        this.tableData=res.data
        this.tableList=res.data
        this.total=res.data.length;
        this.pageList()
      })
    },

    resetForm() {
      this.$refs['elForm2'].resetFields()
      this.formData2.name=''
      this.refreshView()

    },
    search() {
      this.refreshView()
    },
    getCiyun(data) {
      getCloudImgOrSaveAll({news_id:data[0]}).then(res=>{
        if(res.flag){
          this.addDialog=true
          this.imgSrc=res.imgurl
        }
      })


    },
    getEmotions(data) {
      const that = this
      getEmotionAll({news_id:data[0]}).then(res=>{
        this.echartsData=[]
        res.data.forEach((item,index)=>{
          this.echartsData.push({date:item[0],percent:0})
          getEmotionAllComment({created_at:item[0],news_id:data[0]}).then(ress=>{
            this.echartsData[index].percent = (ress.percent*100).toFixed(2)
          })
        })
        getZhu({news_id:data[0]}).then(res=>{
          this.echartsData2=res.result
        })
        setTimeout(function (){
          that.emotionDialog=true
        },2000)

      })
    }
  }
}
</script>

<style scoped>

</style>
