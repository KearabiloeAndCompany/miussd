import logging
import json
logger = logging.getLogger(__name__)


def send_sms(message,msisdn):
    import urllib
    try:
        logger.debug("Sending sms.\nMsisdn:{msisdn}".format(message=message,msisdn=msisdn))
        url = "https://api.panaceamobile.com/json?username=kearabiloe&password=_u-9xk5xs2medc6i0frvv_mx5ze3971k-0ttyt87bl9yii7q&text=%s&to=%s&action=message_send&from=%s" % (message,msisdn,"TTI")
        f = urllib.urlopen(url)
        s = json.loads(f.read())
        statusCode = s.get("status")
        statusString = s.get("message")
        if statusCode != '1':
            dispatched=False
        else:
            dispatched=True
        f.close()
        return
    except Exception as e:
        logger.error(e)
    return