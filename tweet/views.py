from django.shortcuts import render,redirect
from .models import Tweet
from .forms import TweetForm , UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages 
from django.db.models import Q


# Create your views here.
def home(request):
    return render(request,'index.html')

def tweet_list(request): 
    tweets = Tweet.objects.all().order_by('-created_at')  #we can called tweets object
    return render(request,'tweet_list.html',{'tweets':tweets})

@login_required
def profile(request): 
    tweets = Tweet.objects.filter(user =request.user)
    return render(request,'profile.html',{'tweets':tweets})

@login_required
def tweet_create(request):
    if request.method == "POST": 
       form=TweetForm(request.POST,request.FILES)
       if form.is_valid():
           tweet=form.save(commit=False)
           tweet.user=request.user
           tweet.save()
           return redirect('tweet_list')
    else:
       form =TweetForm()
    return render(request,'tweet.form.html',{'form':form})

@login_required
def tweet_edit(request,tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id,user =request.user)
    if request.method == 'POST':
       form = TweetForm(request.POST,request.FILES,instance=tweet)
       if form.is_valid():
           tweet=form.save(commit=False)
           tweet.user=request.user
           tweet.save()
           return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request,'tweet.form.html',{'form':form})

@login_required
def tweet_delete(request,tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',{'tweet':tweet})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password1','password2'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
         form = UserRegistrationForm()

    return render(request,'registration/register.html',{'form':form })
    
def tweet_like(request,pk):
    if request.user.is_authenticated:
        tweet= get_object_or_404(Tweet,id=pk)
        if tweet.likes.filter(id = request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        return redirect('tweet_list')
    else:
        messages.success(request,("You Must Be Logged In "))
        return redirect('register')   
       
def search_results(request):
    query = request.GET.get('q')
    if query:
        results = Tweet.objects.filter(
            Q(text__icontains=query) |  # Searching in text field
            Q(user__username__icontains=query) |  # Searching in user's username
            Q(photo__icontains=query) |  # Searching in photo (if it's a text field or caption)
            Q(created_at__icontains=query)  # Searching by date
        )
    else:
        results = Tweet.objects.none()
    
    return render(request, 'search_results.html', {'results': results, 'query': query})

