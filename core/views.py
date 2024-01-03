from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Post, PostImage
from django.contrib.auth import authenticate, login as authlogin, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    try:
        user = request.user

        posts = Post.objects.all().order_by("-id")
        
      
       
       
        if user.is_anonymous == False:
            auth_user = User.objects.filter(id = user.id).first()

            if request.method == 'POST':
                text = request.POST['text']

                if request.FILES.get('photo') is not None:
                    photos = request.FILES.getlist('photo')
                    
                    newpost = Post.objects.create(
                        user = auth_user,
                        text = text
                    )

                    for p in photos:
                       
                       newphoto = PostImage.objects.create(image = p)
                       newpost.images.add(newphoto)
                       newpost.save()
                   
                      
                   
                else:
                    newpost = Post.objects.create(
                        user = auth_user,
                        text = text
                    )

            
            return render(request, 'index.html', {'user': auth_user, 'posts': posts})
        return render(request, 'index.html', {'user': None, 'posts': posts})
        
    except BaseException as e:
         messages.warning(request, e)
         return render(request, 'index.html')


def signup(request):
     try:
        if request.method == 'POST':
          if request.FILES.get("photo") == None:
               messages.warning(request, "upload profile photo")
          elif request.POST['first_name'] == "" or request.POST['last_name'] == "" or request.POST['email'] == "" or request.POST['password'] == "":
              messages.warning(request, "Input fields cannot be empty")
          elif request.POST['password'] != request.POST['repassword']:
              messages.warning(request, "Password Do Not Match")
          elif User.objects.filter(username=request.POST['username']).exists():
              messages.warning(request, "username already exists")
              
          elif User.objects.filter(email=request.POST['email']).exists():
              messages.warning(request, "email taken")
          else:
              user = User.objects.create_user(
                  username = request.POST['username'],
                  first_name = request.POST['first_name'],
                  last_name = request.POST['last_name'],
                  photo = request.FILES['photo'],
                  address = request.POST['address'],
                  phone = request.POST['phone'],
                  email = request.POST['email'],
                  password = request.POST['password']
              )

              user.save()

              auth_user = authenticate(email=request.POST['email'], password=request.POST['password'])
              a = authlogin(request, auth_user)
             



              messages.success(request, "account created successfully")

              return redirect("/")

              

        return render(request, 'signup.html')
     except BaseException as e:
         
         messages.warning(request, e)
         return render(request, 'signup.html')

def login(request):
     try:
         if request.method == 'POST':
             email = request.POST['email']
             password = request.POST['password']
             
             auth_user = authenticate(email = email, password = password)

             if auth_user is not None:
                 authlogin(request, auth_user)
                 
                 return redirect('/')

             else:
                messages.warning(request, "invalid credentials")    

                return redirect('login')

         else:
          return render(request, 'login.html')

     except BaseException as e:
        messages.warning(request, e) 
        return render(request, 'login.html')


@login_required(login_url="/login")
def signout(request):
    logout(request)
    return redirect('/login')
    