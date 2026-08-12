import os, secrets
from flask import Flask, render_template_string, redirect, request, session, jsonify
import requests
from urllib.parse import urlencode

app=Flask(__name__)
app.secret_key=os.environ.get("FLASK_SECRET_KEY",secrets.token_hex(32))
CLIENT_KEY=os.environ.get("TIKTOK_CLIENT_KEY","")
CLIENT_SECRET=os.environ.get("TIKTOK_CLIENT_SECRET","")
REDIRECT_URI=os.environ.get("TIKTOK_REDIRECT_URI","")
HANDLE="@kaomi4239"

AUTH="https://www.tiktok.com/v2/auth/authorize/"
TOKEN="https://open.tiktokapis.com/v2/oauth/token/"
USER="https://open.tiktokapis.com/v2/user/info/"
VIDEOS="https://open.tiktokapis.com/v2/video/list/"


def load_index_template():
    """Load index.html from project root and return it as a template string.
    This keeps the existing single-file layout while allowing Flask to render
    the Jinja placeholders like {{handle}} and the configured check.
    """
    base=os.path.dirname(__file__)
    path=os.path.join(base,"index.html")
    try:
        with open(path,encoding="utf-8") as f:
            return f.read()
    except Exception:
        # Fallback minimal page if file missing
        return "<html><body><h1>K-A-O 100K GLOBAL ENGINE</h1></body></html>"

@app.get("/")
def home():
    tpl=load_index_template()
    return render_template_string(tpl,handle=HANDLE,configured=bool(CLIENT_KEY and CLIENT_SECRET and REDIRECT_URI))

@app.get("/login/tiktok")
def login():
    if not (CLIENT_KEY and CLIENT_SECRET and REDIRECT_URI):
        return redirect("/?setup=1")
    state=secrets.token_urlsafe(32)
    session["state"]=state
    q=urlencode({
        "client_key":CLIENT_KEY,
        "response_type":"code",
        "scope":"user.info.basic,video.list",
        "redirect_uri":REDIRECT_URI,
        "state":state,
        "disable_auto_auth":"1"
    })
    return redirect(AUTH+"?"+q)

@app.get("/auth/callback/")
def callback():
    if request.args.get("state")!=session.get("state"):
        return "OAuth state mismatch",400
    code=request.args.get("code")
    if not code:
        return "Authorization code missing",400
    r=requests.post(TOKEN,data={
        "client_key":CLIENT_KEY,
        "client_secret":CLIENT_SECRET,
        "code":code,
        "grant_type":"authorization_code",
        "redirect_uri":REDIRECT_URI
    },headers={"Content-Type":"application/x-www-form-urlencoded"},timeout=30)
    d=r.json()
    if not r.ok or "access_token" not in d:
        return jsonify(d),400
    session["access_token"]=d["access_token"]
    session.pop("state",None)
    return redirect("/")

def headers():
    t=session.get("access_token")
    return {"Authorization":f"Bearer {t}"} if t else None

@app.get("/api/account")
def account():
    h=headers()
    if not h:return jsonify({"connected":False}),401
    r=requests.get(USER,params={"fields":"open_id,avatar_url,display_name"},headers=h,timeout=30)
    return jsonify(r.json()),r.status_code

@app.get("/api/videos")
def videos():
    h=headers()
    if not h:return jsonify({"connected":False,"videos":[]}),401
    fields="id,title,video_description,duration,cover_image_url,share_url,create_time,like_count,comment_count,share_count,view_count"
    out=[]; cursor=None
    for _ in range(10):
        body={"max_count":20}
        if cursor:body["cursor"]=cursor
        r=requests.post(VIDEOS,params={"fields":fields},json=body,
            headers={**h,"Content-Type":"application/json"},timeout=30)
        d=r.json()
        if not r.ok:return jsonify(d),r.status_code
        data=d.get("data",{});out+=data.get("videos",[])
        if not data.get("has_more"):break
        cursor=data.get("cursor")
        if not cursor:break
    return jsonify({"connected":True,"handle":HANDLE,"videos":out})

@app.post("/api/disconnect")
def disconnect():
    session.clear();return jsonify({"ok":True})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT","5000")))
