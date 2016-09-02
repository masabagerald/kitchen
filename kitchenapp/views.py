from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
from kitchenapp.bing_search import run_query
from kitchenapp.models import Category,Food
from  django.contrib.auth import  authenticate,login,logout

from datetime import datetime

def index(request):


    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.


        # Query the database for a list of ALL categories currently stored.
        # Order the categories by no. likes in descending order.
        # Retrieve the top 5 only - or all if less than 5.
        # Place the list in our context_dict dictionary which will be passed to the template engine.

        request.session.set_test_cookie()


        category_list = Category.objects.order_by('-likes')[:5]
        food_list = Food.objects.order_by('-views')[:5]


        context_dict = {'categories': category_list,'food':food_list}

        #visits = int(request.COOKIES.get('visits','1'))

        visits = request.session.get('visits')
        if not visits:
            visits = 1


        reset_last_visit_time = False


        last_visit = request.session.get('last_time')
        if last_visit:
           # last_visit = request.COOKIES['last_visit']
            last_visit_time = datetime.strptime(last_visit[:-7],"%y-%m-%d %H:%m:%s")

            if(datetime.now() - last_visit_time).seconds > 0:
                visits = visits + 1
                reset_last_visit_time = True
        else:

            reset_last_visit_time = True

            #context_dict['visits'] = visits



        if reset_last_visit_time:

            request.session['last_visit'] = str(datetime.now())
            request.session['visits'] = visits

            #response.set_cookie('last_vistit',datetime.now())
            #response.set_cookie('visits',visits)
        context_dict['visits'] = visits

        response = render(request,'kitchenup/index.html',context_dict)


        # Render the response and send it back!

        return response

def category(request,category_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug = category_slug)
        context_dict['category_name'] = category.name

        foods = Food.objects.filter(category=category)

        context_dict['foods'] = foods

        context_dict['category'] = category

        context_dict['slug'] = category_slug

    except Category.DoesNotExist:

        pass
    return render(request,'kitchenup/category.html',context_dict)







from kitchenapp.forms import CategoryForm,FoodForm,UserForm,UserProfileForm




def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'kitchenup/add_category.html', {'form': form})

def add_food(request,category_slug):
    try:
        cat = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        cat = None

    if  request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():

            if cat:
                page = form .save(commit = False)
                page.category = cat
                page.views=0
                page.save()

                return category(request,category_slug)
        else:

            print form.errors

    else:
        form = FoodForm()
    context_dic  ={'form':form,'category':cat}

    return render(request,'kitchenup/add_food.html',context_dic)



def register(request):

    if request.session.test_cookie_worked():
        print ">>> test cookie worked"

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data= request.POST)
        profile_form = UserProfileForm(data= request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile .save()
            registered = True

        else:
            print user_form.errors,profile_form.errors


    else:
        user_form = UserForm()
        profile_form = UserProfileForm()




    return render(request,
                  'kitchenup/register.html',
                  {'user_form':user_form,'profile_form':profile_form ,'registered':registered},
    )

def search(request):
    result_list = []

    if request.method =='post':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)

    return render(request,'kitchenup/search.html',{'result_list':result_list})


def signin(request):


    if request.method == 'post':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user  = authenticate(username=username,password =password)

        if user is not None:

            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/kitchen/')
            else:
                return HttpResponse("your account is disabled")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:

        return render(request,'kitchenup/login.html',{})

@login_required
def restricted(request):
    return HttpResponse("you are logged in")

@login_required
def signout(request):
    logout(request)

    return HttpResponseRedirect('/kitchen/')

@login_required
def like_category(request):

    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0;
    if cat_id:
        cat = Category.objects.get(id =int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()

    return HttpResponse(likes)
