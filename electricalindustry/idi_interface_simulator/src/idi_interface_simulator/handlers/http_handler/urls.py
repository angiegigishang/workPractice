from idi_interface_simulator.handlers.http_handler.handler import (
    SetHandler,
    ChangeStatusHandler,
    CountHandler)

url = [
    (r'/api/simulator/set/(?P<product_line>.*)', SetHandler),
    (r'/api/simulator/change_status', ChangeStatusHandler),
    (r'/api/simulator/count', CountHandler),
]
