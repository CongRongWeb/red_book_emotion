import axios from "axios";
import { Message } from "element-ui";

axios.defaults.isRetryRequest = false;

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API,
  withCredentials: true, // send cookies when cross-domain requests
  timeout: 100000,
  headers: { clientType: "app" }
});

// // 刷新token的请求方法
function getRefreshToken() {
  // refresh_token使用vuex存在本地的localstorage，之后会详细说
  const params = {
    refreshToken: sessionStorage.getItem("receipt_refreshToken")
  };
  return service.get("tb-user/refreshToken", {
    params,
    headers: { clientType: "app" }
  });
}

// request interceptor
service.interceptors.request.use(
  config => {
    config.headers["Authorization"] =
      "Bearer " + sessionStorage.getItem("receipt_accessToken");

    return config;
  },
  error => {
    // do something with request error
    console.log(error); // for debug
    return Promise.reject(error);
  }
);

// response interceptor
service.interceptors.response.use(
  response => {
    const resConfig = response.config;
    const res = response.data;
    // 判断是否已经刷新过token
    if (!resConfig.isRetryRequest) {
      if (res.code === "O_T_001") {
        Message.error(res.msg);
        // if (res.code == "O_T_001") {
        return getRefreshToken().then(res => {
          if (res.code === "M0000") {
            const data = res.data;
            console.log("重新请求");
            resConfig.isRetryRequest = true;
            sessionStorage.setItem("receipt_accessToken", data.access_token);
            sessionStorage.setItem("receipt_refreshToken", data.refresh_token);
            resConfig.headers["Authorization"] =
              "Bearer " + sessionStorage.getItem("receipt_accessToken");
            return axios(resConfig);
          } else {
            Message.error("重新请求失败");
          }
        });
      }
    } else {
      Message.error("加载超时");
      // Toast.fail('加载超时')
    }
    return res;
  },
  error => {
    // console.log(!navigator.onLine)
    // console.log(error == 'Network Error')
    if (!navigator.onLine || error.message === "Network Error") {
      Message.error("网络异常,请检查网络");
      // Toast.fail('网络异常,请检查网络')
    }
    return Promise.reject(error);
  }
);

export default service;
