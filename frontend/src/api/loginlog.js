// import http from '../services/http'
import request from '@/utils/request'

const name = "loginlog";

export function getAll(page=0,size,params) {
    return request({
        url: `/api/v1/${name}/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}



export function getObj(id) {
    return request({
        url: `/api/v1/${name}/${id}`,
        method: 'get',
    })
}
