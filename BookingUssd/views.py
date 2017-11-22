from django.shortcuts import render
from django.http import HttpResponse
import logging
from django.conf import settings
from django.utils import timezone
from BookingUssd.utils import send_sms
from BookingUssd.models import *
from django.contrib.humanize.templatetags import humanize
from django.utils.translation import gettext
from django.utils.crypto import get_random_string
logger = logging.getLogger(__name__)

def ussdView(request):
    try:
        logger.debug(request.session.keys())
        msisdn = request.GET.get('ussd_msisdn')
        node_name = request.GET.get("ussd_node_name")
        network = request.GET.get("ussd_network_name")
        ussd_request = request.GET.get("ussd_request")
        session_id = request.GET.get("ussd_session_id",get_random_string(length=32))
        try:
            ussd_request_args = ussd_request.strip("#").split(settings.USSD_STRING[:-1],1)[1][1:].split("*")
        except Exception as e:
            logger.debug(e.message)
            ussd_request_args = ussd_request
        logger.debug(ussd_request)
        if not ussd_request.endswith('#'):
            ussd_request = ussd_request+"#"
        
        ussd_session = UssdSession.objects.get_or_create(session_id=session_id)[0]
        if not ussd_session.church:
            ussd_session.church = Church.objects.get(ussd_string=ussd_request)
            ussd_session.save()
        church = ussd_session.church
        logger.debug(ussd_request)
        logger.debug(church)
        logger.debug(node_name)
        #Replace country code
        #msisdn = '0'+str(msisdn[2:])



        if node_name == "PublicMenu":
            logger.debug("Selected MEnu")
            logger.info(church)
            response = "{church_name}:\n" \
                        "1. {book_appointment}\n" \
                        "2. {featured_update}\n" \
                        "3. {updates}\n" \
                        "4. Contact\n".format(church_name=church.name,
                            featured_update=church.featured_update.title,
                            book_appointment=church.booking_action_label,
                            updates=church.updates_action_label)

            if church.admin.filter(user__username=msisdn).exists():
                logger.debug("User is Admin")
                response += "0. Admin\n"
            else:
                response += "5. Share via sms\n"

            return HttpResponse(response)

        if node_name == "BookingSubject":
            
            response = "{booking_subject}\n\n*. Back".format(booking_subject=church.booking_subject_label)

            return HttpResponse(response) 


        if node_name == "BookingMessage":
            
            response = "{booking_message}\n\n*. Back".format(booking_message=church.booking_message_label)

            return HttpResponse(response) 


        if node_name == "BookingConfirmation":

            # Create booking request
            # http://0.0.0.0:8000/ussd/?ussd_msisdn=27730174671&ussd_node_name=Confirmation&ussd_response_Home=1&ussd_response_Address=TestLoc&ussd_response_DateTime=TestDatetime
            cars_no = request.GET.get("ussd_response_BookingSubject")
            address = request.GET.get("ussd_response_BookingMessage")

            msg_admin = "New Request:\n" \
                        "{cars_no}\n" \
                        "{address}\n"\
                        "By:{cell_no} @ {time_now}\n".format(cars_no=cars_no,
                            address=address,
                            cell_no=msisdn,
                            time_now=str(timezone.now())[:16])

            msg_requester = church.booking_submission_message.format(SUPPORT_CELL_NO=settings.SUPPORT_CELL_NO)
            #send_sms(msg_admin,settings.SUPPORT_CELL_NO)
            #send_sms(msg_requester,msisdn)

            logger.debug(msg_admin)
            response = msg_requester
            response += "\n*. Back"
            return HttpResponse(response)

        if node_name == "FeaturedDetail":
            update = church.featured_update
            response = "{update_title}\n{update_detail}\n\n*. Back".format(update_title=update.title,update_datetime=str(update.datetime)[:16],update_detail=update.description)

            return HttpResponse(response)             

        if node_name == "UpdatesList":
            updates = Update.objects.filter(church=church,published=True)
            counter = 1
            response = ""

            for update in updates:
                response += "{counter}. {update_title}\n".format(counter=update.id,update_title=update.title,update_time=update.datetime)
                counter += 1
            response += "\n*. Back"
            return HttpResponse(response)

        if node_name == "UpdatesDetail":
            update_id = request.GET.get("ussd_response_UpdatesList")
            update = Update.objects.get(id=update_id)
            response = "{update_title}\n{update_detail}\n\n*. Back".format(update_title=update.title,update_datetime=str(update.datetime)[:16],update_detail=update.description)

            return HttpResponse(response)            
        else:
            response = "No option selected"
            response += "\n*. Menu"
            return HttpResponse(response, status=200)

    except Exception as e:
        logger.exception(e)
        response="An error occurred. Please contact support\n\n*. Back"
        return HttpResponse(response)

