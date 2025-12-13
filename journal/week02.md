# Week 2 — Distributed Tracing

This week focused on adding distributed tracing, logging, and error reporting to the Cruddur application using **AWS X-Ray**, **Honeycomb (OpenTelemetry)**, **CloudWatch Logs**, and **Rollbar**.

---

## 1. AWS X-Ray — Distributed Tracing for Flask

### Set Region
```bash
export AWS_REGION="us-east-1"
```

### Install Dependencies

Add to `requirements.txt`:
```
aws-xray-sdk
```

Install:
```bash
pip install -r requirements.txt
```

### Add Middleware to `app.py`
```python
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='Cruddur', dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)
```

### Create `aws/json/xray.json`
```json
{
  "SamplingRule": {
    "RuleName": "Cruddur",
    "ResourceARN": "*",
    "Priority": 9000,
    "FixedRate": 0.1,
    "ReservoirSize": 5,
    "ServiceName": "Cruddur",
    "ServiceType": "*",
    "Host": "*",
    "HTTPMethod": "*",
    "URLPath": "*",
    "Version": 1
  }
}
```

### Create X-Ray Group and Sampling Rule
```bash
FLASK_ADDRESS="https://4567-${CODESPACE_NAME}.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
aws xray create-group \
  --group-name "Cruddur" \
  --filter-expression "service(\"$FLASK_ADDRESS\") {fault OR error}" \
  --region us-east-1

aws xray create-sampling-rule \
  --cli-input-json file://aws/json/xray.json \
  --region us-east-1
```

---

## 2. Honeycomb — OpenTelemetry Tracing

### Add Dependencies

Add to `requirements.txt`:
```
opentelemetry-api
opentelemetry-sdk
opentelemetry-exporter-otlp-proto-http
opentelemetry-instrumentation-flask
opentelemetry-instrumentation-requests
```

Install:
```bash
pip install -r requirements.txt
```

### Add Tracing to `app.py`
```python
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
```

### Add Env Vars (docker-compose)
```yaml
OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"
OTEL_SERVICE_NAME: "${HONEYCOMB_SERVICE_NAME}"
```

---

## 3. CloudWatch Logs

### Add Dependency

Add to `requirements.txt`:
```
watchtower
```

Install:
```bash
pip install -r requirements.txt
```

### Add Logging to `app.py`
```python
import watchtower
import logging
from time import strftime

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)
```

### Add Automatic Request Logging
```python
@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    LOGGER.error(
        '%s %s %s %s %s %s',
        timestamp,
        request.remote_addr,
        request.method,
        request.scheme,
        request.full_path,
        response.status
    )
    return response
```

---
## 4. Rollbar — Backend Error Tracking

Integrated **Rollbar** to capture and monitor backend exceptions in the Flask application.

### Add Dependencies

Added to `requirements.txt`:

blinker
rollbar


Installed dependencies:
```bash
pip install -r requirements.txt

Add Environment Variable (docker-compose)

ROLLBAR_ACCESS_TOKEN: "${ROLLBAR_ACCESS_TOKEN}"

Initialize Rollbar in app.py

import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

rollbar_access_token = os.getenv("ROLLBAR_ACCESS_TOKEN")

if rollbar_access_token:
    rollbar.init(
        access_token=rollbar_access_token,
        environment="development",
        root=os.path.dirname(os.path.realpath(__file__)),
    )
    got_request_exception.connect(
        rollbar.contrib.flask.report_exception,
        app
    )

Test Endpoint

Created a test route that intentionally raises an exception:

@app.route("/rollbar/test")
def rollbar_test():
    raise Exception("Rollbar backend test: intentional exception")

Verification

Triggered the endpoint using curl

Confirmed the exception appeared in the Rollbar dashboard

Verified full Python/Flask stack trace and environment metadata

Evidence (stored in journal/assets/week02/)

Week02-08-Rollbar-Backend-Exception-List.png

Week02-09-Rollbar-Backend-Exception-Details.png


---

## STEP 3 — TWO SMALL FIXES

### A) Fix Required Screenshots table (Rollbar row)

Change this row:

```markdown
| Rollbar | "Hello World!" test event appears |







---

## Required Screenshots

| Section | Required Proof |
|---------|----------------|
| X-Ray | X-Ray console showing service graph traces |
| Honeycomb | Dataset showing spans arriving |
| CloudWatch | Log group "cruddur" visible + logs inside |
| Rollbar | "Hello World!" test event appears |

### Screenshot Format Example:
```markdown
![X-Ray Service Graph](assets/week02-xray.png)
![Honeycomb Dataset](assets/week02-honeycomb.png)
![CloudWatch Logs](assets/week02-cloudwatch.png)
![Rollbar Test Event](assets/week02-rollbar.png)
```

---

## Week 2 Summary

This week I implemented:

* **AWS X-Ray** distributed tracing
* **Honeycomb** tracing through OpenTelemetry
* **CloudWatch** structured logging
* **Rollbar** error reporting

These tools help diagnose errors, trace user requests, and monitor performance in a distributed system.

---

## ✅ Week 2 Distributed Tracing: Complete# Week 2 — Distributed Tracing