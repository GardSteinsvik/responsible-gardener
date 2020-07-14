import uasyncio
import gc
import time
from machine import ADC, Pin

from gardener.data import get_last_watered, set_last_watered, get_water_amount, set_water_amount, get_pump_state, set_pump_state

from gardener.web import WebApp, start_response, jsonify
webapp = WebApp()

moisture = ADC(0)  # 3V3 A0
moisture_sensor_disconnected = False

pump = Pin(15, Pin.OUT)  # 5V D8
pump_lock = True

time_synchronized = False


@webapp.route('/', method='GET')
def index(request, response):
    yield from webapp.sendfile(response, '/index.html')


@webapp.route('/api/data', method='GET')
def data_resource(request, response):
    moisture_value = round(((1024-moisture.read())*100/1024), 1)
    last_watered_time_tuple = get_last_watered()
    last_watered = '{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z'.format(last_watered_time_tuple[0], last_watered_time_tuple[1], last_watered_time_tuple[2], last_watered_time_tuple[3], last_watered_time_tuple[4], last_watered_time_tuple[5])
    water_amount = get_water_amount()
    gc.collect()
    yield from jsonify(response, {
        'moisture': moisture_value,
        'lastWatered': last_watered,
        'waterAmount': water_amount
    })


@webapp.route('/moisture', method='GET')
def moisture_resource(reqeust, response):
    moisture_value = round(((1024-moisture.read())*100/1024), 1)
    gc.collect()
    yield from start_response(response, 'text/plain')
    yield from response.awrite('soil_moisture {}'.format(moisture_value))


@webapp.route('/pump/lock', method='POST')
def pump_command(request, response):
    global pump_lock
    pump_lock = True
    gc.collect()
    yield from jsonify(response, {'status': 200})


@webapp.route('/pump/on', method='POST')
def pump_command(request, response):
    set_pump_state('on')
    yield from jsonify(response, {'status': 200})


@webapp.route('/pump/off', method='POST')
def pump_command(request, response):
    set_pump_state('off')
    yield from jsonify(response, {'status': 200})


@webapp.route('/pump/start', method='POST')
def pump_command(request, response):
    water_amount = get_water_amount()
    #  print('Opening pump lock. Watering for {} seconds'.format(water_amount))
    global pump_lock
    pump_lock = False
    pump.on()
    consecutive_seconds = 0
    while consecutive_seconds < water_amount:
        consecutive_seconds = consecutive_seconds + 1
        if not pump_lock:
            await uasyncio.sleep(1)
    #  print('Stopping pump. Setting pump lock')
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
    yield from request.read_json_data()
    # yield from request.read_form_data()
    water_amount = request.form['waterAmount']
    set_water_amount(water_amount)
    gc.collect()
    yield from jsonify(response, {'status': 200})


async def pump_routine():
    while True:
        # print('[Water Routine] Starting.')

        will_water = True
        pump_state = get_pump_state()
        now = time.localtime(time.time())
        last_watered = get_last_watered()

        # print('[Water Routine] Last watered: {} | Time: {}'.format(last_watered[2], now[2]))

        global time_synchronized
        if not time_synchronized:
            will_water = False  # Not watering: Time is not synchronized.

        if now[3] != 12:
            will_water = False  # Not watering: It is not between 12:00 and 12:59

        if pump_state == 'off':
            will_water = False  # Not watering: Pump is turned off.

        if last_watered[2] == now[2]:
            will_water = False  # Not watering: Plant has already been watered today.

        if will_water:
            global pump_lock
            pump_lock = False
            water_amount = get_water_amount()
            # print('[Water Routine] Starting pump. Watering for {} seconds'.format(water_amount))
            set_last_watered(now)
            pump.on()
            consecutive_seconds = 0

            while consecutive_seconds < water_amount:
                consecutive_seconds = consecutive_seconds + 1
                if not pump_lock:
                    await uasyncio.sleep(1)

            # print('[Water Routine] Stopping pump.')
            pump.off()
            pump_lock = True

        await uasyncio.sleep(1800)


async def check_moisture():
    while True:
        raw_value = moisture.read()
        if raw_value <= 10:
            moisture_sensor_disconnected = True
        elif raw_value == 1024:
            moisture_sensor_disconnected = True
        else:
            moisture_value = round(((1024-raw_value)*100/1024), 1)
            # print('Moisture: {} | {}%'.format(raw_value, moisture_value))
        await uasyncio.sleep(1)


async def set_time():
    """
    Set the time from NTP
    """
    while True:
        global time_synchronized
        try:
            from ntptime import settime
            settime()
            time_synchronized = True
        except Exception:
            # Ignore errors
            time_synchronized = False
            pass
        gc.collect()
        await uasyncio.sleep(1800)


def main():
    loop = uasyncio.get_event_loop()
    loop.create_task(set_time())
    loop.create_task(pump_routine())
    # loop.create_task(check_moisture())
    loop.create_task(uasyncio.start_server(webapp.handle, '0.0.0.0', 80))
    loop.run_forever()
