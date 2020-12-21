// import http from '../services/http'
import request from '@/utils/request'


export function getTagAll() {
    return request({
        url: `/api/v1/tag/`,
        method: 'get',
    })
}


export function getTag(page=0,size,params) {
    return request({
        url: `/api/v1/tag/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}

export function add(data) {
    return request({
        url: '/api/v1/tag/',
        method: 'post',
        data
    })
}

export function del(id) {
    return request({
        url: '/api/v1/tag/' + id + '/',
        method: 'delete'
    })
}

export function edit(id, data) {
    return request({
        url: '/api/v1/tag/' + id + '/',
        method: 'put',
        data
    })
}