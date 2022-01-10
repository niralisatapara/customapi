import frappe
from frappe import _
from frappe.utils import escape_html
from frappe.website.utils import is_signup_disabled

@frappe.whitelist(allow_guest=True)
def sign_up(email, full_name, password, redirect_to=None):
	if is_signup_disabled():
		frappe.throw(_('Sign Up is disabled'), title='Not Allowed')

	user = frappe.db.get("User", {"email": email})
	if user:
		if user.enabled:
			return 0, _("Already Registered")
		else:
			return 0, _("Registered but disabled")
	else:
		if frappe.db.get_creation_count('User', 60) > 300:
			frappe.respond_as_web_page(_('Temporarily Disabled'),
				_('Too many users signed up recently, so the registration is disabled. Please try back in an hour'),
				http_status_code=429)

		user = frappe.get_doc({
			"doctype":"User",
			"email": email,
			"first_name": escape_html(full_name),
			"enabled": 1,
			"new_password": password,
			"user_type": "Website User"
		})
		user.flags.ignore_permissions = True
		user.flags.ignore_password_policy = True
		user.insert()
		api_secret = frappe.generate_hash(length=15)
		# if api key is not set generate api key
		if not user.api_key:
			api_key = frappe.generate_hash(length=15)
			user.api_key = api_key
		user.api_secret = api_secret
		user.save()
		api_token = "token " + user.api_key + ":" + user.get_password('api_secret')
		api_access_token = {"api_key":user.api_key, "api_secret":user.get_password('api_secret'), "api_token":api_token}
		# set default signup role as per Portal Settings
		default_role = frappe.db.get_value("Portal Settings", None, "default_role")
		if default_role:
			user.add_roles(default_role)

		if redirect_to:
			frappe.cache().hset('redirect_after_login', user.name, redirect_to)

		frappe.db.commit()
		return api_access_token

@frappe.whitelist(allow_guest=True)
def get_access_api_token(user):
	try:
		access_api_token = {}
		doc = frappe.get_doc("User", user)
		api_key = doc.api_key
		api_secret = doc.get_password('api_secret')
		if api_key and api_secret:
			api_token = "token " + api_key + ":" + api_secret
			access_api_token = {"api_key":api_key, "api_secret":api_secret, "api_token":api_token}
	except Exception as e:
		return e		
	return access_api_token 