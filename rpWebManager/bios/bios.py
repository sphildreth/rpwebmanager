from flask import Blueprint, render_template


bios_bp = Blueprint("bios", __name__, template_folder="templates")


@bios_bp.route("/", defaults={'page': 'bios_index'})
def index():
   return render_template("bios/bios_index.html")