from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post
from django.views.decorators.http import require_POST
from .forms import CommentForm
from django.contrib import messages

# Create your views here.

@require_POST
def comment(request,post_pk):
    # 先获取被评论的文章，因为后面需要把评论和对应的文章联系起来
    # 这里我们使用了django提供的一个快捷函数get_object_or_404,
    # 该函数的作用是若有文章(Post)存在则获取内容，没有返回404
    post = get_object_or_404(Post,pk=post_pk)

    # django将用户提交的数据存在request.POST中，这就是一个类字典对象
    # 我们利用这些数据构造了CommentForm的实例，创建了变量保存用户提交的数据
    form = CommentForm(request.POST)

    # 当调用 form.is_vaild()的时候，django会自动检查表单是否符合格式要求
    if form.is_valid():
        # 检查到数据是合法的，调用表单的 save 方法保存到数据库
        # commit=False只用来利用表单生成Comment实例，并且不保存生成的数据
        comment = form.save(commit=False)

        # 将评论和被评论的文章关联起来
        comment.post = post

        # 最后将评论数据保存进数据库，调用模型实例的 save 方法
        comment.save()

        messages.add_message(request,messages.SUCCESS,'评论发表成功！',extra_tags='success')

        # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
        # 就是将 url 定位到该文章
        return redirect(post)

    # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误。
    # 注意这里被评论的文章 post 也传给了模板，因为我们需要根据 post 来生成表单的提交地址。
    context = {
        'post':post,
        'form':form,
    }
    messages.add_message(request,messages.ERROR,'评论发表失败！请修改表单中的错误后重新提交',extra_tags='danger')
    return render(request,'comments/preview.html',context=context)
