import logging
import json
from django.conf import settings
logger = logging.getLogger(__name__)


def send_sms(message,msisdn):
    import urllib
    try:
        logger.debug("Sending sms.\nMsisdn:{msisdn}".format(message=message,msisdn=msisdn))
        url = "https://api.panaceamobile.com/json?username={username}&password={password}&text={body}&to={recipient}&action=message_send&from={sender}".format(body=sms.message,
            recipient=sms.msisdn,
            sender="Crowdcoin",
            username=settings.PANACEA_USER,
            password=settings.PANACEA_PASSWORD)
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