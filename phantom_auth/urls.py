from django.urls import path
from .views import InitConnectView, VerifySignatureView, TokenBalanceView

urlpatterns = [
    path('init-connect/', InitConnectView.as_view()),
    path('verify-signature/', VerifySignatureView.as_view()),
    path('balance/', TokenBalanceView.as_view())
]