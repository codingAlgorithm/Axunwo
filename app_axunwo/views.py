from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response

from app_axunwo import validator
from .forms import LoginForm
from .forms import SignupForm
from .forms import PostForm
from .models import NewUser, RentPost
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as checkLogin
import datetime
from .models import Document
from .forms import DocumentForm
from django.core.urlresolvers import reverse


# Create your views here.

def index(request):
    return render(request, 'index.html')


def logmeout(request):
    logout(request)
    return render(request, 'index.html')

#
# def login(request):
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = LoginForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             username = form
#             return HttpResponseRedirect('/')
#
#             # if a GET (or any other method) we'll create a blank form
#     else:
#         form = LoginForm()

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect('/upload/')
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(request, 'list.html', {'documents': documents, 'form': form})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            checkLogin(request, user)
            return HttpResponseRedirect('/')
        else:
            request.method = 'GET'
            return render(request, 'login.html', {'error': "password or username is not correct!"})


def signup(request):
    if request.method == 'GET':
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        user = NewUser(username=user_name, password=pass_word)
        user.set_password(user.password)
        user.save()
        return HttpResponse(user_name)


def search(request):
    if request.method == 'GET':
        all_post = RentPost.objects.all()

        for post in all_post:
            photo_urls = []
            photos = post.photo_list.split(',')
            year = photos[0].split('-')[1]
            month = photos[0].split('-')[2]
            day = photos[0].split('-')[3]
            for photo in photos:
                photo_urls.append("documents/" + year + "/" + month + "/" + day + "/" + photo)
            post.photo_list = photo_urls
        return render(request, 'search.html', {'allpost': all_post})


@login_required
def post(request):
    errors = []
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        current_user = request.user
        content = request.POST.get('post_content')
        atime = request.POST.get('post_time')
        ctime = datetime.datetime.now().strftime("%Y-%m-%d")
        title = request.POST.get('post_title')
        price = request.POST.get('post_price')
        post_bedroom = request.POST.get('post_bedroom')
        post_bathroom = request.POST.get('post_bathroom')
        location = request.POST.get('post_address')
        type = request.POST.get('post_type')
        rentway = request.POST.get('rent_way')
        dog = request.POST.get('post_dog') == 'on'
        cat = request.POST.get('post_cat') == 'on'
        pool = request.POST.get('post_pool') == 'on'
        gym = request.POST.get('post_gym') == 'on'
        wechat = request.POST.get('post_wechat')
        phone = request.POST.get('post_phone')

        if validator.validatePost():
            paths = []
            files = request.FILES.getlist('files')
            current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            i = 0
            for file in files:
                file.name = current_user.username + "-" + current_time + "-" + str(i) + "." + file.name.split(".")[-1]
                i += 1
                paths.append(file.name)
                newdoc = Document(docfile=file)
                newdoc.save()
                photolist = ','.join(paths)

            mypost = RentPost(post_content = content, post_title = title, photo_list = photolist, post_price = price,
                              post_bedroom = post_bedroom, post_bathroom = post_bathroom, post_address = location,
                              post_type = type, post_rentway = rentway, post_pool = pool, post_gym = gym, post_cat_allowed = cat,
                              post_dog_allowed = dog, post_wechat = wechat, post_phone = phone, post_available_time = atime,
                              post_time = ctime, user = current_user)
            mypost.save()

            return HttpResponse(photolist)

        else:
            return HttpResponse("error")
    else:
        return render(request, 'post.html', {'errors': errors})

        # current_user = request.user
        # forms = PostForm(request.POST)
        # if forms.is_valid():
        #     instance = forms.save(commit=False)
        #     instance.user = current_user
        #     instance.post_time = datetime.datetime.now()
        #     instance.save()

        # content = request.Post.get('post_content')
        # time =  request.Post.get('post_time')
        # title = request.Post.get('post_title')
        # photolist = request.Post.get('photo_list')
        # price = request.Post.get('post_price')
        # status = request.Post.get('post_status')
        # post_bedroom = request.Post.get('post_bedroom')
        # post_bathroom = request.Post.get('post_bathroom')
        # location = request.Post.get('post_location')
        # zipcode = request.Post.get('post_zipcode')
        # available_time = request.Post.get('post_available_time')
        # sqft = request.Post.get('post_sqft')
        # type = request.Post.get('post_type')
        # rent_way = request.Post.get('rent_way')
        # bus = request.Post.get('post_bus')
        # subway = request.Post.get('post_subway')
        # dog = request.Post.get('post_dog_allowed')
        # cat = request.Post.get('post_cat_allowed')
        # pool = request.Post.get('post_pool')
        # gym = request.Post.get('post_gym')
        # post = RentPost(content = content, time = time, title = title, photolist = photolist, price = price, status = status, post_bedroom = post_bedroom, post_bathroom = post_bathroom, location = location , zipcode = zipcode, available_time = available_time, sqft = sqft, type = type, rent_way = rent_way
        #                 ,bus = bus, subway = subway, dog = dog, cat = cat, pool = pool, gym = gym)
        # post.save()
        # return HttpResponse(content, price)


        # create a form instance and populate it with data from the request:
        # form = PostForm(request.POST)
        # # check whether it's valid:
        # if form.is_valid():
        #
        #     # process the data in form.cleaned_data as required
        #     # ...
        #     # redirect to a new URL:

        #         if a GET (or any other method) we'll create a blank form


def account(request):
    return render(request, 'login.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')



