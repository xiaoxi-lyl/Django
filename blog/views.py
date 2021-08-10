from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
import markdown
from .models import Post,Category,Tag
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# Create your views here.
# 主页视图函数
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request,'blog/index.html',context={
        'post_list':post_list
    })

# 详情页函数
def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    md = markdown.Markdown(extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 'markdown.extensions.toc',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>',md.toc,re.S)
    post.toc = m.group(1) if m is not None else ''
    post.toc = md.toc
    return render(request,'blog/detail.html',context={'post':post})

# 归档和分类视图函数
def archive(request,year,month):
    post_list = Post.objects.filter(create_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

# 分类页面
def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

# 标签页面
def tag(request,pk):
    t = get_object_or_404(Tag,pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})