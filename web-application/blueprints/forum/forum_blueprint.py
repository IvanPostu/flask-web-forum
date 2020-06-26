from flask import Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import BaseQuery
from flask_security import login_required

from typing import AnyStr

from models import Post, Tag
from .forms import PostForm
from app import db

forum = Blueprint('forum', __name__, template_folder='templates')


@forum.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except Exception:
            print('Something wrong!')

        return redirect(url_for('forum.index'))

    form = PostForm()
    return render_template('forum/create_post.html', form=form)


@forum.route('/<slug>/edit/', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    post_query: BaseQuery = Post.query
    post = post_query.filter(Post.slug == slug).first_or_404()

    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()

        return redirect(url_for('forum.post_detail', slug=post.slug))

    form = PostForm(obj=post)
    return render_template('forum/edit_post.html', post=post, form=form)


@forum.route('/')
def index():

    q = request.args.get('q')
    page: AnyStr = request.args.get('page')

    posts: BaseQuery

    if page and page.isdigit():
        page_number: int = int(page)
    else:
        page_number: int = 1

    if q:
        posts = Post.query.filter(Post.title.contains(
            q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())

    pages = posts.paginate(page=page_number, per_page=5)

    return render_template('forum/index.html', pages=pages)


@forum.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    tags = post.tags
    return render_template('forum/post_detail.html', post=post, tags=tags)


@forum.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    posts_query: BaseQuery = tag.posts
    posts = posts_query.all()
    return render_template('forum/tag_detail.html', tag=tag, posts=posts)
