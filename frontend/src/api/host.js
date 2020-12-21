// import http from '../services/http'
import request from '@/utils/request'

export function getHost(page,size,params) {
    return request({
        url: `/api/v1/hosts/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}

export function getNodeAll() {
    return request({
        url: `/api/v1/node/`,
        method: 'get',
    })
}

export function getHostObj(id) {
    return request({
        url: `/api/v1/hosts/${id}`,
        method: 'get',
    })
}

export function getHostRecord(page,size,params) {
    return request({
        url: `/api/v1/hostrecord/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}




export function add(data) {
    return request({
        url: '/api/v1/hosts/',
        method: 'post',
        data
    })
}

export function del(id) {
    return request({
        url: '/api/v1/hosts/' + id + '/',
        method: 'delete'
    })
}

export function edit(id, data) {
    return request({
        url: '/api/v1/hosts/' + id + '/',
        method: 'put',
        data
    })
}