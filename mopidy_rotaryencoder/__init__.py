import logging
import os
from mopidy import config, ext

__version__ = '0.1.2'

logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = 'Mopidy-RotaryEncoder'
    ext_name = 'rotaryencoder'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['datapin'] = config.Integer()
        schema['volume_delta'] = config.Integer()
        schema['clkpin'] = config.Integer()
        schema['swpin'] = config.Integer()
        return schema

    def setup(self, registry):
        from .frontend import RotaryEncoderFrontend
        registry.add('frontend', RotaryEncoderFrontend)
