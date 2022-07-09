
def mysql_connection():

   import mysql.connector   

   try:
      con= mysql.connector.connect(user="root",password="finance123",auth_plugin="mysql_native_password",database='financeapp')
   except mysql.connector.Error as error:
      returnMesage = "Something went wrong: " + format(error)
      return(None,"Failure",returnMesage)
   return(con,"Succcess","Success")
   