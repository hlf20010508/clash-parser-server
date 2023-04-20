from clash_parser import Clash_Parser
from parsers import rules, proxy_groups, in_group_proxies
from flask import Flask, request, send_file, make_response
from io import BytesIO

app = Flask(__name__)

# http://example.com/?url=https://your_proxy.com/...
@app.route("/", methods=["GET"])
def index():
    url = request.args.get("url")

    client = Clash_Parser(url)
    client.prepend_rules(rules)
    client.append_proxy_groups(proxy_groups)
    client.set_proxies_in_group(in_group_proxies)
    profile = client.dump_profile()

    profile_io = BytesIO(profile.encode())

    response = make_response(
        send_file(profile_io, as_attachment=True, download_name="clash.yaml")
    )
    response.headers["Subscription-Userinfo"] = client.headers["Subscription-Userinfo"]
    response.headers["Content-Disposition"] = client.headers['Content-Disposition']
    response.headers["Content-Type"] = client.headers["Content-Type"]
    response.headers["Cache-Control"] = client.headers["Cache-Control"]
    return response
