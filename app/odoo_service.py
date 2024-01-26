import xmlrpc.client

class OdooService:
    def __init__(self, endpoint: str, database: str, user_email: str, user_password: str):
        self.endpoint = endpoint
        self.database = database
        self.user_email = user_email
        self.user_password = user_password
        common_proxy = xmlrpc.client.ServerProxy(f'{endpoint}/xmlrpc/2/common')
        self.user_id = common_proxy.authenticate(database, user_email, user_password, {})

    def register_employee(self, employee_name: str, position: str, official_email: str, country: str):
        object_proxy = xmlrpc.client.ServerProxy(f'{self.endpoint}/xmlrpc/2/object')
        employee_model = 'hr.employee'
        created_employee = object_proxy.execute_kw(self.database, self.user_id, self.user_password,
                                                   employee_model, 'create', [{
            'name': employee_name,
            'job_title': position,
            'work_email': official_email,
            'country_id': country,
        }])
        return created_employee

    def remove_employee(self, employee_email: str):
        object_proxy = xmlrpc.client.ServerProxy(f'{self.endpoint}/xmlrpc/2/object')
        employee_model = 'hr.employee'
        employee_ids = object_proxy.execute_kw(self.database, self.user_id, self.user_password,
                                               employee_model, 'search', [[['work_email', '=', employee_email]]])
        result = object_proxy.execute_kw(self.database, self.user_id, self.user_password,
                                         employee_model, 'unlink', [employee_ids])
        return result
