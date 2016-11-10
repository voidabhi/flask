

@app.before_request
def statsd_start():
    startTime = time.time()
    endpoint = request.endpoint
    if endpoint:
        @flask.after_this_request
        def statsd_finish(response):
            endTime = time.time()
            duration = endTime - startTime
            status = response.status_code
            method = request.method
            routepreifx = "routes." + method + "." + endpoint
            app.statsd.incr(routeprefix + ".request")
            app.statsd.incr(routeprefix + ".status." + str(status))
            app.statsd.timing(routeprefix + ".timing", duration * 1000)
            return response
