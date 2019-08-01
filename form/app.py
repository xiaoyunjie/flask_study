# -*- coding:utf-8 -*-

"""
@Author     :   Browser
@file       :   app.py 
@time       :   2019/07/19
@software   :   PyCharm 
@description:   " "
"""


import os
import uuid
from flask import Flask, url_for, render_template,request,redirect,flash,session,send_from_directory
from forms import LoginForm,FortyTwoForm,UploadForm,MultiUploadForm,RichTextForm,NewPostForm,SigninForm,RegisterForm
from wtforms import ValidationError
from flask_wtf.csrf import validate_csrf
from flask_ckeditor import CKEditor,upload_success,upload_fail
from flask_dropzone import Dropzone

app = Flask(__name__)

app.secret_key = os.getenv('SECRET.KEY','secret string')
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True

app.config['Max_CONTENT_LENGTH'] = 3*1024*1024
app.config['UPLOAD_PATH'] = os.path.join(app.root_path,'uploads')
app.config['ALLOWED_EXTENSIONS'] = ['png','jpg','jpeg','gif']

ckeditor = CKEditor(app)
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload_for_ckeditor'

dropzone = Dropzone(app)
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image'
app.config['DROPZONE_MAX_FILE_SIZE'] = 3
app.config['DROPZONE_MAX_FILES'] = 30

# 默认展示页面
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

# 初始登入页面
@app.route('/html',methods=['GET','POST'])
def html():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form.get('username')
        flash('Welcome home, %s!' % username )
        return redirect(url_for('index'))
    return render_template('pure_html.html')

# 基础登入页面
@app.route('/basic', methods=['GET','POST'])
def basic():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home, %s!' % username)
        return redirect(url_for('index'))
    return render_template('basic.html',form=form)

# bootstrap登入页面
@app.route('/bootstrap',methods=['GET','POST'])
def bootstrap():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home, %s!' % username)
        return redirect(url_for('index'))
    return  render_template('bootstrap.html',form=form)

# 验证器
@app.route('/custom-validator',methods=['GET','POST'])
def custom_validator():
    form = FortyTwoForm()
    if form.validate_on_submit():
        flash('Bingo')
        return redirect(url_for('index'))
    return render_template('custom_validator.html',form=form)

# 文件路径展示
@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'],filename)

# 图片展示
@app.route('/uploaded-images')
def show_images():
    return render_template('uploaded.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename

# 图片上传
@app.route('/upload',methods=['GET','POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'],filename))
        flash('Upload Success!!')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))
    return render_template('upload.html',form=form)

# 多图片上传
@app.route('/multi-upload',methods=['GET','POST'])
def multi_upload():
    form = MultiUploadForm()
    #check csrf
    if request.method == 'POST':
        filenames = []
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash('CSRF token error.')
            return redirect(url_for('multi_upload'))
        # check files
        if 'photo' not in request.files:
            flash('This field is required')
            return redirect(url_for('multi_upload'))
        for f in request.files.getlist('photo'):
            if f and allowed_file(f.filename):
                filename = random_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_PATH'],filename))
                filenames.append(filename)
            else:
                flash('Invalid file type')
                return redirect(url_for('multi_upload'))
        flash('Upload Success!!')
        session['filenames'] = filenames
        return redirect(url_for('show_images'))
    return render_template('upload.html',form=form)

# 富编辑器
@app.route('/ckeditor',methods=['GET','POST'])
def integrate_ckeditor():
    form = RichTextForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        flash('You post is published!')
        return render_template('post.html',title=title,body=body)
    return render_template('ckeditor.html',form=form)

@app.route('/upload-ck', methods=['POST'])
def upload_for_ckeditor():
    f = request.files.get('upload')
    if not allowed_file(f.filename):
        return upload_fail('Image only!')
    f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))
    url = url_for('get_file', filename=f.filename)
    return upload_success(url, f.filename)

# 单表单，多提交按钮
@app.route('/two__submits',methods=['GET','POST'])
def two_submits():
    form = NewPostForm()
    if form.validate_on_submit():
        if form.save.data:
            flash('You click the save button')
        elif form.publish.data:
            flash('You click the publish button')
        return redirect(url_for('index'))
    return render_template('2submit.html',form=form)

# 单页面多表单--单视图
@app.route('/multi_form',methods=['GET','POST'])
def multi_form():
    signin_form = SigninForm()
    register_form = RegisterForm()
    if signin_form.submit1 and signin_form.validate_on_submit():
        username = signin_form.username.data
        flash('%s you just submit signin_form' % username)
        return redirect(url_for('index'))
    if register_form.submit2 and register_form.validate_on_submit():
        username = register_form.username.data
        flash('%s you just submit register_form' % username)
        return redirect(url_for('index'))
    return render_template('2form.html',signin_form=signin_form,register_form=register_form)

# 单页面多表单-多视图
@app.route('/multi_form_multi_view',methods=['GET'])
def multi_form_multi_view():
    signin_form = SigninForm()
    register_form = RegisterForm()
    return render_template('2form2view.html',signin_form=signin_form,register_form=register_form)

@app.route('/handle_signin',methods=['POST'])
def handle_signin():
    signin_form = SigninForm()
    register_form = RegisterForm()
    if signin_form.validate_on_submit():
        username = signin_form.username.data
        flash('%s you just submit signin_form' % username )
        return redirect(url_for('index'))
    return render_template('2form2view.html',signin_form=signin_form,register_form=register_form)

@app.route('/handle_register',methods=['POST'])
def handle_register():
    signin_form = SigninForm()
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        flash('%s you just submit register_form' % username)
        return redirect(url_for('index'))
    return render_template('2form2view.html',signin_form=signin_form,register_form=register_form)


@app.route('/dropzone-upload', methods=['GET', 'POST'])
def dropzone_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'This field is required.', 400
        f = request.files.get('file')

        if f and allowed_file(f.filename):
            filename = random_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        else:
            return 'Invalid file type.', 400
    return render_template('dropzone.html')