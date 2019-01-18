from mg_app_framework import TaskKey, get_handler

MONGO_DATABASE = 'wage_settlement'


def get_target_mongo_collection(col_name):
    mongo_handler = get_handler(TaskKey.mongodb)
    db = mongo_handler[MONGO_DATABASE]
    col = db[col_name]
    return col
