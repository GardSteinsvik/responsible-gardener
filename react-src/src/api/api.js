import {client} from './api-client'

function getData() {
    return client('api/data', {method: 'GET'})
}

function setLastWatered() {
    return client('last-watered/write', {method: 'POST'})
}

function setWaterAmount(waterAmount) {
    return client('water-amount', {
        body: {waterAmount}
    })
}

export {getData, setLastWatered, setWaterAmount};