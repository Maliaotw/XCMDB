// import http from '../services/http'
import request from '@/utils/request'

export function getBusunit(page,size,params) {
    return request({
        url: `/api/v1/busunit/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}


export function add(data) {
    return request({
        url: '/api/v1/busunit/',
        method: 'post',
        data
    })
}

export function del(id) {
    return request({
        url: '/api/v1/busunit/' + id + '/',
        method: 'delete'
    })
}

export function edit(id, data) {
    return request({
        url: '/api/v1/busunit/' + id + '/',
        method: 'put',
        data
    })
}