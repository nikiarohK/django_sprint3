from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone
from .models import Post, Category


def index(request):
    current_time = timezone.now()

    posts = (
        Post.objects.filter(
            pub_date__lte=current_time,
            is_published=True,
            category__is_published=True
        )
        .select_related("category", "author", "location")
        .order_by("-pub_date")[:5]
    )

    context = {"posts": posts}
    template = "blog/index.html"
    return render(request, template, context)


def post_detail(request, pk):
    template = "blog/detail.html"

    post = get_object_or_404(Post, pk=pk)

    current_time = timezone.now()

    if (
        post.pub_date > current_time
        or not post.is_published
        or not post.category.is_published
    ):
        raise Http404("Публикация не найдена или недоступна")

    context = {"post": post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = "blog/category.html"

    current_time = timezone.now()

    category = get_object_or_404(Category, slug=category_slug)

    if not category.is_published:
        raise Http404("Категория не опубликована")

    posts = Post.objects.filter(
        category=category, is_published=True, pub_date__lte=current_time
    )
    context = {"category": category, "posts": posts}
    return render(request, template, context)
