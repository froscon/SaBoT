from django.contrib.auth.decorators import user_passes_test, login_required

def user_is_staff(func):
	return user_passes_test(lambda u: u.is_staff)(login_required(func))

def user_is_finance(func):
	return user_passes_test(lambda u: u.is_staff and u.groups.filter(name="finance"))(login_required(func))
