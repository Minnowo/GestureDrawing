import logging

try:

   import hydrus_api
   import hydrus_api.utils

   DEFAULT_URL = hydrus_api.DEFAULT_API_URL

   HYDRUS_API_OK = True


except ImportError as e:

    logging.warn(e)

    logging.warn("Could not import from hydrus_api, install the hydrus_api package")

    DEFAULT_URL = "http://127.0.0.1:45869"
    HYDRUS_API_OK = False




def require_hydrus_api(func):
    def wrapper(*args, **kwargs):
        if not HYDRUS_API_OK:
            logging.warning("This function requires the hydrus_api python package.")
        else:
            return func(*args, **kwargs)

    return wrapper

_hydrus_client = None


@require_hydrus_api
def get_client(api_key=None, api_url=DEFAULT_URL, verify_session=True):

    global _hydrus_client

    if _hydrus_client is None:
        return get_update_client(api_url=api_url,api_key=api_key,verify_session=verify_session)

    return _hydrus_client

@require_hydrus_api
def get_update_client(api_url, verify_session, api_key=None):

    global _hydrus_client

    if _hydrus_client is None:
        _hydrus_client = hydrus_api.Client(access_key=api_key,api_url=api_url)

    if api_key:
        _hydrus_client.access_key = api_key

    if api_url:
        _hydrus_client.api_url = api_url

    _hydrus_client.session.verify = verify_session

    return _hydrus_client


@require_hydrus_api
def get_api_key():

    NAME = "Gesture Drawing"
    REQUIRED_PERMISSIONS = (
        hydrus_api.Permission.SEARCH_FILES,
    )

    client = get_client()

    if not client:
        return ""

    api_key = client.request_new_permissions(NAME, REQUIRED_PERMISSIONS)['access_key']
    
    logging.info(f"API Key {api_key}")

    client.access_key = api_key

    return api_key

