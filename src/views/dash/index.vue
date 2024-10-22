<template>
<div >
  <div style="border: 1px solid black">
    <div style="font-size: 16px;font-weight: 900">
      数据概览
    </div>
    <div style="display: flex;justify-content: space-evenly">
      <div style="display: flex;padding: 50px;align-items: center">
        <div>
          <img style="width: 30px;height: 30px;padding-right: 30px" src="../../assets/img/database.png" />
        </div>
        <div style="display: flex;flex-direction: column">
          <div style="font-size: 16px">
            全部信息
          </div>
          <div style="font-size: 20px;font-weight: 500">
            {{newsIdList.length}}
          </div>
        </div>

      </div>
      <div style="display: flex;padding: 50px;align-items: center">
        <div>
          <img style="width: 30px;height: 30px;padding-right: 30px" src="../../assets/img/neg.png" />
        </div>
        <div style="display: flex;flex-direction: column">
          <div style="font-size: 16px">
            消极信息
          </div>
          <div style="font-size: 20px;font-weight: 500">
            {{negList.length}}
          </div>
        </div>

      </div>
      <div style="display: flex;padding: 50px;align-items: center">
        <div>
          <img style="width: 30px;height: 30px;padding-right: 30px" src="../../assets/img/pos.png" />
        </div>
        <div style="display: flex;flex-direction: column">
          <div style="font-size: 16px">
            积极&中性信息
          </div>
          <div style="font-size: 20px;font-weight: 500">
            {{newsIdList.length - negList.length}}
          </div>
        </div>

      </div>

    </div>
  </div>
  <div style="margin-top: 20px;border: 1px solid black">
    <div style="font-size: 16px;font-weight: 900">
      情感占比
    </div>
    <echart-dialog  :chart-data="echartsData" ></echart-dialog>
  </div>
</div>
</template>

<script>
import echartDialog from "./components";
import {getNews,getDash} from "../../api";
export default {
  name: "index",
  components:{
    echartDialog
  },
  data(){
    return{
      echartsData:[0,0,0],
      newsIdList:[],
      result:[],
      negList:[],
      middleList:[],
    }
  },
  mounted() {
    this.getNewsId()

  },
  methods:{
    getNewsId(){
      getNews({name:''}).then(res=>{
        console.log(res)
        this.newsIdList=res.data
        this.newsIdList.forEach(item=>{
          getDash({news_id: item[0]}).then(rr=>{
            this.result.push(rr.percent)
          })
        })
      })
      const that = this

      setTimeout(function (){
        that.negList = that.result.filter(i=>{return i<0.5})
        that.middleList=that.result.filter(i=>{return i==0.5})
        that.echartsData = [that.negList.length,that.middleList.length,that.result.length - that.negList.length - that.middleList.length]
      },2000)
    }
  }
}
</script>

<style scoped>

</style>
