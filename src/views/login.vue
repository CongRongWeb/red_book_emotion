<template>
  <div class="login-wrap">
    <el-form label-position="left" :model="ruleForm" :rules="rules" ref="ruleForm" label-width="0px" class="demo-ruleForm login-container">
      <h3 class="title">用户登录</h3>
      <el-form-item prop="username">
        <el-input type="text" v-model="ruleForm.username" auto-complete="off" placeholder="账号"></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input type="password" v-model="ruleForm.password" auto-complete="off" placeholder="密码"></el-input>
      </el-form-item>
      <el-form-item style="width:100%;">
        <el-button type="primary" style="width:100%;" @click="submitForm('ruleForm')" :loading="logining">登录</el-button>
      </el-form-item>
    </el-form>
    <canvas id="canvas" class="login-anim"></canvas>
  </div>
</template>
<script type="text/ecmascript-6">
import {login,} from '../api/index'
import { setCookie, getCookie, delCookie } from '../utils/util'
import md5 from 'js-md5'
export default {
  name: 'login',
  data() {
    return {
      //定义loading默认为false
      logining: false,
      // 记住密码
      rememberpwd: false,
      ruleForm: {
        //username和password默认为空
        username: '',
        password: ''
      },
      //rules前端验证
      rules: {
        username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
      }
    }
  },
  // 创建完毕状态(里面是操作)
  mounted() {
    // 实现页面底部波纹特效
    sessionStorage.setItem("page","\"/static/portrait.jpg\"");
    let canvas = document.getElementById('canvas');
    let ctx = canvas.getContext('2d');
    canvas.width = canvas.parentNode.offsetWidth;
    canvas.height = canvas.parentNode.offsetHeight;

    // 如果浏览器支持requestAnimFrame则使用requestAnimFrame否则使用setTimeout
    window.requestAnimFrame = (function () {

      return window.requestAnimationFrame
        || window.webkitRequestAnimationFrame
        || window.mozRequestAnimationFrame
        || function (callback) {

          window.setTimeout(callback, 1000 / 60);
        };
    })();

    // 波浪大小
    let boHeight = 40;// canvas.height / 10;
    let posHeight = canvas.height - 150;// canvas.height / 1.2;

    // 初始角度为0
    let step = 0;
    // 定义三条不同波浪的颜色
    let lines = ["rgba(69, 159, 117, 0.1)", "rgba(95, 170, 135, 0.6)", "rgba(69, 159, 117, 0.4)"];

    function loop() {

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      step++;
      // 画3个不同颜色的矩形
      for (let j = lines.length - 1; j >= 0; j--) {

        ctx.fillStyle = lines[j];

        //每个矩形的角度都不同，每个之间相差45度
        let angle = (step + j * 70) * Math.PI / 180; // 50
        let deltaHeight = Math.sin(angle) * boHeight;
        let deltaHeightRight = Math.cos(angle) * boHeight;
        ctx.beginPath();
        ctx.moveTo(0, posHeight + deltaHeight);
        ctx.moveTo(0, posHeight + deltaHeight);
        ctx.bezierCurveTo(canvas.width / 2, posHeight + deltaHeight - boHeight, canvas.width / 2, posHeight + deltaHeightRight - boHeight, canvas.width, posHeight + deltaHeightRight);
        ctx.lineTo(canvas.width, canvas.height);
        ctx.lineTo(0, canvas.height);
        ctx.lineTo(0, posHeight + deltaHeight);
        ctx.closePath();
        ctx.fill();
      }
      requestAnimFrame(loop);
    }

    loop();
  },
  methods: {

    //获取info列表
    submitForm(formName) {
      const that =this
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.logining = true
          if(this.ruleForm.username=='admin'&&this.ruleForm.password=='admin'){
            setTimeout(function () {
              that.logining = false
              // localStorage.setItem('uuid',res.uuid)
              // that.$store.uutype=that.ruleForm.uutype
              // that.$store.uuid=res.uuid
              that.$router.push({ path: '/index' })
            },1000)
          }else{
            that.logining = false
            this.$message.error('用户名或密码错误！')
          }
        } else {
          this.$message.error('请输入用户名密码！')
          this.logining = false
          return false
        }
      })
    },
  }
}
</script>

<style scoped>
.login-wrap {
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  padding-top: 10%;
  /* background-color: #112346; */
  background-repeat: no-repeat;
  background-position: center right;
  background-size: 100%;
}
.login-container {
  border-radius: 10px;
  margin: 0px auto;
  width: 350px;
  padding: 30px 35px 15px 35px;
  background: #fff;
  border: 1px solid #eaeaea;
  text-align: left;
  box-shadow: 0 0 20px 2px rgba(0, 0, 0, 0.1);
}
.title {
  margin: 0px auto 40px auto;
  text-align: center;
  color: #505458;
}
.remember {
  margin: 0px 0px 35px 0px;
}
.code-box {
  text-align: right;
}
.codeimg {
  height: 40px;
}
.login-anim {
  position: absolute;
  bottom: 0;
  left: 0;
  z-index: -1;
}
</style>
