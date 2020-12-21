// import http from '../services/http'
import request from '@/utils/request'


export function getISP(page=0,size,params) {
    return request({
        url: `/api/v1/isp/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}


export function getISPObj(id) {
    return request({
        url: `/api/v1/isp/${id}`,
        method: 'get',
    })
}



export function add(data) {
    return request({
        url: '/api/v1/isp/',
        method: 'post',
        data
    })
}

export function del(id) {
    return request({
        url: '/api/v1/isp/' + id + '/',
        method: 'delete'
    })
}

export function edit(id, data) {
    return request({
        url: '/api/v1/isp/' + id + '/',
        method: 'put',
        data
    })
}