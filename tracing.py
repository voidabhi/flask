from flask import Flask
from flask_opentracing import FlaskTracer

app = Flask(__name__)

tracer = FlaskTracer(tracer=some_opentracing_tracer)

@app.route("/traced-path")
@tracer.trace()
def traced_endpoint():
  return "This endpoint is traced!"
  
@app.route("/untraced-path")
def untraced_endpoint():
	return "This endpoint is not traced."
