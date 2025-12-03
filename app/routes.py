from flask import Blueprint, flash, redirect, render_template, request, url_for

from .models import Note, db

bp = Blueprint("main", __name__)


@bp.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        if not title or not body:
            flash("Both title and note body are required", "warning")
            return redirect(url_for("main.index"))

        note = Note(title=title, body=body)
        db.session.add(note)
        db.session.commit()
        flash("Note saved", "success")
        return redirect(url_for("main.index"))

    notes = Note.query.order_by(Note.created_at.desc()).all()
    return render_template("index.html", notes=notes)
