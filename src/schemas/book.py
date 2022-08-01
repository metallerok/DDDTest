import typing
from marshmallow import fields, Schema, ValidationError
from src.models.primitives.book import BookTitle
from src.models.exc import AttributeValidationError


class BookTitleField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return BookTitle(value)
        except AttributeValidationError as e:
            raise ValidationError(e.message)
        except Exception:
            raise ValidationError("Invalid book title")

    def _serialize(self, value: BookTitle, attr: str, obj: typing.Any, **kwargs):
        if value:
            return value.title

        return None


class BookSchema(Schema):
    id = fields.String(required=True, allow_none=False, dump_only=True)
    title = BookTitleField()
