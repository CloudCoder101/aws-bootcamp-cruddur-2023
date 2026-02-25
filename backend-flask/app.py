from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from services.show_activity import ShowActivity
import os

import watchtower
import logging
from time import strftime

# ----------------------------
# Honeycomb / OpenTelemetry imports
# ----------------------------
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# ----------------------------
# Rollbar imports
# ----------------------------
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

# ----------------------------
# AWS X-Ray imports
# ----------------------------
#from aws_xray_sdk.core import xray_recorder
#from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# ----------------------------
# Local service imports
# ----------------------------
from services.home_activities import *
from services.db import get_conn
#from aws_xray_sdk.core import xray_recorder
#from aws_xray_sdk.ext.flask.middleware import XRayMiddlewarefrom services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *

# ----------------------------
# Flask App Initialization
# ----------------------------
app = Flask(__name__)

# ============================================================
# Honeycomb / OpenTelemetry Setup
# ============================================================
provider = TracerProvider()
otlp_exporter = OTLPSpanExporter(
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"),
    headers={
        "x-honeycomb-team": os.getenv("HONEYCOMB_API_KEY"),
        "x-honeycomb-dataset": os.getenv("HONEYCOMB_DATASET"),
    }
)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(provider)

# Instrument Flask + outgoing HTTP requests
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# ============================================================
# Rollbar Setup
# ============================================================
rollbar_access_token = os.getenv("ROLLBAR_ACCESS_TOKEN")

if rollbar_access_token:
    rollbar.init(
        access_token=rollbar_access_token,
        environment="development",
        root=os.path.dirname(os.path.realpath(__file__)),
    )
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

# ============================================================
# AWS X-Ray Setup
# ============================================================
#xray_url = os.getenv("AWS_XRAY_URL")
#xray_recorder.configure(service='Cruddur', dynamic_naming=xray_url)
#XRayMiddleware(app, xray_recorder)

# ============================================================
# CloudWatch Logging Setup
# ============================================================
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()

#cw_handler = watchtower.CloudWatchLogHandler(log_group='Cruddur')
#LOGGER.addHandler(console_handler)
#LOGGER.addHandler(cw_handler)
#LOGGER.info("CloudWatch logging initialized")

LOGGER.addHandler(console_handler)

# CloudWatch logging (optional: requires AWS creds)
try:
    #cw_handler = watchtower.CloudWatchLogHandler(log_group='Cruddur')
    #LOGGER.addHandler(cw_handler)
    LOGGER.info("CloudWatch logging initialized")
except Exception as e:
    LOGGER.warning(f"CloudWatch logging disabled (no AWS creds?): {e}")

# ============================================================
# CORS Setup
# ============================================================

frontend = os.getenv('FRONTEND_URL', 'http://localhost:3000')
backend = os.getenv('BACKEND_URL', 'http://localhost:4567')
origins = [frontend, backend]
cors = CORS(
    app,
    resources={r"/api/*": {"origins": origins}},
    expose_headers="location,link",
    allow_headers="content-type,if-modified-since",
    methods="OPTIONS,GET,HEAD,POST"
)

# ============================================================
# Routes
# ============================================================

@app.route("/api/health-check")
def health_check():
    return {"success": True}, 200

@app.route("/rollbar/test")
def rollbar_test():
    raise Exception("Rollbar backend test: intentional exception")

@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():
    user_handle = 'andrewbrown'
    model = MessageGroups.run(user_handle=user_handle)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200


@app.route("/api/messages/@<string:handle>", methods=['GET'])
def data_messages(handle):
    user_sender_handle = 'andrewbrown'
    user_receiver_handle = request.args.get('user_reciever_handle')
    model = Messages.run(user_sender_handle=user_sender_handle, user_receiver_handle=user_receiver_handle)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200


@app.route("/api/messages", methods=['POST', 'OPTIONS'])
@cross_origin()
def data_create_message():
    user_sender_handle = 'andrewbrown'
    user_receiver_handle = request.json['user_receiver_handle']
    message = request.json['message']
    model = CreateMessage.run(message=message, user_sender_handle=user_sender_handle, user_receiver_handle=user_receiver_handle)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200



@app.route("/api/activities/home", methods=["GET"])
def data_home():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                  a.uuid::text,
                  u.handle,
                  a.message,
                  a.created_at,
                  a.expires_at,
                  a.likes_count,
                  (
                    SELECT count(*)
                    FROM replies r
                    WHERE r.reply_to_activity_uuid = a.uuid
                  ) AS replies_count
                FROM activities a
                LEFT JOIN public.users u ON u.uuid = a.user_uuid
                ORDER BY a.created_at DESC
                LIMIT 20;
            """)
            activities = cur.fetchall()
            for a in activities:
                cur.execute("""
                    SELECT
                        uuid::text,
                        reply_to_activity_uuid::text,
                        message,
                        created_at,
                        likes_count
                    FROM replies
                    WHERE reply_to_activity_uuid = %s::uuid
                    ORDER BY created_at ASC;
                """, (a["uuid"],))
                a["replies"] = cur.fetchall()
    return activities, 200


@app.route("/api/activities/@<string:handle>", methods=['GET'])
def data_handle(handle):
    model = UserActivities.run(handle)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200


@app.route("/api/activities/search", methods=['GET'])
def data_search():
    term = request.args.get('term')
    model = SearchActivities.run(term)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200


@app.route("/api/activities", methods=['POST', 'OPTIONS'])
@cross_origin()
def data_activities():
    user_handle = 'andrewbrown'
    message = request.json['message']
    ttl = request.json.get('ttl', '7-days')
    model = CreateActivity.run(message, user_handle, ttl)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200



@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
    data = ShowActivity.run(activity_uuid=activity_uuid)
    return data, 200


@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST', 'OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
    user_handle = 'andrewbrown'
    message = request.json['message']
    model = CreateReply.run(message, user_handle, activity_uuid)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200

# ============================================================
# After-Request Logging (CloudWatch)
# ============================================================
@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response

# ============================================================
# Run App
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)

  
