from marshmallow import Schema, fields


class DataSchema(Schema):
    """Description of changes made by operation that triggered the event."""

    old = fields.Dict(missing=None)
    new = fields.Dict(missing=None)


class EventSchema(Schema):
    """Operation name and description."""

    session_variables = fields.Dict(keys=fields.Str(), values=fields.Str())
    op = fields.Str()
    data = fields.Nested(DataSchema)


class TriggerSchema(Schema):
    """Event trigger name."""

    name = fields.Str()


class TableSchema(Schema):
    """Database table information."""

    schema = fields.Str()
    name = fields.Str()


class DeliveryInfoSchema(Schema):
    """Event delivery information."""

    max_retries = fields.Int()
    current_retry = fields.Int()


class PayloadSchema(Schema):
    """Hasura event payload."""

    event = fields.Nested(EventSchema)
    created_at = fields.DateTime(format="iso")
    id = fields.UUID()
    trigger = fields.Nested(TriggerSchema)
    table = fields.Nested(TableSchema)
    delivery_info = fields.Nested(DeliveryInfoSchema)
