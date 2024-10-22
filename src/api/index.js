import axios from "@/utils/request";
export function getUserList(data) {
  return axios({
    url: '/getUserList',
    method: 'post',
    data:data
  })
}


export function getNews(data) {
  return axios({
    url: '/getNews',
    method: 'post',
    data:data
  })
}

export function getComment(data) {
  return axios({
    url: '/getComment',
    method: 'post',
    data:data
  })
}

export function getCloudImgOrSave(data) {
  return axios({
    url: '/getCloudImgOrSave',
    method: 'post',
    data:data
  })
}
export function getEmotion(data) {
  return axios({
    url: '/getEmotion',
    method: 'post',
    data:data
  })
}



export function getCloudImgOrSaveAll(data) {
  return axios({
    url: '/getCloudImgOrSaveAll',
    method: 'post',
    data:data
  })
}
export function getEmotionAll(data) {
  return axios({
    url: '/getEmotionAll',
    method: 'post',
    data:data
  })
}
export function getEmotionAllComment(data) {
  return axios({
    url: '/getEmotionAllComment',
    method: 'post',
    data:data
  })
}

export function makeSpider(data) {
  return axios({
    url: '/makeSpider',
    method: 'post',
    data:data
  })
}

export function getDash(data) {
  return axios({
    url: '/getDash',
    method: 'post',
    data:data
  })
}

export function getZhu(data) {
  return axios({
    url: '/getZhu',
    method: 'post',
    data:data
  })
}















