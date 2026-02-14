from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from allauth.account.signals import user_signed_up
from loja.models import Usuario

User = get_user_model()

@receiver(pre_social_login)
def merge_google_user(request, sociallogin, **kwargs):

    email = sociallogin.account.extra_data.get("email")

    if not email:
        return

    # se já existe auth user
    try:
        auth_user = User.objects.get(email=email)
        sociallogin.connect(request, auth_user)
        return
    except User.DoesNotExist:
        pass

    # procurar usuario da loja
    try:
        usuario_loja = Usuario.objects.get(email=email)

        sociallogin.user.email = email
        sociallogin.user.first_name = usuario_loja.nome
        sociallogin.user.save()

        usuario_loja.auth_user = sociallogin.user
        usuario_loja.save()

    except Usuario.DoesNotExist:
        pass
@receiver(user_signed_up)
def criar_usuario_loja(request, user, **kwargs):

    Usuario.objects.get_or_create(
        auth_user=user,
        email=user.email,
        defaults={
            "nome": user.first_name
        }
    )