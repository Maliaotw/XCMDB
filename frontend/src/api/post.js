// import http from '../services/http'
import request from '@/utils/request'

export function getPost(page,size,params) {
    return request({
        url: `/api/v1/post/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}


export function add(data) {
    return request({
        url: '/api/v1/post/',
        method: 'post',
        data
    })
}

export function del(id) {
    return request({
        url: '/api/v1/post/' + id + '/',
        method: 'delete'
    })
}

export function edit(id, data) {
    return request({
        url: '/api/v1/post/' + id + '/',
        method: 'put',
        data
    })
}