from django.urls import path, re_path, include
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django_registration.backends.activation.views import RegistrationView

from sabot.views import (
    ParticipantsView,
    OwnerSettingCreateView,
    PermCheckUpdateView,
    EmailOutputView,
    XMLListView,
    MultipleListView,
    PropertySetterView,
    PermCheckPropertySetterView,
    PermCheckSimpleDeleteView,
    ArchiveCreatorView,
)
from sabot.decorators import user_is_staff

from account.views import (
    TokenLoginView,
    UserProfileView,
    ActivateAndSetPWView,
    GenerateAuthTokenView,
)
from account.forms import RegistrationFormNameAndUniqueEmail
from account.models import UserProfile


urlpatterns = [
    re_path(
        "^token/(?P<token>[0-9a-z]+)$", TokenLoginView.as_view(), name="auth_token"
    ),
    path(
        "profile", login_required(UserProfileView.as_view()), name="auth_user_profile"
    ),
    re_path(
        "^activatepw/(?P<activation_key>[^/]+)/?$",
        ActivateAndSetPWView.as_view(),
        name="auth_activate_pw",
    ),
    path(
        "register/",
        RegistrationView.as_view(form_class=RegistrationFormNameAndUniqueEmail),
        name="auth_register_with_name",
    ),
    # staff pages
    path(
        "list+projects",
        user_is_staff(
            ListView.as_view(
                model=User, template_name="registration/userAffiliation.html"
            )
        ),
        name="auth_user_affil",
    ),
    path(
        "list",
        user_is_staff(
            ListView.as_view(model=User, template_name="registration/userList.html")
        ),
        name="auth_user_list",
    ),
    path(
        "<int:pk>/makestaff",
        user_is_staff(
            PropertySetterView.as_view(
                model=User,
                property_name="is_staff",
                property_value=True,
                next_view="auth_user_list",
            )
        ),
        name="auth_user_makestaff",
    ),
    path(
        "<int:pk>/revokestaff",
        user_is_staff(
            PropertySetterView.as_view(
                model=User,
                property_name="is_staff",
                property_value=False,
                next_view="auth_user_list",
            )
        ),
        name="auth_user_revokestaff",
    ),
    path(
        "<int:pk>/enable",
        user_is_staff(
            PropertySetterView.as_view(
                model=User,
                property_name="is_active",
                property_value=True,
                next_view="auth_user_list",
            )
        ),
        name="auth_user_enable",
    ),
    path(
        "<int:pk>/disable",
        user_is_staff(
            PropertySetterView.as_view(
                model=User,
                property_name="is_active",
                property_value=False,
                next_view="auth_user_list",
            )
        ),
        name="auth_user_disable",
    ),
    path(
        "<int:pk>/delete",
        user_is_staff(
            DeleteView.as_view(
                model=User,
                template_name="registration/del.html",
                success_url="/accounts/list",
            )
        ),
        name="auth_user_delete",
    ),
    path(
        "<int:pk>/removeToken",
        user_is_staff(
            PropertySetterView.as_view(
                model=UserProfile,
                property_name="authToken",
                property_value=None,
                next_view="auth_user_list",
            )
        ),
        name="auth_user_remove_token",
    ),
    path(
        "<int:pk>/genAuthToken",
        user_is_staff(GenerateAuthTokenView.as_view()),
        name="auth_user_gen_token",
    ),
    path("", include("django.contrib.auth.urls")),
]
