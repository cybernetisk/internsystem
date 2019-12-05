from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render, resolve_url
from django.utils.http import is_safe_url
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils


def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=settings.SAML_FOLDER)
    return auth


def prepare_django_request(request):
    result = {
        "http_host": request.META["HTTP_HOST"],
        "script_name": request.META["PATH_INFO"],
        # as we run behind proxy, we fake the ports
        "server_port": 443 if request.is_secure() else request.META["SERVER_PORT"],
        "get_data": request.GET.copy(),
        "post_data": request.POST.copy(),
    }
    return result


# AssertionConsumerService
def acs(request):
    req = prepare_django_request(request)
    auth = init_saml_auth(req)

    auth.process_response()

    data = {"errors": auth.get_errors(), "not_auth_warn": not auth.is_authenticated()}

    if not data["errors"]:
        request.session["samlUserdata"] = auth.get_attributes()
        request.session["samlNameId"] = auth.get_nameid()
        request.session["samlSessionIndex"] = auth.get_session_index()

        user = authenticate(saml_authentication=auth)
        if user is None:
            data["errors"] = ["Authentication backend failed."]
        elif not user.is_active:
            data["errors"] = ["User is not active. TODO: logout at idp?"]
        else:
            login(request, user)
            if (
                "RelayState" in req["post_data"]
                and OneLogin_Saml2_Utils.get_self_url(req)
                != req["post_data"]["RelayState"]
            ):
                return HttpResponseRedirect(
                    auth.redirect_to(req["post_data"]["RelayState"])
                )
            return HttpResponseRedirect(
                OneLogin_Saml2_Utils.get_self_url(req) + "/profile"
            )

    return draw_page(request, data)


# SingleLogoutService
def sls(request):
    req = prepare_django_request(request)
    auth = init_saml_auth(req)

    def dscb():
        return request.session.flush()

    url = auth.process_slo(delete_session_cb=dscb)

    data = {"not_auth_warn": False, "errors": auth.get_errors()}

    if len(data["errors"]) == 0:
        logout(request)
        if url is not None:
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect(OneLogin_Saml2_Utils.get_self_url(req))

    return draw_page(request, data)


def index(request):
    if "sso" in request.GET:
        return sso(request)

    req = prepare_django_request(request)
    auth = init_saml_auth(req)

    data = {"errors": [], "not_auth_warn": False}

    if "slo" in req["get_data"]:
        name_id = None
        session_index = None
        if "samlNameId" in request.session:
            name_id = request.session["samlNameId"]
        if "samlSessionIndex" in request.session:
            session_index = request.session["samlSessionIndex"]
        return HttpResponseRedirect(
            auth.logout(name_id=name_id, session_index=session_index)
        )

    return draw_page(request, data)


def sso(request):
    req = prepare_django_request(request)
    auth = init_saml_auth(req)

    # Ensure the user-originating redirection url is safe.
    redirect_to = request.POST.get("next", request.GET.get("next", ""))
    if not is_safe_url(url=redirect_to, allowed_hosts=request.get_host()):
        redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

    return HttpResponseRedirect(auth.login(redirect_to))


def draw_page(request, data):
    attributes = False
    paint_logout = False

    if "samlUserdata" in request.session:
        paint_logout = True
        if len(request.session["samlUserdata"]) > 0:
            attributes = request.session["samlUserdata"].items()

    return render(
        request,
        "index.html",
        {
            "errors": data["errors"],
            "not_auth_warn": data["not_auth_warn"],
            "attributes": attributes,
            "paint_logout": paint_logout,
        },
    )


# Metadata for the SAML2-service
def metadata(request):
    req = prepare_django_request(request)
    auth = init_saml_auth(req)
    saml_settings = auth.get_settings()
    metadata = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = HttpResponse(content=metadata, content_type="text/xml")
    else:
        resp = HttpResponseServerError(content=", ".join(errors))
    return resp
