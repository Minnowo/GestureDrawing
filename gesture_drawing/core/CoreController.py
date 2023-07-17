import logging
import traceback

from . import CoreHydrusAPI  
from . import CoreData as CD


class ClientController():

    def __init__(self) -> None:

        self._settings = {
                "hydrus" : {
                    "port": 45869,
                    "url_scheme": "https",
                    "host": "127.0.0.1",
                    "api_key" : "",
                    "verify_https": False,
                    }
                }

        self.update_hydrus()

    def get_setting(self, *args):

        setting_path = args

        if not isinstance(setting_path, tuple):

            return self._settings.get(setting_path, None)

        setting = self._settings

        for p in setting_path:

            setting = setting.get(p, None)

            if setting is None:
                return 

        return setting

    def set_setting(self, setting_path, setting_value):

        l = len(setting_path)

        setting = self._settings

        for i, p in enumerate(setting_path):

            if i + 1 == l:
                break

            if p not in setting:

                _ = {}
                setting[p] = _
                setting = _

            else:
                setting = setting[p]

        setting[setting_path[l - 1]] = setting_value

    def get_hydrus_url(self):

        scheme = self.get_setting("hydrus", "url_scheme")
        host = self.get_setting("hydrus", "host")
        port = self.get_setting("hydrus", "port")

        return f"{scheme}://{host}:{port}"

    @CoreHydrusAPI.require_hydrus_api
    def update_hydrus(self):

        api_key = self.get_setting("hydrus", "api_key")
        url = self.get_hydrus_url()
        verify = self.get_setting("hydrus", "verify_https")

        CoreHydrusAPI.get_update_client(api_key=api_key, api_url=url, verify_session=verify)


    @CoreHydrusAPI.require_hydrus_api
    def get_hydrus_api_key(self):

        api_key = CoreHydrusAPI.get_api_key()

        self.set_setting(("hydrus", "api_key"), api_key)

        return api_key


    @CoreHydrusAPI.require_hydrus_api
    def verify_hydrus_api(self):

        self.update_hydrus()

        return CoreHydrusAPI.verify_permissions()


    def boot_everything(self):

        try:
            self._is_booted = True

            CD.load_settings(self._settings)

        except Exception as e:
            trace = traceback.format_exc()

            logging.error(trace)


    def shutdown_everything(self):

        try:

            CD.save_settings(self._settings)

            self._is_booted = False

        except Exception as e:
            trace = traceback.format_exc()

            logging.error(trace)