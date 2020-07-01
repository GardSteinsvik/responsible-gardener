const localStorageKey = '__garden_token__'

function client(endpoint, {body, ...customConfig} = {}) {

    console.log({body})

    const token = window.localStorage.getItem(localStorageKey)
    const headers = {
        'Content-Type': 'application/json',
    }

    if (token) {
        headers.Authorization = `Bearer ${token}`
    }

    const config = {
        method: body ? 'POST' : 'GET',
        ...customConfig,
        headers: {
            ...headers,
            ...customConfig.headers,
        },
    }

  if (body) {
    config.body = JSON.stringify(body)
  }

  console.log(`${process.env.REACT_APP_API_URL}/${endpoint}`, config)

  return fetch(`${process.env.REACT_APP_API_URL}/${endpoint}`, config)
    .then(async response => {
        const data = await response.json()

        if (response.ok) {
            return data
        } else {
            return Promise.reject(data)
        }
    })
}

export {client}