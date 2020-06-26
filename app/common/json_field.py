# https://medium.com/@philamersune/using-postgresql-jsonfield-in-sqlite-95ad4ad2e5f1
import json
from typing import Any, Dict, Optional

from django.conf import settings
from django.contrib.postgres.fields import JSONField as DjangoJSONField
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Field, Model
from django.db.models.expressions import Expression


class PostgreSQLJSONField(DjangoJSONField):
    pass


class SQLiteJSONField(Field):  # type: ignore
    def db_type(self, connection: BaseDatabaseWrapper) -> str:
        return "text"

    def from_db_value(  # type: ignore
        self,
        value: Optional[str],
        expression: Expression,  # pylint: disable=unused-argument
        connection: BaseDatabaseWrapper,  # pylint: disable=unused-argument
    ) -> Any:
        if value is not None:
            return self.to_python(value)
        return value

    def to_python(self, value: Optional[str]) -> Any:  # type: ignore
        if value is not None:
            try:
                return json.loads(value)
            except (TypeError, ValueError):
                return value
        return value

    def get_prep_value(  # type: ignore
        self, value: Optional[Dict[str, Any]]
    ) -> Optional[str]:
        if value is not None:
            return str(json.dumps(value))
        return value

    def value_to_string(self, obj: Model) -> Any:  # type: ignore
        return self.value_from_object(obj)


JSONField = (
    SQLiteJSONField
    if "sqlite" in str(settings.DATABASES["default"]["ENGINE"])
    else PostgreSQLJSONField
)
