// import http from '../services/http'
import request from '@/utils/request'

export function getTdAll() {
    return request({
        url: `/api/v1/td/`,
        method: 'get',
    })
}



export function getTd(page=0,size,params) {
    return request({
        url: `/api/v1/td/?offset=${page}&limit=${size}`,
        method: 'get',
        params
    })
}

export function getTdObj(id) {
    return request({
        url: `/api/v1/td/${id}`,
        method: 'get',
    })
}
