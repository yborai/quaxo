"""
A quaxo cement project
"""
import os
import sys

from cement.core.foundation import CementApp
from cement.utils.misc import init_defaults

from .configure import CONFIG_PATH, CRED_ITEMS, DEFAULTS
from .cli.controllers import __ALL__ as StubControllers

sections = tuple(zip(*CRED_ITEMS))[0] + ("log.logging",)
defaults = init_defaults(*sections)
defaults["log.logging"]["level"] = os.environ.get("ZEPHYR_DEBUG_LEVEL", "INFO")
defaults["log.colorlog"] = defaults["log.logging"]

class StubException(Exception):
    pass

class Stub(CementApp):
    class Meta:
        label = "quaxo"
        base_controller = "base"
        config_defaults = defaults
        config_files = [CONFIG_PATH]
        handlers = StubControllers
        extensions = [
            "quaxo.output",
            "colorlog",
        ]
        output_handler = "default" # See .output
        log_handler = "colorlog"

    def configure(self):
        for section, keys in CRED_ITEMS:
            for key in keys:
                env = os.environ.get(key, DEFAULTS.get(key, ""))
                if env:
                    self.config.set(section, key, env)


def main():
    with Stub() as app:
        app.configure()
        try:
            app.run()
        except StubException as e:
            message = e.args[0]
            app.log.error(message)
            sys.exit(1)


if __name__ == "__main__":
    main()
