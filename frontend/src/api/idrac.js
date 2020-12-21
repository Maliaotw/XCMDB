// import http from '../services/http'
import request from '@/utils/request'


export function getIdracObj(id) {
    return request({
        url: `/api/v1/idrac/${id}`,
        method: 'get',
    })
}


export function getIdrac(page,size,params) {
    return request({
        url: `/api/v1/idrac/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}



export function getidracs(page,size,params) {
    return request({
        url: `/api/v1/idrac/status`,
        method: 'get',
        params
    })
}


export function add(data) {
    return request({
        url: '/api/v1/idrac/',
        method: 'post',
        data
    })
}

export function del(id) {
    return request({
        url: '/api/v1/idrac/' + id + '/',
        method: 'delete'
    })
}

export function edit(id, data) {
    return request({
        url: '/api/v1/idrac/' + id + '/',
        method: 'put',
        data
    })
}
