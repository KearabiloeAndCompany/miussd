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
import json

logger = logging.getLogger(__name__)

def ussdView(request):
    try:
        logger.debug(request.GET.copy())
        msisdn = request.GET.get('ussd_msisdn')
        node_name = request.GET.get("ussd_node_name")
        network = request.GET.get("ussd_network_name")
        ussd_request = request.GET.get("ussd_request")
        session_id = request.GET.get("ussd_session_id",get_random_string(length=32))
        try:
            ussd_request_args = ussd_request.strip("#").split(settings.BASE_USSD_STRING[:-1],1)[1][1:].split("*")
        except Exception as e:
            logger.debug(e.message)
            ussd_request_args = ussd_request
        logger.debug(ussd_request)
        if not ussd_request.endswith('#'):
            ussd_request = ussd_request+"#"
        
        ussd_session = UssdSession.objects.get_or_create(session_id=session_id)[0]
        if not ussd_session.church:
            ussd_session.church = Church.objects.get(ussd_string=ussd_request)
        ussd_session.request = json.dumps(request.GET.copy())
        ussd_session.save()
        church = ussd_session.church
        logger.debug(ussd_request)
        logger.debug(church)
        logger.debug(node_name)
        #Replace country code
        #msisdn = '0'+str(msisdn[2:])


        if node_name == "PublicMenu":
            if not church.featured_update:
                featured_update = "Featured Update"
            else:
                featured_update = church.featured_update.title
            response = "{church_name}:\n" \
                        "1. {book_appointment}\n" \
                        "2. {featured_update}\n" \
                        "3. {updates}\n" \
                        "4. Contact\n".format(church_name=church.name,
                            featured_update=featured_update,
                            book_appointment=church.booking_action_label,
                            updates=church.updates_action_label)


            if church.admin.filter(user__username=msisdn).exists():
                logger.debug("User is Admin")
                response += "00. Admin\n"



            return HttpResponse(response)

        if node_name == "AdminMenu":
            response = "1. Change Name\n"\
                        "2. New/Featured Update\n"\
                        "3. Add Admin\n"

            return HttpResponse(response)


        if node_name == "AdminConfirmUserAction":
            username = request.GET.get("ussd_response_AdminRegister_Username")
            response = "Please confirm your action:\n"\
                        "1. Add {username} to {church}\n"\
                        "2. Create new account\n\n00. Back".format(username=username,church=church.name)

            return HttpResponse(response)

        if node_name == "AdminAddAdminConfirmation":
            username = request.GET.get("ussd_response_AdminRegister_Username")
            first_name = request.GET.get("ussd_response_AdminRegister_Firstname")
            last_name = request.GET.get("ussd_response_AdminRegister_Lastname")
            try:
                user,new_user = User.objects.get_or_create(username=username)
                if new_user:
                    user.first_name=first_name,
                    user.last_name=last_name
                    user.save()

                church_admin = ChurchAdmin.objects.get_or_create(user=user)[0]
                church.admin.add(church_admin)
                church.save()
                response = "You have successfully added admin {user} to {church}".format(user=user.username,church=church.name)

            except Exception,e:
                logger.exception(e)
                response = e.message

            return HttpResponse(response)            

        if node_name == "AdminChangeNameConfirmation":
            new_name = request.GET.get("ussd_response_AdminChangeName")
            church.name = new_name
            church.save()
            response = "Your New Public name is:\n{display_name}\n00. Back".format(display_name=church.name)

            return HttpResponse(response)

        if node_name == "AdminChangeName":
            response = "Current name:{display_name}\n"\
                        "Enter a new name:\n"\
                        "Example: CocaCola SA\n"\
                        "\n00. Back".format(display_name=church.name)

            return HttpResponse(response)

        if node_name == "AdminChangeNameConfirmation":
            new_name = request.GET.get("ussd_response_AdminChangeName")
            church.name = new_name
            church.save()
            response = "Your New Public name is:\n{display_name}\n00. Back".format(display_name=church.name)

            return HttpResponse(response)

        if node_name == "AdminNewUpdateTitle":
            response = "Enter Update's Title:\n"\
                        "Example: How it works\n"\
                        "\n00. Back"

            return HttpResponse(response)

        if node_name == "AdminNewUpdateDescription":
            response = "Enter Update's Content:\n"\
                        "Example: This is how this services works.\n"\
                        "\n00. Back"

            return HttpResponse(response)


        if node_name == "AdminNewUpdateFeatured":
            response = "Do you want to make this update featured?\n"\
                        "This will make it visible on the Menu as option 3.\n\n"\
                        "1. Yes.\n"\
                        "2. No.\n"\
                        "\n00. Back"

            return HttpResponse(response)


        if node_name == "AdminNewUpdateConfirmation":
            update_title = request.GET.get("ussd_response_AdminNewUpdateTitle")
            update_description = request.GET.get("ussd_response_AdminNewUpdateDescription")
            update_featured = request.GET.get("ussd_response_AdminNewUpdateFeatured")
            logger.info(update_featured)
            if update_featured in ["1",1]:
                logger.debug("Making Update Featured")
                update_featured = True
            else:
                update_featured = False
            logger.info(update_featured)
            update = Update.objects.create(title=update_title,description=update_description, datetime=timezone.now())
            update.church.add(church)
            update.save()

            if update_featured:
                church.featured_update = update
                church.save()

            response = "Published Update:\n"\
                        "{update_title}\n"\
                        "{update_description}\n"\
                        "\n00. Back".format(update_title=update.title, update_description=update.description)

            return HttpResponse(response)

        if node_name == "AdminRegisterConfirmation":
            username = request.GET.get("ussd_response_AdminRegister_Username")
            first_name = request.GET.get("ussd_response_AdminRegister_Firstname")
            last_name = request.GET.get("ussd_response_AdminRegister_Lastname")
            display_name = request.GET.get("ussd_response_AdminRegister_Displayname")
            # pin = request.GET.get("ussd_response_AdminRegister_Pin","0000")
            # email = request.GET.get("ussd_response_AdminRegister_Email")

            try:
                user,new_user = User.objects.get_or_create(username=username)
                if new_user:
                    user.first_name=first_name,
                    user.last_name=last_name
                    user.save()


                church_admin = ChurchAdmin.objects.get_or_create(user=user)[0]

                church = Church.objects.create(name=display_name)
                church.admin.add(church_admin)
                church.save()

                response = "Profile Created. Dial {church_ussd} from " \
                            "{admin_username} to manage {display_name}".format(display_name=church.name,
                                admin_username=user.username,
                                church_ussd=church.ussd_string)
            except Exception,e:
                logger.exception(e)
                response = "An error occured.\n{error_message}".format(error_message=e.message)

            return HttpResponse(response)

        if node_name == "BookingSubject":
            
            response = "{booking_subject}\n\n00. Back".format(booking_subject=church.booking_subject_label)

            return HttpResponse(response) 


        if node_name == "BookingMessage":
            
            response = "{booking_message}\n\n00. Back".format(booking_message=church.booking_message_label)

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
            for admin in church.admin.all():
                send_sms(msg_admin,admin.notification_msisdn)
            #send_sms(msg_requester,msisdn)

            logger.debug(msg_admin)
            response = msg_requester
            response += "\n00. Back"
            return HttpResponse(response)

        if node_name == "FeaturedDetail":
            if church.featured_update:
                update = church.featured_update
                response = "{update_title}\n{update_detail}\n\n00. Back".format(update_title=update.title,update_datetime=str(update.datetime)[:16],update_detail=update.description)
            else:
                response = "To set a featured update go back to \nMenu and select Admin,\nNew/Featured Update and \nconfirm featured update when prompted\n\n00. Back"

            return HttpResponse(response)             

        if node_name == "ContactDetail":
            update = church.featured_update
            response = "{contact}\n\n00. Back".format(contact=church.contact_details)

            return HttpResponse(response)             

        if node_name == "UpdateList":
            updates = Update.objects.filter(church=church,published=True)
            counter = 1
            response = ""

            for update in updates:
                response += "{counter}. {update_title}\n".format(counter=update.id,update_title=update.title[:10],update_time=update.datetime)
                counter += 1
            response += "\n00. Back"
            return HttpResponse(response)

        if node_name == "UpdateDetail":
            update_id = int(request.GET.get("ussd_response_UpdateList"))
            update = Update.objects.get(id=update_id)
            response = "{update_title}\n{update_detail}\n\n00. Back".format(update_title=update.title,update_datetime=str(update.datetime)[:16],update_detail=update.description)

            return HttpResponse(response)            
        else:
            response = "No option selected"
            response += "\n00. Menu"
            return HttpResponse(response, status=200)

    except Exception as e:
        logger.exception(e)
        response="An error occurred. Please contact support\n\n00. Back"
        return HttpResponse(response)

