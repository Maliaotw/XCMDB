// import http from '../services/http'
import request from '@/utils/request'

export function getDashBoard() {
    return request({
        url: 'api/v1/dashboard',
        method: 'get',
    })
}