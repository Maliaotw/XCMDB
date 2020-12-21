// import http from '../services/http'
import request from '@/utils/request'

export function getComment(page,size) {
    return request({
        url: `/api/v1/comment/?offset=${page}&limit=${size}`,
        method: 'get',
    })
}


export function add(data) {
    return request({
        url: '/api/v1/comment/',
        method: 'post',
        data
    })
}

export function del(id) {
    return request({
        url: '/api/v1/comment/' + id + '/',
        method: 'delete'
    })
}

export function edit(id, data) {
    return request({
        url: '/api/v1/comment/' + id + '/',
        method: 'put',
        data
    })
}