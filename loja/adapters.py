from allauth.usersessions.adapter import DefaultUserSessionsAdapter

class CustomUserSessionsAdapter(DefaultUserSessionsAdapter):

    def on_login(self, request, user):
        # Executado quando o usuário loga
        print(f"Usuário {user.username} logou")

    def on_logout(self, request, user):
        print(f"Usuário {user.username} saiu")
