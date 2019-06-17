import gc
import uasyncio
from machine import ADC

from gardener.web import WebApp, start_response, jsonify
webapp = WebApp()

moisture = ADC(0)


@webapp.route('/', method='GET')
def index(request, response):
    gc.collect()
    yield from webapp.sendfile(response, '/index.html')


@webapp.route('/moisture', method='GET')
def moisture_resource(request, response):
    moisture_value = round(((1024-moisture.read())*100/1024), 1)
    yield from start_response(response, 'text/plain')
    yield from response.awrite('soil_moisture {}'.format(moisture_value))


@webapp.route('/api/moisture', method='GET')
def moisture_resource(request, response):
    moisture_value = round(((1024-moisture.read())*100/1024), 1)
    yield from jsonify(response, {'moisture': moisture_value})

async def check_moisture():
    while True:
        moisture_value = round(((1024-moisture.read())*100/1024), 1)
        print('Moisture: {} | {}%'.format(moisture.read(), moisture_value))
        await uasyncio.sleep(10)


def main():
    loop = uasyncio.get_event_loop()
    loop.create_task(check_moisture())
    loop.create_task(uasyncio.start_server(webapp.handle, '0.0.0.0', 80))
    loop.run_forever()