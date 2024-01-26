import xmlrpc.client

class OdooService:
    def __init__(self, endpoint: str, database: str, user_email: str, user_password: str):
        self.endpoint = endpoint
        self.database = database
        self.user_email = user_email
        self.user_password = user_password
        self.common_proxy = xmlrpc.client.ServerProxy(f'{endpoint}/xmlrpc/2/common')
        self.user_id = self.common_proxy.authenticate(database, user_email, user_password, {})

    def register_employee(self, employee_name: str, position: str, official_email: str, password: str):
        object_proxy = xmlrpc.client.ServerProxy(f'{self.endpoint}/xmlrpc/2/object')
        
        # Primero, crear el empleado
        employee_model = 'hr.employee'
        created_employee_id = object_proxy.execute_kw(self.database, self.user_id, self.user_password,
                                                      employee_model, 'create', [{
                                                          'name': employee_name,
                                                          'job_title': position,
                                                          'work_email': official_email,
                                                      }])
        
        # Luego, crear el usuario y asociarlo con el empleado
        user_model = 'res.users'
        created_user_id = object_proxy.execute_kw(self.database, self.user_id, self.user_password,
                                                  user_model, 'create', [{
                                                      'name': employee_name,
                                                      'login': official_email,
                                                      'password': password,
                                                      'email': official_email,
                                                      'employee_ids': [(4, created_employee_id)]
                                                  }])
        return created_user_id


    def remove_employee(self, employee_email: str):
        object_proxy = xmlrpc.client.ServerProxy(f'{self.endpoint}/xmlrpc/2/object')
        employee_model = 'hr.employee'
        employee_ids = object_proxy.execute_kw(self.database, self.user_id, self.user_password,
                                               employee_model, 'search', [[['work_email', '=', employee_email]]])
        result = object_proxy.execute_kw(self.database, self.user_id, self.user_password,
                                         employee_model, 'unlink', [employee_ids])
        return result
