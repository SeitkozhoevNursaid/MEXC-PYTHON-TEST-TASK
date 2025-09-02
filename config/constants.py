from decouple import config


MASTER_ACCOUNT = {
    "api_key": config("MASTER_ACCOUNT_API_KEY"),
    "api_secret": config("MASTER_ACCOUNT_API_SECRET"),
}


COPIER_ACCOUNTS = [
    {
        "api_key": config("COPIER1_API_KEY"),
    },
    {
        "api_key": config("COPIER2_API_KEY"),
    }
]


CREATE_ORDER_URL = 'https://futures.mexc.com/api/v1/private/order/create'
