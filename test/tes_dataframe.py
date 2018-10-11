# from __future__ import print_function
from displayfunction import display
from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("IdsToStix") \
        .getOrCreate()

    # import pyspark class Row from module sql
    from pyspark.sql import *

    # Create Example Data - Departments and Employees

    # Create the Departments
    department1 = Row(id='123456', name='Computer Science')
    department2 = Row(id='789012', name='Mechanical Engineering')
    department3 = Row(id='345678', name='Theater and Drama')
    department4 = Row(id='901234', name='Indoor Recreation')

    # Create the Employees
    Employee = Row("firstName", "lastName", "email", "salary")
    employee1 = Employee('michael', 'armbrust', 'no-reply@berkeley.edu', 100000)
    employee2 = Employee('xiangrui', 'meng', 'no-reply@stanford.edu', 120000)
    employee3 = Employee('matei', None, 'no-reply@waterloo.edu', 140000)
    employee4 = Employee(None, 'wendell', 'no-reply@berkeley.edu', 160000)

    # Create the DepartmentWithEmployees instances from Departments and Employees
    departmentWithEmployees1 = Row(department=department1, employees=[employee1, employee2])
    departmentWithEmployees2 = Row(department=department2, employees=[employee3, employee4])
    departmentWithEmployees3 = Row(department=department3, employees=[employee1, employee4])
    departmentWithEmployees4 = Row(department=department4, employees=[employee2, employee3])

    print department1
    print employee2
    print departmentWithEmployees1

    departmentsWithEmployeesSeq1 = [departmentWithEmployees1, departmentWithEmployees2]
    df1 = spark.createDataFrame(departmentsWithEmployeesSeq1)

    js = df1.toJSON().collect()
    print js

    departmentsWithEmployeesSeq2 = [departmentWithEmployees3, departmentWithEmployees4]
    df2 = spark.createDataFrame(departmentsWithEmployeesSeq2)

    obs = Row(created='2018-04-13T01:03:43.279Z', first_observed='2018-04-13T01:03:43.279105Z', id='observed-data--cda49e89-2387-4c89-9a8d-3000c06d6b8a', last_observed='2018-04-13T01:03:43.279105Z', modified='2018-04-13T01:03:43.279Z', number_observed=1)

    df = spark.createDataFrame([obs])
    df.printSchema()

    # display(df2)

    spark.stop()
