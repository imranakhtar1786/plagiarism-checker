from django.shortcuts import render,HttpResponseRedirect
import docx2txt
import datetime
import requests
from bs4 import BeautifulSoup
import trafilatura
import random
import django
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success,error
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from .models import *
from django.contrib.auth.models import User
from .plag_checker import main

# def get_useragent():
#     _useragent_list = [
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
#         'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
#     ]
#     return random.choice(_useragent_list)

# def split_in_sentences(text):
#     sentences=[x.strip() for x in text.strip().replace('\n', '').split(". ")]
#     return sentences


# def generate_shingles(text, k):
#     shingles = set()
#     text = text.lower().split()  # Convert text to lowercase and split into words
#     for i in range(len(text) - k + 1):
#         shingle = ' '.join(text[i:i + k])  # Join k consecutive words to form a shingle
#         shingles.add(shingle)
#     return shingles


# def similarity(set1, set2):
#     intersection = len(set1.intersection(set2))
#     try:
#         return  (intersection / len(set1))*100
#     except:
#         return 0
# def similarity_score(input_text, collected_text, k=3):
    
#     shingles1 = generate_shingles(input_text, k)
#     shingles2 = generate_shingles(collected_text, k)
#     similarity_score = similarity(shingles1, shingles2)
#     return similarity_score


# def get_content(url):
#     for i in range(3):
#         download= trafilatura.fetch_url(url)
#         content=trafilatura.extract(download, include_comments=False, include_tables=False)
#         if content:
#             return content
        
#         elif i==2 and content is None:
#             return ''
        

# def google_search(query):
#     links=[]
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}

#     # Perform a Google search
#     response = requests.get(
#                         url="https://www.google.com/search",
#                         headers={"User-Agent": get_useragent()},
#                         params={"q": f'"{query}"',
#                                 "num": 5,  # Prevents multiple requests
#                                 "hl": 'en'})

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Extract and print search results
#         search_results = soup.find_all('h3')
#         for idx, result in enumerate(search_results, start=1):
#             link = result.find_parent('a')
#             if link:
#                 link_text = link.get('href')
#                 if link_text and link_text.startswith('http'):
#                     links.append(link_text)         
#     else:
#         print("Failed to perform the Google search.")
#     return links #list of links


# def get_results(sentences):
    
#     sources={}

#     for sentence in sentences:

#         serp_urls=google_search(sentence)
#         #print(sentence)
#         temp={}
#         for url in serp_urls:
#             content=get_content(url)
#             sentence_score = similarity_score(sentence, content)
#             temp[url] = int(sentence_score)
#         #print(temp)
#         max_score_url=max(temp, key=temp.get)
#         max_score=temp[max_score_url]

#         current_score={'url':max_score_url, 'score':max_score}
            
#         if sources:
#             last_sentence=list(sources.keys())[-1]
#             last_url=sources[last_sentence]['url']
#             last_url_score=sources[last_sentence]['score']
#             if last_url==max_score_url:
#                 combined_sentence = last_sentence + ". " + sentence
#                 sources[combined_sentence] = {'url':max_score_url, 'score':int((max_score+last_url_score)/2)} #(current_score['score']+last_url_score)/2
                
#                 del sources[last_sentence]
#             else:
#                 sources[sentence] = current_score
#         else:
#             sources[sentence] = current_score
    
#     return sources



# from datetime import datetime

# def plagiarism_checker(input_text):
#     sentences=split_in_sentences(input_text)

#     print("Time =", datetime.now().strftime("%H:%M:%S"))
#     result=get_results(sentences)
#     print("scores Time =", datetime.now().strftime("%H:%M:%S"))
#     # print(result)
#     return result


# def get_raw_result(input_text):
    
#     text=""
#     try:
#         result =plagiarism_checker(str(input_text))
#         all_scores=[]
#         for key, value in result.items():
#             text+=f'\n{"-"}\nSentence: {key} \nSource: {value["url"]} \nText Maches: {value["score"]}%'
#             all_scores.append(value['score'])
#         if all_scores:
#             total_score=sum(all_scores)/len(all_scores)
#         #if total_score:
#             text+=(f'\n\nUnique: {int(100-total_score)}%   &   Plagiarism: {int(total_score)}%')
#     except Exception as e:
#         text=f'Error:{e}'

#     return text


# if __name__ == "__main__":
    
#     input_text=input("Enter The Text: ")
#     print("Working...")
#     final_output=get_raw_result(input_text)
#     print(final_output)



def homepage4(Request):
    return render(Request,'index.html')

@login_required(login_url="/login/")
def plag(Request):
    if Request.method=="POST":
        try:
            try:
                doc=Request.FILES.get("doc")
                index=str(doc)
                text=docx2txt.process(doc)
                text=" ".join(text.split()[0:200])
            except:
                text=Request.POST.get("text")
                text=" ".join(text.split()[0:200])
                index=text[0:50]
            print(text)
            #a=plagiarism_checker(text)
            a=main(text)
            print(a)
            per=0
            url=""
            length=0
            for i in a.values():
                #if i["score"]>0:
                per=per+i["score"]
                length+=1
            per=round(per/length)
            history=Request.session.get("history",None)
            if(history==None):
                Request.session["history"]=[]
                Request.session.set_expiry(60*60*24*7)
            his=[datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S"),per,index]
            print(his)
            Request.session["history"] +=[his]
            print("percentage",per,url)
        except:
            index=None
            url=None
            per=None
            a=None
        return render(Request,'index.html',{"key":index,"score":per,"a":a})

def loginpage(Request):
    if (Request.method=="POST"):
        password=Request.POST.get("password")
        username=Request.POST.get("username")
        user=authenticate(username=username,password=password)
        if(user is not None):
            login(Request,user)
            if(user.is_superuser):
                return HttpResponseRedirect("/admin/")
            else:
                print("login")
                return HttpResponseRedirect("/")
        else:
            print("error")
            error(Request,"Invalid Username or Password!!")   
    return render(Request,"login.html")

@login_required(login_url="/login/")
def logoutpage(Request):
    logout(Request)
    return HttpResponseRedirect("/login/")

def signup(Request):
    try:
        if (Request.method=="POST"):
            password=Request.POST.get("password")
            cpassword=Request.POST.get("cpassword")
            if(password==cpassword):
                name=Request.POST.get("name")
                username=Request.POST.get("username")
                phone=Request.POST.get("phone")
                email=Request.POST.get("email")
                try:
                    UserAccount.objects.get(email=email)
                    error(Request,"Email Already Exist")
                    return HttpResponseRedirect("/signup/")
                except:
                    pass
                otp=randint(100000,999999)
                subject = 'OTP For SIGNUP !!! PLAGCHEKER'
                message ="""Hello """+ name +""",\n"""+"""OTP For Account Create Is """+str(otp)+""". Please Never Share Your OTP With Anyone."""
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail( subject, message, email_from, recipient_list )
                user=[name,username,phone,email,otp,password]
                Request.session["user"]=user
                Request.session.set_expiry(60*60*24*7)
                return HttpResponseRedirect("/otp-Verifying/")
            else:
                error(Request,"Password and Confirm Password Doesn't Match")
    except:
        pass
    return render(Request,"signup.html")

def otp(Request):
    try:
        if (Request.method=="POST"):
            usera=Request.session.get("user")
            otp=int(Request.POST.get("otp"))
            if otp==usera[4]:
                User.objects.create_user(username=usera[1],password=usera[5],email=usera[3],first_name=usera[0])
                u=UserAccount()
                u.name=usera[0]
                u.username=usera[1]
                u.email=usera[3]
                u.phone=usera[2]
                u.save()
                del Request.session["user"]
                success(Request,"Account is Created")
                return HttpResponseRedirect("/login/")
            else:
                error(Request,"Invalid OTP")
    except:
        pass
    return render(Request,"otp.html")

@login_required(login_url="/login/")
def history(Request):
    try:
        history=Request.session["history"]
        history.reverse()
    except:
        history=[]
    return render(Request,"history.html",{"history":history})

