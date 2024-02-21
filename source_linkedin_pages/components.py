#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

from dataclasses import dataclass
from typing import Any, Mapping

from airbyte_cdk.sources.declarative.auth import DeclarativeOauth2Authenticator
from airbyte_cdk.sources.declarative.auth.declarative_authenticator import DeclarativeAuthenticator
from airbyte_cdk.sources.declarative.auth.token import BearerAuthenticator
import logging


@dataclass
class Authenticator(DeclarativeAuthenticator):
    config: Mapping[str, Any]
    bearer: BearerAuthenticator
    oauth: DeclarativeOauth2Authenticator

    def __new__(cls, bearer, oauth, config, *args, **kwargs):
        logger: logging.Logger = logging.getLogger("airbyte")
        try:
            auth_type = config.get("credentials", {}).get("auth_type")
            if auth_type == "access_token":
                return bearer
            elif auth_type == "oAuth2.0":
                return oauth
            else:
                raise Exception("Not possible configure Auth method")
        except Exception as e:
            logger.error(str(e))
