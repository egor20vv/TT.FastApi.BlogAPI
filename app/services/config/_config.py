from ._config_utils import (Field, config_repr, config_sub)


@config_repr
class Configs:
    @config_sub
    class JWT:
        SECRET_KEY = Field()
        ALGORITHM = Field()
        DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = Field()
        DEFAULT_REFRASH_TOKEN_EXPIRE_MINUTES = Field()
    
    @config_sub
    class NEO4J:
        @config_sub(config_name='DEFAULT')
        class DEFAULT:
            URI = Field()
            DBNAME = Field()
            USER = Field()
            PASS = Field()
            
        @config_sub(config_name='TEST')
        class TEST:
            URI = Field()
            DBNAME = Field()
            USER = Field()
            PASS = Field('PASS')
            