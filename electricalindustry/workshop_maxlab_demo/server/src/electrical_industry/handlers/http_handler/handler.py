from mg_app_framework import HttpBasicHandler, MesCode


class WebHandler(HttpBasicHandler):
    async def get_process(self):
        num_data = {}
        self.send_response_data(MesCode.success, num_data, 'success get data')

    async def post_process(self):
        num_data = {}
        self.send_response_data(MesCode.success, num_data, 'success post data')

