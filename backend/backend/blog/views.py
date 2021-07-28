from .models import Post

from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic.edit import FormMixin
from .forms import CommentForm

from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
    context={
        'posts':Post.objects.all()
    }
    return render(request,'blog/blog-home.html',context)



class PostListView(ListView):
    model=Post
    template_name='blog/home.html'
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class= CommentForm
    
    def get_success_url(self):
        return reverse("post-detail", kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
         return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm(initial={
            'post': self.object
        })
        return context
    
    def form_valid(self,form):
        form.instance.author= self.request.user
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.post = self.object
        instance.save()
        return super(PostDetailView, self).form_valid(form)


    

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    def form_valid(self,form):
        form.instance.author= self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
           return True
        return False     


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Post
    success_url='/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
           return True
        return False


def LikeView(request, pk):
   
    post = get_object_or_404(Post, pk=pk)
    post.likes.add(request.user)
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    
    return redirect('post-detail',pk=pk)


def DisLikeView(request, pk):

    post = get_object_or_404(Post, pk=pk)
    post.dislikes.add(request.user)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    return redirect('post-detail', pk=pk)



def about(request):
    return render(request, 'blog/about.html', {'title': 'about'})

def BlogHome(request):
    user=request.user
    return render(request,'blog/index.html',{'user':user})
