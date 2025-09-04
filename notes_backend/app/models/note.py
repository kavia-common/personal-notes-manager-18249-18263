from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


class Note(db.Model):
    """Represents a personal note."""
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    # ISO timestamp fields
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    # Soft delete flag (optional for future use)
    archived = db.Column(db.Boolean, nullable=False, default=False, server_default="0")

    def touch(self) -> None:
        """Update the updated_at timestamp to now (UTC)."""
        self.updated_at = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"<Note id={self.id} title={self.title!r}>"
