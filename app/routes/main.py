"""
Main routes for serving the SPA.
"""

from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Serve the main single-page application."""
    return render_template("index.html")


@main_bp.route("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Expense Tracker is running"}
