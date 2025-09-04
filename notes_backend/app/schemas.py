from marshmallow import Schema, fields, validate, EXCLUDE


class PaginationQuerySchema(Schema):
    """Query params for paginated list endpoints."""
    class Meta:
        unknown = EXCLUDE

    page = fields.Integer(load_default=1, metadata={"description": "Page number (1-based)."})
    per_page = fields.Integer(
        load_default=10,
        validate=validate.Range(min=1, max=100),
        metadata={"description": "Items per page (1-100)."},
    )
    q = fields.String(load_default=None, allow_none=True, metadata={"description": "Free-text search in title/content."})
    archived = fields.Boolean(
        load_default=None,
        allow_none=True,
        metadata={"description": "Filter by archived flag. Omit for both."}
    )


class NoteBaseSchema(Schema):
    """Base fields for a note."""
    title = fields.String(required=True, validate=validate.Length(min=1, max=255))
    content = fields.String(required=True)


class NoteCreateSchema(NoteBaseSchema):
    """Schema for creating a note."""
    pass


class NoteUpdateSchema(Schema):
    """Schema for updating a note (PUT/PATCH)."""
    title = fields.String(validate=validate.Length(min=1, max=255))
    content = fields.String()
    archived = fields.Boolean()


class NoteSchema(NoteBaseSchema):
    """Schema for returning a note."""
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    archived = fields.Boolean(dump_only=False, load_default=False)


class NotesListSchema(Schema):
    """Schema for returning a list of notes with pagination metadata."""
    items = fields.List(fields.Nested(NoteSchema))
    total = fields.Integer()
    page = fields.Integer()
    per_page = fields.Integer()
    pages = fields.Integer()
