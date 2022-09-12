from django.shortcuts import render,redirect
import pymongo
import bcrypt
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mpld3
salt=bcrypt.gensalt()
def checkdb(user,pwd):
    myclient= pymongo.MongoClient("mongodb://localhost:27017/")
    mydb=myclient['newdatabase']
    mycol=mydb['user_pass']
    myquery={'name':user,'pass':pwd}
    if mycol.count_documents({'name':user},limit=1):
        return 'Username already taken try different one'
    else:
        mycol.insert_one(myquery)
        return 'Record stored successfully login now'
def checkdb1(user,pwd):
    myclient= pymongo.MongoClient("mongodb://localhost:27017/")
    mydb=myclient['newdatabase']
    mycol=mydb['user_pass']
    docs=mycol.find({},{'pass':1,'_id':0})
    if mycol.count_documents({'name':user},limit=1):
        for i in docs:
            if bcrypt.checkpw(pwd, i['pass']):
                return True
        return False
    else:
        return False
    # Create your views here.
def home(request):
    if request.POST.get('register',False):
        usr=request.POST['fname']
        pw=request.POST['pass']
        pw= pw.encode("UTF-8")
        hashed_pw = bcrypt.hashpw(pw, bcrypt.gensalt())
        print(usr,hashed_pw)
        info=checkdb(usr,hashed_pw)
        return render(request,'index.html',{'info':info,'register':True})
    elif request.POST.get('login',False):
        usr=request.POST['fname1']
        pw=request.POST['pass1']
        pw= pw.encode("UTF-8")
        if(checkdb1(usr,pw)):
            global data
            data="Welcome %s"%(usr)
            print(data)   
            return render(request,'result2.html',{'info':data,'login':True})
        else:
            data='Please register credential not found/Invalid username/password'
            return render(request,'index.html',{'info':data,'login':True})

    else:
        print('enter last else')
        if request.POST.get('corr',False):
            val1=request.POST['num1']
            val2=request.POST['num2']
            x=[int(i) for i in val1.split()]
            h=[int(i) for i in val2.split()]
            h1=h[::-1]
            re=np.convolve(x,h1)
            n= [i for i in range(len(re))]
            fig = plt.figure()
            plt.stem(n,re)
            plt.xlabel('Time-->')
            plt.ylabel('Amplitude-->')
            plt.title('Cross correlated sequences')
            html_graph = mpld3.fig_to_html(fig)
            return render(request,'result2.html',{'res':re,'graph':[html_graph],'info':data,'corr':True})
        elif request.POST.get('conv',False):
            val1=request.POST['num1']
            val2=request.POST['num2']
            x=[int(i) for i in val1.split()]
            h=[int(i) for i in val2.split()]
            re=np.convolve(x,h)
            n= [i for i in range(len(re))]
            fig = plt.figure()
            plt.stem(n,re)
            plt.xlabel('Time-->')
            plt.ylabel('Amplitude-->')
            plt.title('Linear Convolved sequence')
            html_graph = mpld3.fig_to_html(fig)
            return render(request,'result2.html',{'res':re,'graph': [html_graph],'info':data,'conv':True})
        elif request.POST.get('fft',False):
            print('enter')
            val1=request.POST['num1']
            x=[int(i) for i in val1.split()]
            print(x)
            X=np.fft.fft(x)
            return render(request,'result2.html',{'res':X,'info':data,'fft':True})
        return render(request,'index.html')
# def result(request):
#     if request.POST.get('conv',False):
#         val1=request.POST['num1']
#         val2=request.POST['num2']
#         print(int(val1)+int(val2))
#         re=int(val1)+int(val2)
#         return render(request,'result2.html',{'res':re,'conv':True})
#     elif request.POST.get('fft',False):
#         val1=request.POST['num1']
#         val2=request.POST['num2']
#         re=int(val1)-int(val2)
#         return render(request,'result2.html',{'res':re,'fft':True})
#     else:
#         data='no permission register'
#         return render(request,'index.html',{'res':data})

def logout(request):
    print('enter')
    return redirect('/')