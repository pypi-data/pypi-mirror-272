"""Marshmallow Schema for AssistantCommand."""
from marshmallow import Schema, fields


class WorkbookBlockResourceSchema(Schema):
    """Class for AssistantCommandResource schema"""

    id = fields.Integer(dump_only=True)
    workbook_id = fields.Integer(required=True)
    sequence_number = fields.Integer(required=True)
    block_type = fields.String(required=True)
    block_data = fields.String(allow_none=True)
    is_deleted = fields.Boolean(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
