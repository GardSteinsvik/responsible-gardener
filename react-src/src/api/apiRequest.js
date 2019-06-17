const BASE_URL = (window.location.hostname === 'localhost' ? 'http://localhost:3000' : '') + '/api/';

const handleStatusCodeErrors = (response) => {
    if (!response.ok) {
        throw Error(response.statusText);
    }
    return response;
}

const handleNetworkErrors = (error) => {
    console.log('Network error:', error)
}

const parseJson = (response) => {
    if (response.json) {
        return response.json()
    } else {
        return response
    }
}

export const GET = async (resourceUrl = '', customHeaders = null) => {
    const url = BASE_URL + resourceUrl;
    const headers = !customHeaders ? {
        'Accept': 'application/json',
    } : customHeaders;

    const options = {
        method: 'GET',
        headers: headers
    };

    return await fetch(url, options)
        .then(handleStatusCodeErrors)
        .then(parseJson)
        .catch(handleNetworkErrors)
}

export const POST = async (resourceUrl = '', payload = null, customHeaders = null) => {
    const url = BASE_URL + resourceUrl;
    const headers = !customHeaders ? {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    } : customHeaders;
    const body = !!payload ? (!customHeaders ? JSON.stringify(payload) : payload) : null;

    const options = {
        method: 'POST',
        headers: headers,
        body: body,
    };

    return await fetch(url, options)
        .then(handleStatusCodeErrors)
        .then(parseJson)
        .catch(handleNetworkErrors)
}