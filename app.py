from flask import Flask , render_template , request
from  MySqlConnection import *
import mysql.connector
import csv
import sys, os, traceback
import pickle 
import tkinter
from tkinter import *
from tkinter import filedialog 

import numpy as np
import matplotlib.pyplot as plt 
import plotly.graph_objects as go
import datetime

from flask_cachebuster import CacheBuster


app = Flask(__name__)
LoginDetails=[]
l=[]
Id=''
h=[]
em=''
g=''
keys=[]
d={}
t=()
i=[]
e=[]
f=()


@app.after_request
def add_header(r):
    
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def index():
    title = "Fespa"
    return render_template("home.html", title=title )

@app.route('/Home')
def Home():
    title = "Home"
    return render_template("homePostLogin.html", title=title  )

@app.route("/AboutPreLogin")
def AboutPreLogin():
    title = "Fespa"
    return render_template("aboutPost.html", title=title)

@app.route("/About")
def About():
    title = "About"
    return render_template("about.html", title=title)

@app.route('/Login')
def Login():
    title = "Login"
    return render_template("login.html", title=title)


@app.route('/PostLogin' , methods=["POST"])
def PostLogin():
    title = "PostLogin"
    email = request.form.get("emailId")
    password = request.form.get("password")
    h,t,f=LoginCustomer(email,password)
    return render_template(f, title=h ,h=h ,t=t)
    
@app.route('/SignUp', methods=["POST"])
def SignUp():
    title="SignUp"
    return render_template("sign_up.html", title=title)

@app.route('/Calculate', methods=["POST"])
def Calculate():
    title="Calculate"
    return render_template("calculate.html", title=title)


@app.route('/Log', methods=["POST"])
def Log():
    first_Name = request.form.get("First_Name")
    Second_Name = request.form.get("Second_Name")       
    email = request.form.get("emailId")
    Mobile_Number = request.form.get("Mobile_Number")
    DOB= request.form.get("DOB")
    password = request.form.get("password")
    title="Log"
    t,h= RegisterCustomer(first_Name,Second_Name,email,Mobile_Number,DOB,password)
    return render_template( "log.html",title=title , rc=t ,rm=h)

@app.route('/browseFiles', methods=["POST"])
def browseFiles():
    global label_file_explorer
    global em
    title = "Browse" 
    root = tkinter.Tk()
    label_file_explorer= tkinter.Label(root)
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Csv files", "*.csv*"), ("all files","*.*"))) 
    ImportFinanceData(filename,em )   
    return render_template("browseFiles.html",title=title , h=filename)

@app.route('/Import')
def Import():
    title= "Import"
    return render_template("import.html", title=title)

@app.route("/Report")
def Report():
    title = "Report"
    return render_template("report.html", title=title)



@app.route("/Monthly_Finance" , methods=["POST"])
def Monthly_Finance():
    global g
    title = "Monthly Finance"
    g='monthly'
    return render_template("monthly_Finance.html", title=title)


@app.route("/Yearly_Finance" , methods=["POST"])
def Yearly_Finance():
    global g
    title = "Yearly Finance"
    g ="yearly"
    return render_template("yearly_Finance.html", title=title)

@app.route("/Final" , methods=["POST"])
def Final():
    Month =request.form.get("Month")
    Year=request.form.get("Year")
    global g
    global Id
    global t
    global i
    global e
    global f
    title = "Final"
    if g == 'monthly':
       t,i,e = Monthly_ProfileCalculation(Id,Month,Year)
       f=(t,i,e)
    elif g == 'yearly':
        t,i,e = Yearly_ProfileCalculation(Id,Year)
        f=(t,i,e)
    Graph(f)
    return render_template("final.html", title=title , t=t , i=i, e=e , g=g  , Id=Id,f=f )

@app.route('/CurrentNetWorth', methods=["POST"])
def CurrentNetWorth():
    title="CurrentNetWorth"
    return render_template("currentNetworth.html", title=title)

@app.route('/CurrentFinal', methods=["POST"])
def CurrentFinal():
    global Id
    AvgReturn=request.form.get('AvgReturn')
    AvgIntrest=request.form.get('AvgIntrest')
    title="CurrentFinal"
    y= Networth_Calculation(Id,int(AvgReturn),int(AvgIntrest))
    Graph2(y)
    return render_template("currentFinal.html", title=title , k=y)



@app.route('/FinanceFreedom' , methods=["POST"])
def FinanceFreedom():
  title='FinanceFreedom'
  return render_template('financeFreedom.html', title=title)

@app.route('/FinanceFinal', methods=["POST"])
def FinanceFinal():
  global Id
  AvgReturn=request.form.get('AvgReturnFF')
  AvgIntrest=request.form.get('AvgIntrestFF')
  Inflation=request.form.get('InflationFF')
  title='FinanceFinal'
  y=FinancialFreedomCal(Id, int(AvgReturn), int(AvgIntrest), int(Inflation))
  k=GetFutureNetworth(Id, int(AvgReturn), int(AvgIntrest), y[0])
  Graph3(k)
  if y[0]>=9999:
    msg="You cannot achieve financial independence based on your expense/investment patterns"
  else:
    msg="Congratulations! You will achieve financial independence by Year "+str (y[0]) +"."+"\n"+" You will be "+ str(y[1]) +" years old at this time."
  return render_template('financeFinal.html', title=title , msg=msg ,k=k)

@app.route('/RetirementPlanning', methods=["POST"])
def RetirementPlanning():
  title="Retirement Planning"
  return render_template("retirementPlanning.html",title=title)

@app.route('/RetirementFinal', methods=["POST"])
def RetirementFinal():
  global Id
  AvgReturn=request.form.get("AvgReturnRP")
  AvgIntrest=request.form.get("AvgIntrestRP")
  Inflation=request.form.get("InflationRP")
  retirementAge=request.form.get("RetirementAge")
  LifeExpectancy=request.form.get("LifeExpectancy")
  if LifeExpectancy < retirementAge :
    title="error"
    msg="We received an unexpected value for life expectancy"
    return render_template("errorPostLogin.html",h=msg)
  else:
    title="RetirementFinal"
    y=RetirementPlan(Id,int(AvgReturn),int(AvgIntrest),int(Inflation),int(retirementAge),int(LifeExpectancy))
    k=GetFutureNetworth(Id,int(AvgReturn),int(AvgIntrest),y[1])
    Graph4(k)
    return render_template("retirementFinal.html" , title=title ,y=y ,k=k)


def RegisterCustomer(FirstName, LastName, EmailAddress, Mobile, DOB, Password):
       global Id
       con,MySQLReturnCode,MySQLReturnMessage=mysql_connection()
       if MySQLReturnCode == 'Failure' :
          return(MySQLReturnCode,MySQLReturnMessage)
       try:
          mycursor =con.cursor()
          sql=("select count(*) from customer where emailid=%s")
          mycursor.execute(sql,(EmailAddress,))
          count = mycursor.fetchone()[0]
          if count>0:
              returnCode   = "Failure"
              returnMesage = "Person already Registered"
              return(returnCode, returnMesage)
          sql="select max(CustomerID) from customer"
          mycursor.execute(sql)
          row=mycursor.fetchone()
          if row[0] is None:
            CustomerID=1
          else:
            MaxCustomerID = row[0]
            CustomerID= MaxCustomerID+1
          
          Id=CustomerID
          sql="insert into customer values (%s,%s,%s,%s,%s,%s,%s)"
          values=(CustomerID,FirstName,LastName,EmailAddress,Mobile,DOB,Password)
          mycursor.execute(sql,values)
          con.commit()
       except mysql.connector.Error as error:
          returnCode   = "Failure"
          returnMesage = "Database Call Failed. Contact Technical Support " + format(error)
          return(returnCode, returnMesage)
       except Exception as excp:
          exc_type, exc_obj, exc_traceback = sys.exc_info()
          traceback.print_tb(exc_traceback)
          tb = traceback.extract_tb(exc_traceback)[-1]
          returnCode   = "Failure"
          returnMesage = "Failure in User Registration. Contact Technical Support " + str(exc_obj) + " Error in Linenumber " + str(tb[1]) + " in python program " + str(tb[0])
          return(returnCode, returnMesage)
       returnCode   = "Success"
       returnMesage = FirstName + " " + LastName + " Succcessfully Registered " 
       return(returnCode, returnMesage)

def LoginCustomer( EmailAddress, Password):
       global Id
       global em
       con,MySQLReturnCode,MySQLReturnMessage=mysql_connection()
       if MySQLReturnCode == 'Failure' :
          return(MySQLReturnCode,MySQLReturnMessage)
       try:
          mycursor =con.cursor()
          sql=("select Password from customer where emailid=%s")
          mycursor.execute(sql,(EmailAddress,))
          row =mycursor.fetchone()
          

          if  row is None:
              returnCode   = "Failure"
              returnMesage = "User Not Registered " 
              returnTemplate = "error.html"
              return(returnCode, returnMesage , returnTemplate )
              


          dbPassword = row[0]
          mycursor.execute("select  CustomerId from customer where emailid= %s" , (EmailAddress,))
          fId=mycursor.fetchone()[0]
          if dbPassword==Password:
              returnCode   = "Success"
              returnMesage = "User Successfully logged in " 
              returnTemplate = "form.html"
              Id=fId
              em=EmailAddress
              return(returnCode, returnMesage , returnTemplate )

          else:
              returnCode   = "Failure"
              returnMesage = "Invalid Password Entered"
              returnTemplate = "error.html"
              return(returnCode, returnMesage , returnTemplate ) 
       except mysql.connector.Error as error:
          returnCode   = "Failure"
          returnMesage = "Database Call Failed. Contact Technical Support " + format(error)
          returnTemplate = "error.html"
          return(returnCode, returnMesage, returnTemplate )
       except Exception as excp:
          exc_type, exc_obj, exc_traceback = sys.exc_info()
          traceback.print_tb(exc_traceback)
          tb = traceback.extract_tb(exc_traceback)[-1]
          returnCode   = "Failure"
          returnMesage = "Failure in User Login. Contact Technical Support " + str(exc_obj) + " Error in Linenumber " + str(tb[1]) + " in python program " + str(tb[0])
          returnTemplate = "error.html"
          return(returnCode, returnMesage , returnTemplate )
       

def ImportFinanceData(path,Email):
        con,MySQLReturnCode,MySQLReturnMessage=mysql_connection()
        mycursor =con.cursor()
        sql = ("SELECT CustomerID FROM customer WHERE Emailid = %s")
        mycursor.execute(sql,(Email,))
        CustomerID=mycursor.fetchone()[0]

        sql = ("DELETE FROM financedata where CustomerID = %s")
        mycursor.execute(sql,(CustomerID,))
        con.commit()
        f=open(path,"r",newline="")
        csvreader=csv.reader(f)
        L=[]
        eg=[]
        for row in csvreader:
                L.append(row)

        for i in range(0,len(L)):
                ddmmyyyy = L[i][0]
                
                AccEntryDate = ddmmyyyy[6:10]+'-'+ddmmyyyy[3:5]+'-'+ddmmyyyy[0:2]
                AccEntryItemDesc=L[i][1]
                Amount=L[i][2]
                AccEntryType=L[i][3]
                AccEntrySubType=L[i][4]
                sql="insert into financedata values (%s,%s,%s,%s,%s,%s)"
                values=(CustomerID,AccEntryDate,AccEntryItemDesc,Amount,AccEntryType,AccEntrySubType)
                eg=eg+[values]

        mycursor.executemany(sql,eg)
        con.commit()

        f.close()

def Monthly_ProfileCalculation(CustomerID,Month,Year):
       con,MySQLReturnCode,MySQLReturnMessage=mysql_connection()
       mycursor =con.cursor()
       sql="""SELECT Month(AccEntryDate) as Month, \
                     AccEntryType as Type, \
                     AccEntrySubType as SubType, \
                     Sum(Amount) as Amount \
              FROM financeapp.financedata \
              WHERE
                     CustomerId = %s AND \
                     Month(AccEntryDate) = %s AND \
                     Year(AccEntryDate) = %s AND \
                     AccEntryType != 'One-Time-Expense' \
                     GROUP BY Month, Type, SubType"""
       mycursor.execute(sql,(CustomerID,Month,Year))
       result = mycursor.fetchall()
       
       income=[]
       expense=[]
       title = ('Income','Expenses & Savings')      
       for record in result:
              if  record[1]=="Income":
                     income=income + [ tuple ( [ record[1],record[2],float(record[3]) ] ) ]
              else:
                     expense=expense + [ tuple( [ record[1],record[2],float(record[3]) ] ) ]
       return (title, income,expense)

def Yearly_ProfileCalculation(CustomerID,Year):
       con,MySQLReturnCode,MySQLReturnMessage=mysql_connection()
       mycursor =con.cursor()
       sql="""SELECT Year(AccEntryDate) as Year, \
                     AccEntryType as Type, \
                     AccEntrySubType as SubType, \
                     Sum(Amount) as Amount \
              FROM financeapp.financedata \
              WHERE
                     CustomerId = %s AND
                     Year(AccEntryDate) = %s AND \
                     AccEntryType != 'One-Time-Expense' \
                     GROUP BY Year, Type, SubType"""
       
       mycursor.execute(sql,(CustomerID,Year))
       result = mycursor.fetchall()

       title = ('Income','Expenses & Savings')      

       income=[]
       expense=[]
      
       for record in result:
              if  record[1]=="Income":
                     income=income + [ tuple ( [ record[1],record[2],float(record[3]) ] ) ]
              else:
                     expense=expense + [ tuple( [ record[1],record[2],float(record[3]) ] ) ]
       return (title,income,expense)


def Graph(tup):

    def piechartcreation():
        global keys
        global d
        
        list1=tup
        income=list1[1][0][2]
        expense_nd=list1[2][0][2]
        expense_d=list1[2][1][2]
        investment=list1[2][2][2]
        values=[income,expense_nd,expense_d,investment]

        keys=["Income","Expense(Non discretionary)","Expense(Discretionary)","Investment"]

        d={}
        for i in range(len(values)):
                d[keys[i]]=values[i]

    piechartcreation()

    headers=[[keys[0]],[keys[1],keys[2],keys[3]]]
    parameters= [[d[keys[0]]],[d[keys[1]],d[keys[2]],d[keys[3]]]]

    colors=("#EC6B56","#FFC154","#47B39C")

    wp={'linewidth': 1,'edgecolor':"black"}

     
    def func(pct,allvalues): 
        absolute = int(pct / 100.*np.sum(allvalues)) 
        return"{:.1f}%\n({:d} g)".format(pct, absolute) 

    for i in range(2):
        fig, ax = plt.subplots(figsize =(10, 7))

        wedges, texts, autotexts = ax.pie(parameters[i], 
                                    autopct = lambda pct: func(pct, parameters[i]),  
                                    labels = headers[i],  
                                    colors = colors, 
                                    startangle = 90, 
                                    wedgeprops = wp, 
                                    textprops = dict(color ="black")) 

     
        ax.legend(wedges,headers[i], 
            title ="Key", 
            loc ="center left", 
            bbox_to_anchor =(1,0,0.5,1))

        fig.set_facecolor("black")
        plt.savefig("static/graph"+str(i)+".png")
        
    piechartcreation()


def Graph2(tup):

    def piechartcreation():
        global keys
        global d
        
        list1=tup
        equity=list1[0]
        fixedIncome=list1[1]
        values=[equity,fixedIncome]

        keys=["CurrentEquityNetworth","CurrentFixedIncomeNetworth"]

        d={}
        for i in range(len(values)):
                d[keys[i]]=values[i]

    piechartcreation()

    headers=[[keys[0],keys[1]]]
    parameters= [[d[keys[0]],d[keys[1]]]]

    colors=("#EC6B56","#FFC154","#47B39C")

    wp={'linewidth': 1,'edgecolor':"black"}

     
    def func(pct,allvalues): 
        absolute = int(pct / 100.*np.sum(allvalues)) 
        return"{:.1f}%\n({:d} g)".format(pct, absolute) 

    
    for i in range(1):
        fig, ax = plt.subplots(figsize =(10, 7))

        wedges, texts, autotexts = ax.pie(parameters[i], 
                                    autopct = lambda pct: func(pct, parameters[i]),  
                                    labels = headers[i], 
                                    shadow = True, 
                                    colors = colors, 
                                    startangle = 90, 
                                    wedgeprops = wp, 
                                    textprops = dict(color ="black")) 

     
        ax.legend(wedges,headers[i], 
            title ="Key", 
            loc ="center left", 
            bbox_to_anchor =(1,0,0.5,1))

        fig.set_facecolor("black")
        plt.savefig("static/graph3.png")
      
    piechartcreation()


def Graph3(tup):

    def piechartcreation():
        global keys
        global d
        
        list1=tup
        equity=list1[0]
        fixedIncome=list1[1]
        values=[equity,fixedIncome]

        keys=["FutureEquityNetworth","FutureIncomeNetworth"]

        d={}
        for i in range(len(values)):
                d[keys[i]]=values[i]

    piechartcreation()

    headers=[[keys[0],keys[1]]]
    parameters= [[d[keys[0]],d[keys[1]]]]

    colors=("#EC6B56","#FFC154","#47B39C")

    wp={'linewidth': 1,'edgecolor':"black"}

     
    def func(pct,allvalues): 
        absolute = int(pct / 100.*np.sum(allvalues)) 
        return"{:.1f}%\n({:d} g)".format(pct, absolute) 

    
    for i in range(1):
        fig, ax = plt.subplots(figsize =(10, 7))

        wedges, texts, autotexts = ax.pie(parameters[i], 
                                    autopct = lambda pct: func(pct, parameters[i]),  
                                    labels = headers[i], 
                                    shadow = True, 
                                    colors = colors, 
                                    startangle = 90, 
                                    wedgeprops = wp, 
                                    textprops = dict(color ="black")) 

     
        ax.legend(wedges,headers[i], 
            title ="Key", 
            loc ="center left", 
            bbox_to_anchor =(1,0,0.5,1))

        fig.set_facecolor("black")
        plt.savefig("static/graph4.png")

    piechartcreation()

def Graph4(tup):

    def piechartcreation():
        global keys
        global d
        
        list1=tup
        equity=list1[0]
        fixedIncome=list1[1]
        values=[equity,fixedIncome]

        keys=["FutureEquityNetworth","FutureIncomeNetworth"]

        d={}
        for i in range(len(values)):
                d[keys[i]]=values[i]

    piechartcreation()

    headers=[[keys[0],keys[1]]]
    parameters= [[d[keys[0]],d[keys[1]]]]

    colors=("#EC6B56","#FFC154","#47B39C")

    wp={'linewidth': 1,'edgecolor':"black"}

     
    def func(pct,allvalues): 
        absolute = int(pct / 100.*np.sum(allvalues)) 
        return"{:.1f}%\n({:d} g)".format(pct, absolute) 

    
    for i in range(1):
        fig, ax = plt.subplots(figsize =(10, 7))

        wedges, texts, autotexts = ax.pie(parameters[i], 
                                    autopct = lambda pct: func(pct, parameters[i]),  
                                    labels = headers[i], 
                                    shadow = True, 
                                    colors = colors, 
                                    startangle = 90, 
                                    wedgeprops = wp, 
                                    textprops = dict(color ="black")) 

     
        ax.legend(wedges,headers[i], 
            title ="Key", 
            loc ="center left", 
            bbox_to_anchor =(1,0,0.5,1))

        fig.set_facecolor("black")
        plt.savefig("static/graph5.png")
        
    piechartcreation()


def Networth_Calculation(CustomerID,EquityReturnPct,FixedIncomeInterestPct,Year=0):
       con,MySQLReturnCode,MySQLReturnMessage=mysql_connection()
       mycursor =con.cursor()
       if (Year == 0):
              sql="""SELECT  AccEntryDate,AccEntryItemDesc, Amount,AccEntryType \
                        FROM financeapp.financedata \
                        WHERE  CustomerID = %s AND \
                        AccEntryType IN ( 'Investment' ,'One-Time-Expense') ORDER BY AccEntryDate ASC, AccEntryType DESC"""
              mycursor.execute(sql,(CustomerID,))
       else:
              sql="""SELECT  AccEntryDate,AccEntryItemDesc, Amount,AccEntryType \
                        FROM financeapp.financedata \
                        WHERE  CustomerID = %s AND \
                        Year(AccEntryDate)<=%s AND
                        AccEntryType IN ( 'Investment' ,'One-Time-Expense') ORDER BY AccEntryDate ASC, AccEntryType DESC"""
              mycursor.execute(sql,(CustomerID,Year))
       result = mycursor.fetchall()
       EquityReturn=EquityReturnPct/100
       FixedIncomeInterest=FixedIncomeInterestPct/100
       CurrentEquityNetworth = 0.0
       CurrentFixedIncomeNetworth = 0.0
       for record in result:
              
              if record[1]== 'Equity Investment':
                 CurrentEquityNetworth = CurrentEquityNetworth+ float(record[2])
                 CurrentEquityNetworth = CurrentEquityNetworth*(1 + EquityReturn/12.0)
                            
              elif record[1] == 'Fixed Income Investment (PF/PPF/FDs/Debt MF)':
                            CurrentFixedIncomeNetworth=CurrentFixedIncomeNetworth+float(record[2])
                            CurrentFixedIncomeNetworth = CurrentFixedIncomeNetworth*(1 + FixedIncomeInterest/12.0)
                            
              elif record[1] == 'One-Time-Expense':
                        CurrentEquityNetworth = CurrentEquityNetworth - float(record[2])/2.0
                        CurrentFixedIncomeNetworth = CurrentFixedIncomeNetworth - float(record[2])/2.0
       CurrentEquityNetworth = round(CurrentEquityNetworth,2)
       CurrentFixedIncomeNetworth = round(CurrentFixedIncomeNetworth,2)
       return [CurrentEquityNetworth,CurrentFixedIncomeNetworth,(CurrentEquityNetworth + CurrentFixedIncomeNetworth)]


def GetFutureNetworth(CustomerID,EquityReturnPct,FixedIncomeInterestPct,FutureYear):
       con,MySQLReturnCode,MySQLReturnMessage=mysql_connection()
       mycursor =con.cursor()

       now = datetime.datetime.now()
       CurrentYear = now.year
       sql="""select max(year(AccEntryDate)) from financedata where CustomerId = %s"""
       mycursor.execute(sql, (CustomerID,))
       result = mycursor.fetchall()

       PreviousYear = result[0][0]
       
       BaseYear = PreviousYear - 1
       BaseYearSavings = Yearly_ProfileCalculation(CustomerID,BaseYear)[2][2][2]
       
       PreviousYearSavings = Yearly_ProfileCalculation(CustomerID,PreviousYear)[2][2][2]
       InvestmentGrowthRate = round((PreviousYearSavings-BaseYearSavings)/BaseYearSavings,2)

       sql="""SELECT 
                     AccEntryItemDesc as Type, \
                     Sum(Amount) as Amount \
              FROM financeapp.financedata \
              WHERE
                     CustomerId = %s AND
                     Year(AccEntryDate) = %s AND \
                     AccEntryType = 'Investment' \
                     GROUP BY AccEntryItemDesc"""
       
       mycursor.execute(sql,(CustomerID,PreviousYear))
       result = mycursor.fetchall()
       YearlyEquityInvestment=0
       YearlyFixedIncomeInvestment=0
       for record in result:
              if record[0]=='Equity Investment':
                     YearlyEquityInvestment=float(record[1])
              if record[0]=='Fixed Income Investment (PF/PPF/FDs/Debt MF)':
                     YearlyFixedIncomeInvestment=float(record[1])
       
       EquityReturn = EquityReturnPct/100
       FixedIncomeInterest = FixedIncomeInterestPct/100
       
       Networth = Networth_Calculation(CustomerID,EquityReturnPct,FixedIncomeInterestPct,PreviousYear)
       
       EquityNetworth = Networth[0]
       FixedIncomeNetworth = Networth[1]
       NumOfFutureYears = FutureYear - PreviousYear

       for i in range(NumOfFutureYears):
              YearlyEquityInvestment = YearlyEquityInvestment * (1+InvestmentGrowthRate)
              EquityNetworth = EquityNetworth * (1+EquityReturn) + YearlyEquityInvestment
              YearlyFixedIncomeInvestment = YearlyFixedIncomeInvestment*(1+InvestmentGrowthRate)
              FixedIncomeNetworth = FixedIncomeNetworth * (1+FixedIncomeInterest) + YearlyFixedIncomeInvestment
       return [round(EquityNetworth,2) , round(FixedIncomeNetworth,2) , round((EquityNetworth + FixedIncomeNetworth),2)]

def FinancialFreedomCal(CustomerID,EquityReturnPct,FixedIncomeInterestPct,InflationPct):
       con,MySQLReturnCode,MySQLReturnMessage=mysql_connection()
       mycursor =con.cursor()

       sql="""SELECT Year(DateofBirth) \
              FROM   financeapp.customer \
              WHERE  CustomerId = %s"""
       
       mycursor.execute(sql,(CustomerID,))
       result = mycursor.fetchall()
       YearOfBirth = result[0][0]
       Year100 = YearOfBirth + 100
       
       Inflation = InflationPct/100
       
       now = datetime.datetime.now()
       CurrentYear = now.year
       sql = """select max(year(AccEntryDate)) from financedata where CustomerId = %s"""
       mycursor.execute(sql, (CustomerID,))
       result = mycursor.fetchall()

       PreviousYear = result[0][0]

       BaseYear = PreviousYear - 1
       BaseYearExpense = Yearly_ProfileCalculation(CustomerID,BaseYear)[2][0][2]+Yearly_ProfileCalculation(CustomerID,BaseYear)[2][1][2]
       CurrentYearExpense = BaseYearExpense * ( 1 + Inflation)
       

       EquityReturn = EquityReturnPct/100
       FixedIncomeInterest = FixedIncomeInterestPct/100
       
       CurrentNetworth = Networth_Calculation(CustomerID,EquityReturnPct,FixedIncomeInterestPct)[2]


       if ( (CurrentYearExpense * 25) <=  CurrentNetworth):
       
              return (CurrentYear, CurrentYear - YearOfBirth)

       NextYear = CurrentYear
       NextYearExpense = CurrentYearExpense
       NextYearNetworth = CurrentNetworth
       
       while ( ( (NextYearExpense * 25) >  NextYearNetworth ) and ( NextYear <= Year100 ) ):
              NextYear = NextYear + 1
              NextYearExpense = NextYearExpense * (1 + Inflation)
              NextYearNetworth = GetFutureNetworth(CustomerID,EquityReturnPct,FixedIncomeInterestPct,NextYear)[2]

       if NextYear > Year100 :
              return (9999,99)
       
       AgeWhenFinancialFreedomAchieved = NextYear - YearOfBirth
       return (NextYear,AgeWhenFinancialFreedomAchieved) 



def RetirementPlan(CustomerID,EquityReturnPct,FixedIncomeInterestPct,InflationPct,RetirementAge,LifeExpectancy):
       con,MySQLReturnCode,MySQLReturnMessage=mysql_connection()
       mycursor =con.cursor()

       sql="""SELECT Year(DateofBirth) \
              FROM   financeapp.customer \
              WHERE  CustomerId = %s"""
       
       mycursor.execute(sql,(CustomerID,))
       result = mycursor.fetchall()
       YearOfBirth = result[0][0]
       RetirementYear=YearOfBirth + RetirementAge
       FutureYear=YearOfBirth + LifeExpectancy
       NumberOfyearsInRetirement=LifeExpectancy-RetirementAge
       
       Inflation = InflationPct/100
       
       now = datetime.datetime.now()
       CurrentYear = now.year
       sql = """select max(year(AccEntryDate)) from financedata where CustomerId = %s"""
       mycursor.execute(sql, (CustomerID,))
       result = mycursor.fetchall()

       PreviousYear = result[0][0]
       PreviousYearExpense = Yearly_ProfileCalculation(CustomerID,PreviousYear)[2][0][2]+Yearly_ProfileCalculation(CustomerID,PreviousYear)[2][1][2]
       CurrentYearExpense = PreviousYearExpense * (1 + Inflation)
       RetirementYearExpense = CurrentYearExpense * (1 + Inflation)**(RetirementYear-CurrentYear)
       RetirementYearNetworth = GetFutureNetworth(CustomerID,EquityReturnPct,FixedIncomeInterestPct,RetirementYear)[2]

       EquityReturn = EquityReturnPct/100
       FixedIncomeInterest = FixedIncomeInterestPct/100
       YearsOfStability=RetirementYearNetworth//RetirementYearExpense
       if ( (RetirementYearExpense * NumberOfyearsInRetirement) <=  RetirementYearNetworth):
       
              returntext="You can comfortably Retire at " + str(RetirementAge) + ". You will have " + str(YearsOfStability) + " Years of expenses covered."
       else:
              returntext="You can't Retire at " + str(RetirementAge) + ". You only have " + str(YearsOfStability) + " Years of expenses covered, upto age of " + str(int(RetirementAge+YearsOfStability)) + "."

       return [returntext,RetirementYear]