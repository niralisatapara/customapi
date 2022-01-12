import frappe
import frappe.client

class BaseController:
	def __init__(self, doctype, name=None):
		self.doctype = doctype
		self.name = name

	@frappe.whitelist()
	def get_list(self):
		data = frappe.call(frappe.client.get_list, self.doctype, **frappe.local.form_dict)
		# set frappe.get_list result to response
		return frappe.local.response.update({"data": data})

	@frappe.whitelist()
	def get_doc(self):
		doc = frappe.get_doc(self.doctype, self.name)
		#if frappe.local.request.method=="GET":
		if not doc.has_permission("read"):
			raise frappe.PermissionError
		return frappe.local.response.update({"data": doc})

	@frappe.whitelist()
	def create(self):
		#if frappe.local.request.method == "POST":
		# fetch data from from dict
		data = get_request_form_data()
		data.update({"doctype": self.doctype})

		# insert document from request data
		doc = frappe.get_doc(data).insert()

		# set response data
		frappe.local.response.update({"data": doc.as_dict()})

		# commit for POST requests
		frappe.db.commit()

		return frappe.local.response

	@frappe.whitelist()
	def update(self):
		pass
		
	@frappe.whitelist()
	def delete(self):
		#if frappe.local.request.method == "DELETE":
		frappe.delete_doc(self.doctype, self.name, ignore_missing=False)
		frappe.local.response.http_status_code = 202
		frappe.local.response.message = "ok"
		frappe.db.commit()
	
def get_request_form_data():
	if frappe.local.form_dict.data is None:
		data = frappe.safe_decode(frappe.local.request.get_data())
	else:
		data = frappe.local.form_dict.data

	return frappe.parse_json(data)
