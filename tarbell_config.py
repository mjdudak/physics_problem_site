from flask import Blueprint, render_template, g
from tarbell.hooks import register_hook

# create a blueprint for this project
# tarbell will consume this when the project loads
blueprint = Blueprint('myproject', __name__)

# -*- coding: utf-8 -*-

"""
Tarbell project configuration
"""

# Google spreadsheet key
SPREADSHEET_KEY = "1hOaTu2LuwtN9sykia2x9y0KdcZDrkhIZDweuohqlBGM"

# Exclude these files from publication
EXCLUDES = ["*.md", "requirements.txt"]

# Spreadsheet cache lifetime in seconds. (Default: 4)
# SPREADSHEET_CACHE_TTL = 4

# Create JSON data at ./data.json, disabled by default
# CREATE_JSON = True

# Get context from a local file or URL. This file can be a CSV or Excel
# spreadsheet file. Relative, absolute, and remote (http/https) paths can be 
# used.
# CONTEXT_SOURCE_FILE = ""

# EXPERIMENTAL: Path to a credentials file to authenticate with Google Drive.
# This is useful for for automated deployment. This option may be replaced by
# command line flag or environment variable. Take care not to commit or publish
# your credentials file.
# CREDENTIALS_PATH = ""

# S3 bucket configuration
#S3_BUCKETS = {
    # Provide target -> s3 url pairs, such as:
    #     "mytarget": "mys3url.bucket.url/some/path"
    # then use tarbell publish mytarget to publish to it
    
#}

# Default template variables
DEFAULT_CONTEXT = {
    'name': 'physics_problem_site',
    'title': 'Physics '
             'I '
             'Problem '
             'Site'
}

@blueprint.route("/units/<id>.html")
def unit_page(id):
    site = g.current_site
    topics = site.get_context()["unit" + id + "_topics"]
    units = site.get_context()["units"]
    return render_template("_unit_page.html", id=id, topics=topics, units=units)

@blueprint.route("/units/<id>/<topic_id>.html")
def topic_page(id, topic_id):
    site = g.current_site
    units = site.get_context()["units"]
    problems = site.get_context()["unit" + id]
    topics = site.get_context()["unit" + id + "_topics"]
    topic = [t for t in topics if t["topic_id"] == int(topic_id)][0]
    problems_relevant = []
    for p in problems:
        if p["id"]:
            if p["problem_topic"] == topic["topic"] and p["problem_level"] == topic["topic_level"]:
                problems_relevant.append(p)
    return render_template("_topic_page.html", id=id, topic=topic, problems=problems_relevant, units=units)