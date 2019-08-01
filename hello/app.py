# -*- coding:utf-8 -*-

"""
@Author     :   Browser
@file       :   tm.py
@time       :   2019/07/05
@software   :   PyCharm 
@description:   " "
"""


from flask import Flask,jsonify,make_response,url_for,redirect,request,session,abort,render_template,flash
from flask_login import LoginManager
from jinja2.utils import generate_lorem_ipsum
from jinja2 import escape,environment
import  os



app = Flask(__name__)

app.secret_key = os.getenv('SECRET.KEY','34LTPUKNvlb6P8K6') #第二个参数为默认值
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登入'

@app.route('/')
def hello():
    # return "<h1>hello flask</h1>"
    return render_template('a.html',name2='park')

### application/json
@app.route('/foo')
def foo():
    return jsonify({'name':'browser','gender':'male'})

### copkie
@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('cookie')))
    response.set_cookie('name',name)
    return response

@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('cookie'))

@app.route('/cookie')
def cookie():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name','browser')
        response =  '<h1>hello,%s</h1>' % name
    #根据认证状态返回不同结果
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return  response

@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page'

@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('cookie'))

#ajax
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''
    <h1>A very long post</h1>
    <div class="body">%s</div>
    <button id="load">Load More</button>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script type="text/javascript">
    $(function() {
        $('#load').click(function(){
            $.ajax({
                url: '/more',
                type: 'get',
                success: function(data){
                    $('.body').append(data);
                }
            })
        })
    })
    </script>''' % post_body

@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)

# xss
@app.route('/xss')
def xss_test():
    xssname = request.args.get('name')
    result = '<h1>Hello,%s!</h1>' % xssname
    # result = '<h1>Hello,%s!</h1>' % escape(xssname)
    return result

@app.route('/flash')
def show_flash():
    flash('my name is browser')
    return redirect(url_for('hello'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html')



from templates.tm import   musical

