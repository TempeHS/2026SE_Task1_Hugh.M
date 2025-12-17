from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify
from flask import session
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging

import userManagement as dbHandler

# Code snippet for logging a message
# app.logger.critical("message")

app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

# Generate a unique basic 16 key: https://acte.ltd/utils/randomkeygen
app = Flask(__name__)
app.secret_key = b"_53oi3uriq9pifpff;apl"
csrf = CSRFProtect(app)


# Redirect index.html to domain root for consistent UX
@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)


@app.route("/", methods=["POST", "GET"])
@csp_header(
    {
        # Server Side CSP is consistent with meta CSP in layout.html
        "base-uri": "'self'",
        "default-src": "'self'",
        "style-src": "'self'",
        "script-src": "'self'",
        "img-src": "'self' data:",
        "media-src": "'self'",
        "font-src": "'self'",
        "object-src": "'self'",
        "child-src": "'self'",
        "connect-src": "'self'",
        "worker-src": "'self'",
        "report-uri": "/csp_report",
        "frame-ancestors": "'none'",
        "form-action": "'self'",
        "frame-src": "'none'",
    }
)
def index():
    return render_template("/index.html")


@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")


@app.route("/form_login.html", methods=["POST", "GET"])
def form_login():
    if request.method == "POST":
        un = request.form.get("email", "").strip()
        pwd = request.form.get("password", "")
        loggedin = dbHandler.login(un, pwd)
        if loggedin:
            session["login"] = True
            session["user"] = un
            return redirect("/index.html")
        return render_template("/form_login.html")
    else:
        return render_template("/form_login.html")


@app.route("/form_signup.html", methods=["POST", "GET"])
def form_signup():
    if request.method == "POST":
        un = request.form.get("email", "").strip()
        pwd = request.form.get("password", "")
        signedup = dbHandler.signup(un, pwd)
        if signedup:
            return redirect("/form_login.html")
        else:
            return render_template("/form_signup.html")
    else:
        return render_template("/form_signup.html")


@app.route("/logout.html", methods=["GET"])
def logout():
    session.clear()
    return redirect("/index.html")


@app.route("/form_add_devlogs.html", methods=["POST", "GET"])
def form_add_devlogs():
    if request.method == "POST":
        dev_name = request.form.get("devname", "").strip()
        proj_name = request.form.get("projname", "").strip()
        start_time = request.form.get("starttime", "").strip()
        end_time = request.form.get("endtime", "").strip()
        entry_time = request.form.get("entrydate", "").strip()
        working_time = request.form.get("timeworked", "").strip()
        repository = request.form.get("repo", "").strip()
        dev_notes = request.form.get("devnotes", "").strip()
        if dbHandler.devlogpost(
            dev_name,
            proj_name,
            start_time,
            end_time,
            entry_time,
            working_time,
            repository,
            dev_notes
        ):
            print("hello :3")
            return redirect("/developer_logs.html")
        else:
            print("devlog failed")
            return render_template("/form_add_devlogs.html")
    else:
        return render_template("/form_add_devlogs.html")


@app.route("/developer_logs.html")
def developer_logs():
    return render_template("/developer_logs.html")


# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
