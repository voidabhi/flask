import uuid

class RequestIDMiddleware(object):
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        req_id = unicode(uuid.uuid4())
        environ["HTTP_X_REQUEST_ID"] = req_id
        def new_start_response(status, response_headers, exc_info=None):
            response_headers.append(("X-Request-ID", req_id))
            return start_response(status, response_headers, exc_info)
        return self.application(environ, new_start_response)
