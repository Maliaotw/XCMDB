// import http from '../services/http'
import request from '@/utils/request'

export function getRackunit(id) {
    return request({
        url: `/api/v1/rackunit/${id}`,
        method: 'get',
    })
}


export function add(data) {
    return request({
        url: '/api/v1/rackunit/',
        method: 'post',
        data
    })
}

export function del(id) {
    return request({
        url: '/api/v1/rackunit/' + id + '/',
        method: 'delete'
    })
}

export function edit(id, data) {
    return request({
        url: '/api/v1/rackunit/' + id + '/',
        method: 'put',
        data
    })
}