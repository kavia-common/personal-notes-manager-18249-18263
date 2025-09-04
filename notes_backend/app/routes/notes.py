from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_

from ..models.note import db, Note
from ..schemas import (
    NoteCreateSchema,
    NoteSchema,
    NoteUpdateSchema,
    NotesListSchema,
    PaginationQuerySchema,
)

# Blueprint for Notes APIs
blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/notes",
    description="CRUD operations for personal notes",
)


@blp.route("")
class NotesCollection(MethodView):
    """Endpoints for listing and creating notes."""

    @blp.arguments(PaginationQuerySchema, location="query")
    @blp.response(200, NotesListSchema)
    def get(self, args):
        # PUBLIC_INTERFACE
        """List notes with optional pagination and search.

        Query Parameters:
        - page: integer, page number starting from 1 (default 1)
        - per_page: integer, items per page (default 10, max 100)
        - q: string, optional search term looked up in title and content
        - archived: boolean, optional filter by archived flag

        Returns:
        - JSON object with items, total, page, per_page, and pages
        """
        page = args.get("page", 1)
        per_page = args.get("per_page", 10)
        q = args.get("q")
        archived = args.get("archived")

        query = Note.query
        if archived is not None:
            query = query.filter(Note.archived.is_(archived))
        if q:
            ilike_term = f"%{q}%"
            query = query.filter(or_(Note.title.ilike(ilike_term), Note.content.ilike(ilike_term)))

        pagination = query.order_by(Note.updated_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
        return {
            "items": pagination.items,
            "total": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": pagination.pages,
        }

    @blp.arguments(NoteCreateSchema)
    @blp.response(201, NoteSchema)
    def post(self, payload):
        # PUBLIC_INTERFACE
        """Create a new note.

        Request Body (application/json):
        - title: string (1..255), required
        - content: string, required

        Returns:
        - Created note object with id and timestamps.
        """
        note = Note(title=payload["title"], content=payload["content"])
        db.session.add(note)
        db.session.commit()
        return note


@blp.route("/<int:note_id>")
class NoteItem(MethodView):
    """Endpoints for retrieving, updating, and deleting a note."""

    @blp.response(200, NoteSchema)
    def get(self, note_id: int):
        # PUBLIC_INTERFACE
        """Retrieve a single note by ID.

        Path Parameters:
        - note_id: integer

        Returns:
        - Note object if found; 404 otherwise.
        """
        note = Note.query.get(note_id)
        if not note:
            abort(404, message="Note not found")
        return note

    @blp.arguments(NoteUpdateSchema)
    @blp.response(200, NoteSchema)
    def put(self, payload, note_id: int):
        # PUBLIC_INTERFACE
        """Replace fields of an existing note.

        Path Parameters:
        - note_id: integer

        Request Body:
        - title: string (optional)
        - content: string (optional)
        - archived: boolean (optional)

        Returns:
        - Updated note object; 404 if not found.
        """
        note = Note.query.get(note_id)
        if not note:
            abort(404, message="Note not found")

        # Replace/Upsert only provided fields
        if "title" in payload:
            note.title = payload["title"]
        if "content" in payload:
            note.content = payload["content"]
        if "archived" in payload:
            note.archived = bool(payload["archived"])

        note.touch()
        db.session.commit()
        return note

    @blp.arguments(NoteUpdateSchema, location="json")
    @blp.response(200, NoteSchema)
    def patch(self, payload, note_id: int):
        # PUBLIC_INTERFACE
        """Partially update an existing note.

        Path Parameters:
        - note_id: integer

        Request Body:
        - Any subset of: title, content, archived

        Returns:
        - Updated note object; 404 if not found.
        """
        note = Note.query.get(note_id)
        if not note:
            abort(404, message="Note not found")

        updated = False
        if "title" in payload:
            note.title = payload["title"]
            updated = True
        if "content" in payload:
            note.content = payload["content"]
            updated = True
        if "archived" in payload:
            note.archived = bool(payload["archived"])
            updated = True

        if updated:
            note.touch()
            db.session.commit()
        return note

    @blp.response(204)
    def delete(self, note_id: int):
        # PUBLIC_INTERFACE
        """Delete a note by ID.

        Path Parameters:
        - note_id: integer

        Returns:
        - 204 No Content on success; 404 if not found.
        """
        note = Note.query.get(note_id)
        if not note:
            abort(404, message="Note not found")
        db.session.delete(note)
        db.session.commit()
        return ""
