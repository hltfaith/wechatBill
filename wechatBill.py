from flask import Flask, render_template, request, jsonify, session, redirect, url_for, Markup, send_from_directory
from werkzeug.utils import secure_filename
import os
import json
import markdown

from getData import getfile, createDB
import querydb
from changeFile import reductionFile, indexjs, columnarjs, piejs, wxbillmd
from page_utils import Pagination
from tool.analyseTools import set_access_count, export_bill_docx

app = Flask(__name__)
app.secret_key = 'password'


def boot():
    '''
    前端 JS 文件修改
    :return:
    '''

    # index首页 Chart JS 图表数据加载
    indexjs()
    columnarjs()
    piejs()
    wxbillmd()


def login_required(func):

    def wrapper():

        if session.get('username') == 'changhao' and session.get('password') == 'changhao':
            return func()

    return wrapper


@app.route("/")
def index():
    '''
    首页 - 支出预览
    :return:
    '''

    if session.get('username') == 'changhao' and session.get('password') == 'changhao':

        if not len(getfile()) >= 1:
            return redirect(url_for('upload'))

        db = querydb.DBAPI()

        # 总支出金额
        zcyl_zzc = db.queryForeEnd('zcyl_zzc')

        # 总收入金额
        zcyl_zsr = db.queryForeEnd('zcyl_zsr')

        # 单笔最高支出
        zcyl_dbzgzc = db.queryForeEnd('zcyl_dbzgzc')

        # 单笔最高收入
        zcyl_dbzgsr = db.queryForeEnd('zcyl_dbzgsr')

        # 单笔最高支出百分比
        zcyl_dbzgzcbfb = db.queryForeEnd('zcyl_dbzgzcbfb')

        # 单笔最高收入百分比
        zcyl_dbzgsrbfb = db.queryForeEnd('zcyl_dbzgsrbfb')

        # 消费活跃区域 TOP10
        xfcity = db.queryFootmark('footmark_10top')

        # TOP10 消费清单
        zcyl_xftop10 = db.queryForeEnd('zcyl_xftop10')

        return render_template('index.html', zcyl_zzc=round(zcyl_zzc, 2), zcyl_zsr=round(zcyl_zsr, 2),
                               zcyl_dbzgsr=zcyl_dbzgsr, zcyl_dbzgzc=zcyl_dbzgzc,
                               zcyl_dbzgzcbfb=zcyl_dbzgzcbfb, zcyl_dbzgsrbfb=zcyl_dbzgsrbfb,
                               xfcity=xfcity, zcyl_xftop10=zcyl_xftop10)

    return redirect(url_for('login'))


@app.route("/login", methods=["POST", "GET"])
def login():
    '''
    登录页面
    :return:
    '''

    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']

        # return redirect(url_for('index'))
        return redirect(url_for('upload'))

    return render_template('login.html')


@app.route("/complete")
def complete():
    '''
    支出明细
    :return:
    '''

    if session.get('username') == 'changhao' and session.get('password') == 'changhao':


        db = querydb.DBAPI()

        # 支出明细页面
        data = db.queryForeEnd('zcmx')

        # 支出明细 共多少条记录
        zcmx_jl = db.queryForeEnd('zcmx_jl')

        # 分页查询
        li = []
        for i in range(1, zcmx_jl[0]+1):
            li.append(i)
        pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=50)
        print(request.path)
        print(request.args)
        index_list = li[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()

        return render_template('table_complete.html', data=data, zcmx_jl=zcmx_jl, html=html, index_list=index_list)

    return redirect(url_for('login'))


@app.route("/chartcolumnar")
def chart_columnar():
    '''
    消费支收图
    :return:
    '''

    if session.get('username') == 'changhao' and session.get('password') == 'changhao':
        return render_template('chart_columnar.html')

    return redirect(url_for('login'))


@app.route("/chartpie")
def chart_pie():
    '''
    消费分布图
    :return:
    '''

    if session.get('username') == 'changhao' and session.get('password') == 'changhao':
        return render_template('chart_pie.html')

    return redirect(url_for('login'))


@app.route("/formvalidate")
def form_validate():
    '''
    账单总结报告
    :return:
    '''

    if session.get('username') == 'changhao' and session.get('password') == 'changhao':

        content = md2html('static/js/charts/wechatBill.md')  # markdown文件的路径

        return render_template('form_validate.html', **locals())

    return redirect(url_for('login'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if session.get('username') == 'changhao' and session.get('password') == 'changhao':
        return render_template('upload_file.html')

    return redirect(url_for('login'))


@app.route('/uploadfile', methods=['POST', 'GET'])
def upload_file():

    if request.method == 'POST':

        try:

            f = request.files['file']

            # 当前文件所在路径
            basepath = os.path.dirname(__file__)

            # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            upload_path = os.path.join(basepath, 'static/uploads', secure_filename(f.filename))
            f.save(upload_path)

        except KeyError:
            # 清除&还原 Chart JS 文件, 包含markdown文档
            # 清理 wxbill.db 数据库
            # 清除 csv 账单文件
            reductionFile()

            # 错误页面
            return render_template('uploads_error.html')

        # 判断uploads目录是否存在csv账单文件
        if not len(getfile()) >= 1:

            # 清除&还原 Chart JS 文件, 包含markdown文档
            # 清理 wxbill.db 数据库
            # 清除 csv 账单文件
            reductionFile()

            # 错误页面
            # return redirect(url_for('upload'))
            return render_template('uploads_error.html')

        try:

            # 创建 sqlite 数据库
            createDB()

            # 访客记录
            set_access_count()

            # wechatBill 配置启动加载
            boot()

        except Exception:
            print('程序有异常,请联系程序开发者!!! 邮箱: wu_chang_hao@qq.com')

        return redirect(url_for('index'))

    return redirect(url_for('login'))

@app.route('/output', methods=['POST', 'GET'])
def output_file():

    '''

    微信账单 docx文件格式 导出

    :return:
    '''

    if request.method == 'GET':

        export_bill_docx()

        if os.path.isfile('static/doc/wechatBill.docx'):
            return send_from_directory('static/doc/', 'wechatBill.docx', as_attachment=True)


@app.route("/forgot")
def forgot():
    '''
    忘记密码页面
    :return: 账号 changhao  密码 changhao
    '''

    return render_template('forgot.html')


@app.route("/logout")
def logout():
    '''
    注销登录
    :return:
    '''

    session.pop('username', None)
    session.pop('password', None)

    # 清除 Chart JS 文件, 包含markdown文档
    # 清理 wxbill.db 数据库
    # 清除 csv 账单文件
    reductionFile()

    return redirect(url_for('index'))


# md转html的方法
def md2html(filename):
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
            'markdown.extensions.toc']
    mdcontent = ""
    with open(filename, 'r', encoding='utf-8') as f:
        mdcontent = f.read()
        pass
    html = markdown.markdown(mdcontent, extensions=exts)
    content = Markup(html)
    return content


# *************************************** RESTful 接口 *************************************************

@app.route('/api/index/xffl')
def get_tasks():
    '''
    消费分类API
    :return:
    '''
    # response = make_response(jsonify(response=get_articles(ARTICLES_NAME)))
    # response = make_response(jsonify({'test': '001'}))
    # response.headers['Access-Control-Allow-Origin'] = '*'
    # response.headers['Access-Control-Allow-Methods'] = 'POST'
    # response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    # resp = jsonify({'error':False})
    # # 跨域设置
    # resp.headers['Access-Control-Allow-Origin'] = '*'

    # data = {
    #     'hello': 'world',
    #     'number': 3
    # }
    # js = json.dumps(data)
    #
    # resp = make_response(js, status=200, mimetype='application/json')
    # resp.headers['Access-Control-Allow-Origin'] = '*'


    test = {
        'aa': '11',
        'bb': '22'
            }

    # return "successCallback"+"("+json.dumps(test)+")"
    return render_template('test.html', test=json.dumps(test))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8080)

