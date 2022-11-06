from flasketeer import app
from flasketeer.models import Users, Posts, Contact
from flasketeer.forms import RegisterForm, LoginForm, PostForm, EditForm, ContactForm
from flasketeer import db
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
def home_page():
    articles = Posts.query.all()
    return render_template('index.html', articles=articles, preview=preview_article)


def preview_article(article):
    word_list = article.splitlines()
    word_preview = ' '.join(word_list[:2]) + '...'
    return word_preview

@app.route('/article/<int:article_id>')
def article_page(article_id):
    article = Posts.query.filter_by(id=article_id).first()
    user = Users.query.filter_by(id=article.user_id).first()
    return render_template('article.html', article=article, user=user)


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post_page():
    user_id = current_user.id
    username = current_user.username
    form = PostForm()
    if form.validate_on_submit():
        post_to_create = Posts(post_title=form.post_title.data,
                               post_content=form.post_content.data,
                               user_id=user_id,
                               author=username)
        db.session.add(post_to_create)
        db.session.commit()
        flash('Successfully created post!', category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error signing you up: {err_msg}', category='danger')

    return render_template('post.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = Users(username=form.username.data,
                               firstname=form.firstname.data,
                               lastname=form.lastname.data,
                               email_address=form.email_address.data,
                               password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Welcome to the community {user_to_create.firstname}!', category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error signing you up: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Users.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correctness(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password do not match! Please try again', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out', category='info')
    articles = Posts.query.all()
    return render_template('index.html', articles=articles, preview=preview_article)


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/delete/<int:delete_id>/', methods=['GET'])
@login_required
def delete_page(delete_id):
    article_to_delete = Posts.query.filter_by(id=delete_id).first()

    if current_user.username == article_to_delete.author:
        db.session.delete(article_to_delete)
        db.session.commit()
        flash("Your article has successfully been deleted!", category='success')
        return redirect(url_for('home_page'))
    else:
        flash('Something went wrong lease try agan later', category='danger')


@app.route('/edit/<int:edit_id>', methods=['GET', 'POST'])
def edit_page(edit_id):
    article_to_edit = Posts.query.filter_by(id=edit_id).first()

    if current_user.username != article_to_edit.author:
        flash('You cannot delete another user\'s post!', category='info')
        return redirect(url_for('home_page'))

    form = EditForm()
    form.post_content.data = article_to_edit.post_content

    if form.validate_on_submit():
        article_to_edit.post_title = form.post_title.data
        article_to_edit.post_content = form.post_content.data
        db.session.commit()
        flash('Successfully edited your post!', category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error signing you up: {err_msg}', category='danger')

    return render_template('edit.html', form=form, id=edit_id, prev_article=article_to_edit)


@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    form = ContactForm()
    if form.validate_on_submit():
        message_to_store = Contact(name=form.name.data,
                                   email_address=form.email_address.data,
                                   subject=form.subject.data,
                                   message=form.message.data)
        db.session.add(message_to_store)
        db.session.commit()
        flash('Your message has been successfully sent', category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error sending your message: {err_msg}', category='danger')
    return render_template('contact.html', form=form)

# @app.route("/ajaxlivesearch",methods=["POST","GET"])
# def ajaxlivesearch():
#     if request.method == 'POST':
#         search_word = request.form['query']
#         print(search_word)
#         if search_word == '':
#             article = Posts.query.filter_by(post_title=search_word)
#         else:
#             cur.execute('SELECT * FROM employee WHERE name LIKE %(name)s', { 'name': '%{}%'.format(search_word)})
#             numrows = int(cur.rowcount)
#             employee = cur.fetchall()
#             print(numrows)
#     return jsonify({'htmlresponse': render_template('response.html', articles=articles, numrows=numrows)})
