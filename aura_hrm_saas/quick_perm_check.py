from modules.auth import has_permission
print('admin can delete users?', has_permission(1, 'delete_users'))
print('hr can delete users?', has_permission(2, 'delete_users'))
print('hr can edit employees?', has_permission(2, 'edit_employees'))
print('accountant can edit attendance?', has_permission(3, 'edit_attendance'))
print('employee can view payroll?', has_permission(34, 'view_payroll'))
