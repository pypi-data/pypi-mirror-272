# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class AlertClosedDetails(pydantic.BaseModel):
    alert_id: typing.Optional[str] = pydantic.Field(alias="alertId")
    status: typing.Optional[str]
    reasons: typing.Optional[typing.List[str]]
    reason_description_for_other: typing.Optional[str] = pydantic.Field(alias="reasonDescriptionForOther")
    comment: typing.Optional[str]
    user_id: typing.Optional[str] = pydantic.Field(alias="userId")
    transaction_ids: typing.Optional[typing.List[str]] = pydantic.Field(alias="transactionIds")
    rule_name: typing.Optional[str] = pydantic.Field(alias="ruleName")
    rule_description: typing.Optional[str] = pydantic.Field(alias="ruleDescription")
    rule_id: typing.Optional[str] = pydantic.Field(alias="ruleId")
    rule_instance_id: typing.Optional[str] = pydantic.Field(alias="ruleInstanceId")

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        json_encoders = {dt.datetime: serialize_datetime}
