// import http from '../services/http'
import request from '@/utils/request'

export function getIDCAll() {
    return request({
        url: `/api/v1/idc/`,
        method: 'get',
    })
}



export function getIDC(page=0,size,params) {
    return request({
        url: `/api/v1/idc/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}

export function getDetail(id) {
    return request({
        url: `/api/v1/idc/${id}`,
        method: 'get',
    })
}

export function add(data) {
    return request({
        url: '/api/v1/idc/',
        method: 'post',
        data
    })
}

export function del(id) {
    return request({
        url: '/api/v1/idc/' + id + '/',
        method: 'delete'
    })
}

export function edit(id, data) {
    return request({
        url: '/api/v1/idc/' + id + '/',
        method: 'put',
        data
    })
}