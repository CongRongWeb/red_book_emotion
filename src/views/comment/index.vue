<template>
  <div>
    <div>
      <el-row :gutter="0">
        <el-form ref="elForm2" :model="formData2"  label-width="85px" size="small">
          <el-col :span="6">
            <el-row>
              <el-col :span="24">
                <el-form-item label="笔记标题" prop="news_title">
                  <el-input v-model="formData2.news_title" :style="{width: '100%'}" clearable placeholder="请输入笔记标题">
                  </el-input>
                </el-form-item>
              </el-col>
            </el-row>
          </el-col>
          <el-col :span="6">
            <el-row>
              <el-col :span="24">
                <el-form-item label="作者名称" prop="comment">
                  <el-input v-model="formData2.comment" :style="{width: '100%'}" clearable placeholder="请输入作者名称">
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
          label="笔记标题"
          align="center">
        </el-table-column>
        <el-table-column
          prop="4"
          label="作者名称"
          align="center">
        </el-table-column>

        <el-table-column
          prop="6"
          label="笔记链接"
          :show-overflow-tooltip="true"
          align="center">
          <template slot-scope="scope">
            <a :href="scope.row[6]" target="_blank">
              {{scope.row[6]}}
            </a>
          </template>
        </el-table-column>
        <el-table-column
          prop="7"
          label="编辑时间"
          align="center">
        </el-table-column>
<!--        <el-table-column
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
        </el-table-column>-->
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
        <img :src="imgSrc" style="width: 400px;height: 400px" />
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
        <div style="width: 100%;display: flex">
          <span style="width: 12%;text-align: right">积极度</span>
          <span style="width: 80%">
            <el-progress :text-inside="true" :stroke-width="24" :percentage="percent" status="success"></el-progress>
          </span>
        </div>

      </div>
      <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="emotionDialog = false;">关 闭</el-button>
  </span>
    </el-dialog>

  </div>
</template>

<script>
import {getComment,getCloudImgOrSave,getEmotion} from "../../api/index"
import echartDialog from "./components/echartDialog.vue";
export default {
  name: "index",
  components:{
    echartDialog
  },
  data() {
    return {
      addDialog: false,
      emotionDialog:false,
      formData2: {
        comment: "",
        news_title:""
      },
      tableData: [],
      disabled:false,
      tableList:[],
      page:1,
      total:0,
      limit:10,
      imgSrc:'',
      echartsData:[],
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
        news_title:this.formData2.news_title,
        comment:this.formData2.comment
      }
      getComment(DATA).then(res=>{
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
      getCloudImgOrSave({comment:data[4]}).then(res=>{
        if(res.flag){
          this.addDialog=true
          this.imgSrc=res.imgurl

        }
      })


    },
    getEmotions(data) {
      getEmotion({comment:data[4]}).then(res=>{
        this.echartsData[0]=res.result1['乐']
        this.echartsData[1]=res.result1['哀']
        this.echartsData[2]=res.result1['好']
        this.echartsData[3]=res.result1['怒']
        this.echartsData[4]=res.result1['恶']
        this.echartsData[5]=res.result1['惊']
        this.echartsData[6]=res.result1['惧']
        this.percent= (res.pos / res.result1['words']) * 100
        this.percent=Number(this.percent.toFixed(0))
        this.emotionDialog=true

      })
    }
  }
}
</script>

<style scoped>

</style>
