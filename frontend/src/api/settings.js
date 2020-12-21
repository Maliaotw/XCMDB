// import http from '../services/http'
import request from '@/utils/request'

export function getSeeingsObj(name) {
    return request({
        url: `/api/v1/settings/${name}`,
        method: 'get',
    })
}



export function UpdateSeeingsObj(name,data) {
    return request({
        url: `/api/v1/settings/${name}`,
        method: 'post',
        data
    })
}
