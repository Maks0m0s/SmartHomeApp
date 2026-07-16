from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash

def register(validated_data):
    user = User(
        username=validated_data["username"],
        email=validated_data.get("email", ""),
        first_name=validated_data.get("first_name", ""),
        last_name=validated_data.get("last_name", ""),
    )
    user.set_password(validated_data["password"])
    user.save()

    return user

def delete_account(request):
    user = request.user
    user.delete()          # delete from DB

def update_account(request):
    user = request.user

    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    current_password = request.POST.get('current_password', '')
    new_password = request.POST.get('new_password', '').strip()

    # --- VALIDATION ---
    if not username:
        return {'result': False, 'error': 'Username is required'}

    if not email or '@' not in email:
        return {'result': False, 'error': 'Invalid email'}

    if not current_password:
        return {'result': False, 'error': 'Current password is required'}

    if not user.check_password(current_password):
        return {'result': False, 'error': 'Current password is incorrect'}

    # --- UPDATE FIELDS ---
    user.username = username
    user.email = email
    user.first_name = first_name
    user.last_name = last_name

    # --- UPDATE PASSWORD (optional) ---
    if new_password:
        user.set_password(new_password)
        update_session_auth_hash(request, user)

    user.save()

    return {'result': True}