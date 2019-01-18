from production_line_monitor.handlers.websocket_handler.handler import WebHandler

url = [
    (r'/monitor/websocket_url', WebHandler),
]
