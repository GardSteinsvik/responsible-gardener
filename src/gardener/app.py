import uasyncio
import gc
import time
from machine import ADC, Pin

from gardener.data import get_last_watered, set_last_watered, get_water_amount, set_water_amount

from gardener.web import WebApp, start_response, jsonify
webapp = WebApp()

moisture = ADC(0) # 3V3 A0
moisture_sensor_disconnected = False

pump = Pin(15, Pin.OUT) # 5V D8
pump_lock = True


@webapp.route('/', method='GET')
def index(request, response):
    yield from webapp.sendfile(response, '/index.html')


@webapp.route('/moisture', method='GET')
def moisture_resource(reqeust, response):
    moisture_value = round(((1024-moisture.read())*100/1024), 1)
    gc.collect()
    yield from start_response(response, 'text/plain')
    yield from response.awrite('soil_moisture {}'.format(moisture_value))


@webapp.route('/api/moisture', method='GET')
def moisture_resource(request, response):
    moisture_value = round(((1024-moisture.read())*100/1024), 1)
    gc.collect()
    yield from jsonify(response, {'moisture': moisture_value})


@webapp.route('/api/last-watered', method='GET')
def last_watered_resource(request, response):
    last_watered = get_last_watered()
    result = '{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z'.format(last_watered[0], last_watered[1], last_watered[2], last_watered[3], last_watered[4], last_watered[5])
    gc.collect()
    yield from jsonify(response, {'lastWatered': result})


@webapp.route('/api/water-amount', method='GET')
def water_amount_resource(request, response):
    water_amount = get_water_amount()
    gc.collect()
    yield from jsonify(response, {'waterAmount': water_amount})


@webapp.route('/pump/lock', method='POST')
def pump_command(request, response):
    print('Setting pump lock')
    global pump_lock
    pump_lock = True
    gc.collect()
    yield from jsonify(response, {'status': 200})


@webapp.route('/pump/start', method='POST')
def pump_command(request, response):
    water_amount = get_water_amount()
    print('Opening pump lock. Watering for {} seconds'.format(water_amount))
    global pump_lock
    pump_lock = False
    pump.on()
    consecutive_seconds = 0
    while consecutive_seconds < water_amount:
        consecutive_seconds = consecutive_seconds + 1
        if not pump_lock:
            await uasyncio.sleep(1)
    print('Stopping pump. Setting pump lock')
    pump.off()
    pump_lock = True
    gc.collect()
    yield from jsonify(response, {'status': 200})


@webapp.route('/last-watered/write', method='POST')
def last_watered_command(request, response):
    now = time.localtime(time.time())
    set_last_watered(now)
    gc.collect()
    yield from jsonify(response, {'status': 200})

@webapp.route('/water-amount', method='POST')
def water_amount_command(request, response):
    yield from request.read_form_data()
    water_amount = request.form['waterAmount']
    set_water_amount(water_amount)
    gc.collect()
    yield from jsonify(response, {'status': 200})


async def pump_routine():
    while True:
        last_watered = get_last_watered()
        now = time.localtime(time.time())

        print('LW: {} ~ NOW: {}'.format(last_watered[2], now[2]))

        if last_watered[2] != now[2]:
            global pump_lock
            pump_lock = False
            water_amount = get_water_amount()
            print('Water routine: Starting pump. Watering for {} seconds'.format(water_amount))
            set_last_watered(now)
            pump.on()
            consecutive_seconds = 0

            while consecutive_seconds < water_amount:
                consecutive_seconds = consecutive_seconds + 1
                if not pump_lock:
                    await uasyncio.sleep(1)

            print('Water routine: Stopping pump.')
            pump.off()
            pump_lock = True

        await uasyncio.sleep(3600)


async def check_moisture():
    while True:
        raw_value = moisture.read()
        if raw_value <= 10:
            moisture_sensor_disconnected = True
            print('REEEEE > Moisture sensor disconnected!')
        elif raw_value == 1024:
            moisture_sensor_disconnected = True
            print('REEEEE > Moisture sensor not shorted!')
        else: 
            moisture_value = round(((1024-raw_value)*100/1024), 1)
            print('Moisture: {} | {}%'.format(raw_value, moisture_value))
        await uasyncio.sleep(1)


async def set_time():
    """
    Set the time from NTP
    """
    while True:
        try:
            from ntptime import settime
            print('Setting time from NTP')
            settime()
        except Exception:
            # Ignore errors
            pass
        gc.collect()
        await uasyncio.sleep(3600)


async def check_time():
    while True:
        now = time.localtime(time.time())
        time_string = '-'.join(str(x) for x in now)
        print('Timestring', time_string)
        parsed = tuple(int(x) for x in time_string.split('-'))
        print('parsed time', parsed)
        await uasyncio.sleep(10)


def main():
    loop = uasyncio.get_event_loop()
    loop.create_task(set_time())
    loop.create_task(pump_routine())
    #loop.create_task(check_moisture())
    #loop.create_task(check_time())
    loop.create_task(uasyncio.start_server(webapp.handle, '0.0.0.0', 80))
    loop.run_forever()