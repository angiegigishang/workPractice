from wage_settlement.handlers.http_handler.handler import (
    WebHandler, MaterielGroupPriceHandler, WageDetailHandler,
    TimelyWageHandler
)

url = [
    (r'/http_url', WebHandler),
    (r'/api/wage_settlement/process_materiel_price_mapper', MaterielGroupPriceHandler),
    (r'/api/wage_settlement/timely_wage_mapper', TimelyWageHandler),
    (r'/api/wage_settlement/wage_detail', WageDetailHandler)
]
