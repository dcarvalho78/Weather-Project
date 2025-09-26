from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings
from .models import WeatherReading

def _safe_float(v):
    try:
        return float(v)
    except Exception:
        return None

def _f_to_c(f):
    try:
        return (float(f) - 32.0) * 5.0/9.0
    except Exception:
        return None

def parse_ecowitt_payload(payload: dict):
    out = {}
    out['stationtype'] = payload.get('stationtype') or payload.get('model') or None
    out['station_id'] = payload.get('id') or payload.get('stationid') or payload.get('mac') or None

    if 'tempc' in payload:
        out['temp_c'] = _safe_float(payload.get('tempc'))
    elif 'tempf' in payload:
        out['temp_c'] = _f_to_c(payload.get('tempf'))
    else:
        for k in ('temp1', 'tempf1', 'temp1f', 'tempc1'):
            if k in payload:
                if k.startswith('tempf') or k.endswith('f'):
                    out['temp_c'] = _f_to_c(payload.get(k))
                else:
                    out['temp_c'] = _safe_float(payload.get(k))
                break

    for k in ('humidity', 'humidity1', 'hum', 'humidityin'):
        if k in payload:
            try:
                out['humidity'] = int(float(payload.get(k)))
            except Exception:
                out['humidity'] = None
            break

    for k in ('winddir', 'winddir_deg', 'winddirection'):
        if k in payload:
            try:
                out['wind_dir'] = int(float(payload.get(k)))
            except Exception:
                out['wind_dir'] = None
            break

    if 'windspeedmph' in payload:
        mph = _safe_float(payload.get('windspeedmph'))
        if mph is not None:
            out['wind_speed_mps'] = mph * 0.44704
    elif 'windspeedkph' in payload:
        kph = _safe_float(payload.get('windspeedkph'))
        if kph is not None:
            out['wind_speed_mps'] = kph / 3.6
    elif 'windspeed' in payload:
        out['wind_speed_mps'] = _safe_float(payload.get('windspeed'))

    if 'rainin' in payload:
        inches = _safe_float(payload.get('rainin'))
        if inches is not None:
            out['rain_mm'] = inches * 25.4
    elif 'rainmm' in payload:
        out['rain_mm'] = _safe_float(payload.get('rainmm'))
    elif 'rain' in payload:
        out['rain_mm'] = _safe_float(payload.get('rain'))

    if 'baromrelin' in payload or 'baromabsin' in payload or 'baromin' in payload:
        val = payload.get('baromrelin') or payload.get('baromabsin') or payload.get('baromin')
        try:
            out['pressure_hpa'] = float(val) * 33.8639
        except Exception:
            out['pressure_hpa'] = None
    elif 'barom' in payload:
        out['pressure_hpa'] = _safe_float(payload.get('barom'))

    if 'UV' in payload:
        out['uv'] = _safe_float(payload.get('UV'))
    elif 'uv' in payload:
        out['uv'] = _safe_float(payload.get('uv'))

    out['battery'] = payload.get('batt') or payload.get('battery') or None

    return out

@csrf_exempt
def ecowitt_listener(request):
    if request.method == "GET":
        return JsonResponse({"status":"ok","msg":"ecowitt endpoint alive"})

    if request.method != "POST":
        return HttpResponseBadRequest("POST expected")

    token_required = getattr(settings, "ECOWITT_SHARED_TOKEN", None)
    if token_required:
        token = request.GET.get("token") or request.POST.get("token")
        if token != token_required:
            return JsonResponse({"status":"error","msg":"bad token"}, status=403)

    ip_whitelist = getattr(settings, "ECOWITT_ALLOWED_IPS", None)
    if ip_whitelist:
        remote = request.META.get("REMOTE_ADDR")
        if remote not in ip_whitelist:
            return JsonResponse({"status":"error","msg":"ip not allowed"}, status=403)

    form = request.POST.dict()
    parsed = parse_ecowitt_payload(form)

    reading = WeatherReading.objects.create(
        stationtype = parsed.get("stationtype"),
        station_id = parsed.get("station_id"),
        temp_c = parsed.get("temp_c"),
        humidity = parsed.get("humidity"),
        wind_dir = parsed.get("wind_dir"),
        wind_speed_mps = parsed.get("wind_speed_mps"),
        rain_mm = parsed.get("rain_mm"),
        pressure_hpa = parsed.get("pressure_hpa"),
        uv = parsed.get("uv"),
        battery = parsed.get("battery"),
        raw = form
    )
    return JsonResponse({"status":"ok","id": reading.id})
