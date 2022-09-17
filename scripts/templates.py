LABEL_QUERY_TEMPLATE = 'Translate the following SQL query to natural language as detailed as possible\n\n{}\n\n###\n\n'
# LABEL_QUERY_TEMPLATE = 'Describe the following SQL query as detailed as possible\n\n{}\n\n###\n\n'

FINETUNE_DATASET_TEMPLATE="""
### Postgres SQL tables, with their properties:
#
# Employee(id, name, department_id)
# Department(id, name, address)
# Salary_Payments(id, employee_id, amount, date)
#
### A query to list the names of the departments which employed more than 10 employees in the last 3 months
SELECT
"""