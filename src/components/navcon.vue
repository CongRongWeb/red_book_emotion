/**
* 头部菜单
*/
<template>
  <div>
  <el-dialog
    title="修改密码"
    :visible.sync="dialogVisible"
    width="30%"
    :before-close="handleClose">
    <el-form ref="form" :model="form" label-width="80px">

      <el-form-item label="旧密码">
        <el-input v-model="form.oldPwd"   placeholder="请输入旧密码"></el-input>
      </el-form-item>
      <el-form-item label="新密码">
        <el-input v-model="form.newPwd"   placeholder="请输入新密码"></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">修改</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>

  <el-menu class="el-menu-demo" mode="horizontal" background-color="#334157" text-color="#fff" active-text-color="#fff">
    <el-button class="buttonimg">
      <img class="showimg" :src="collapsed?imgsq:imgshow" @click="toggle(collapsed)">
    </el-button>
    <el-submenu index="2" class="submenu">
      <!-- <template slot="title">{{user.userRealName}}</template> -->
      <template slot="title">管理员</template>
<!--      <el-menu-item @click="changePwd()" index="2-2">修改密码</el-menu-item>-->
      <el-menu-item @click="exit()" index="2-3">退出</el-menu-item>
    </el-submenu>
  </el-menu>

  </div>
</template>
<script>
//import {changePassword} from '../api/index'
export default {
  name: 'navcon',
  data() {
    return {
      collapsed: true,
      dialogVisible:false,
      form:{
        oldPwd:'',
        newPwd:''
      },
      imgshow: require('../assets/img/show.png'),
      imgsq: require('../assets/img/sq.png'),
      user: {}
    }
  },
  // 创建完毕状态(里面是操作)
  created() {
    this.user = JSON.parse(localStorage.getItem('userdata'))
  },
  methods: {
    onSubmit(){
      const DATA={
        oldPwd:this.form.oldPwd,
        newPwd:this.form.newPwd,
        uuid:this.$store.uuid
      }
      // changePassword(DATA).then(res=>{
      //   console.log(res,'asdadadasdas')
      //   if(res.success===0){
      //     const DATAA={
      //       uuid:this.$store.uuid,
      //       opAbs:'修改密码',
      //       opType:'3'
      //     }
      //     this.$message({
      //       type: 'success',
      //       message: '修改密码成功！'
      //     })
      //     this.$router.replace('/')
      //   }else{
      //     this.$message({
      //       type: 'error',
      //       message: '密码错误，修改失败！'
      //     })
      //   }
      // })
    },
    getuuType(val){
      switch (val) {
        case '0':
          return'管理员'
        case '1':
          return '医生'
        case '3':
          return '药房'

      }
    },
    // 退出登录
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done();
        })
        .catch(_ => {});
    },
    changePwd(){
      this.dialogVisible=true

    },
    exit() {
      this.$confirm('退出登录, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          setTimeout(() => {
            this.$store.commit('logout', 'false')
            this.$router.push({ path: '/login' })
            this.$message({
              type: 'success',
              message: '已退出登录!'
            })
          }, 1000)
          // loginout()
          //   .then(res => {
          //     if (res.success) {
          //       //如果请求成功就让他2秒跳转路由
          //       setTimeout(() => {
          //         this.$store.commit('logout', 'false')
          //         this.$router.push({ path: '/login' })
          //         this.$message({
          //           type: 'success',
          //           message: '已退出登录!'
          //         })
          //       }, 1000)
          //     } else {
          //       this.$message.error(res.msg)
          //       this.logining = false
          //       return false
          //     }
          //   })
          //   .catch(err => {
          //     // 获取图形验证码
          //     this.getcode()
          //     this.logining = false
          //     this.$message.error('退出失败，请稍后再试！')
          //   })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          })
        })
    },
    // 切换显示
    toggle(showtype) {
      this.collapsed = !showtype
      this.$root.Bus.$emit('toggle', this.collapsed)
    }
  }
}
</script>
<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  border: none;
}
.submenu {
  float: right;
}
.buttonimg {
  height: 60px;
  background-color: transparent;
  border: none;
}
.showimg {
  width: 26px;
  height: 26px;
  position: absolute;
  top: 17px;
  left: 17px;
}
.showimg:active {
  border: none;
}
</style>
