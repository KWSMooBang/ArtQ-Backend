import time, json, logging
from django.utils.deprecation import MiddlewareMixin

log = logging.getLogger("request")

class RequestLogMiddleware(MiddlewareMixin):
    """
    request/response logging + handling duration (ms)
    sensitive data (password, token etc) are masked
    """
    SENSITIVE_KEYS = {"password", "refresh", "access"}

    def process_request(self, request):
        request._start_time = time.perf_counter()

    def process_response(self, request, response):
        try:
            duration_ms = None
            if hasattr(request, "_start_time"):
                duration_ms = int((time.perf_counter() - request._start_time) * 1000)

            meta = {
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "duration_ms": duration_ms,
                "user": getattr(getattr(request, "user", None), "id", None),
                "ip": self._client_ip(request),
            }

            # request body (JSON only, masking sensitive data)
            if request.method in ("POST", "PUT", "PATCH"):
                try:
                    body = request.body.decode("utf-8")
                    if body and body.strip().startswith("{"):
                        data = json.loads(body)
                        for k in list(data.keys()):
                            if k.lower() in self.SENSITIVE_KEYS:
                                data[k] = "***"
                        meta["body"] = data
                except Exception:
                    pass

            log.info(meta)
        except Exception:
            # make error in logging not affect the main response flow
            pass
        return response

    @staticmethod
    def _client_ip(request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            return xff.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")