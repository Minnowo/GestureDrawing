import logging

try:

    import hydrus_api
    import hydrus_api.utils

    DEFAULT_URL = hydrus_api.DEFAULT_API_URL

    def _new_request_method(self, method: str, path: str, **kwargs):
        if "timeout" not in kwargs:
            kwargs["timeout"] = 3
        return self._api_request_old(method, path, **kwargs)

    hydrus_api.Client._api_request_old = hydrus_api.Client._api_request
    hydrus_api.Client._api_request = _new_request_method

    HYDRUS_API_OK = True


except ImportError as e:

    logging.warn(e)

    logging.warn("Could not import from hydrus_api, install the hydrus_api package")

    DEFAULT_URL = "http://127.0.0.1:45869"
    HYDRUS_API_OK = False


NAME = "Gesture Drawing"
REQUIRED_PERMISSIONS = (
    hydrus_api.Permission.SEARCH_FILES,
)


def require_hydrus_api(func):
    def wrapper(*args, **kwargs):
        if not HYDRUS_API_OK:
            logging.warning("This function requires the hydrus_api python package.")
        else:
            return func(*args, **kwargs)

    return wrapper

_hydrus_client = None


@require_hydrus_api
def get_client(api_key=None, api_url=DEFAULT_URL, verify_session=True) -> hydrus_api.Client:

    global _hydrus_client

    if _hydrus_client is None:
        return get_update_client(api_url=api_url,api_key=api_key,verify_session=verify_session)

    return _hydrus_client

@require_hydrus_api
def get_update_client(api_url, verify_session, api_key=None) -> hydrus_api.Client:

    global _hydrus_client

    if _hydrus_client is None:
        _hydrus_client = hydrus_api.Client(access_key=api_key,api_url=api_url)

    if api_key:
        _hydrus_client.access_key = api_key

    if api_url:
        _hydrus_client.api_url = api_url.rstrip("/")

    _hydrus_client.session.verify = verify_session

    return _hydrus_client


@require_hydrus_api
def get_api_key():


    client = get_client()

    if not client:
        return ""

    try:
        logging.info("LITERALLY ABOUT TO REQUEST PERMS")
        api_key = client.request_new_permissions(NAME, REQUIRED_PERMISSIONS)['access_key']

    except Exception as e:

        msg = str(e)

        if "permission registration dialog is not open" in msg:
            logging.warn("The hydrus permission registration dialog is not open! You must open it under 'Review Services'")
            return ""

        logging.error(e)
        return ""


    
    logging.info(f"API Key {api_key}")

    client.access_key = api_key

    return api_key


@require_hydrus_api
def verify_permissions():

    client = get_client()

    try:

        return hydrus_api.utils.verify_permissions(client,REQUIRED_PERMISSIONS)
    except Exception as e:
        logging.error(e)
        return False
