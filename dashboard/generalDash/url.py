from django.urls import path
from . import views as gen

urlpatterns = [

    path("generalDash",gen.Log,name="login"),

    path("generalDash/login",gen.Log,name="login"),

    path("generalDash/emailValid",gen.Emailenter,name="em"),

    path("generalDash/Valid",gen.validation,name="validation"),

    path("generalDash/sign",gen.Sign,name="validation"),

    path("generalDash/session",gen.Sess,name="session"),

    path("generalDash/createSess",gen.creatSess,name="create"),

    path("generalDash/Analysis/<int:obj>/<int:num>",gen.Home,name="ana"),

    path("generalDash/Logout",gen.Logout_view,name="log"),
]