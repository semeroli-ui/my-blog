from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

# 数据库文件路径
DATABASE = 'blog.db'

# 初始化数据库函数
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # 创建文章表
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 如果表是空的，插入一些示例文章
    c.execute("SELECT COUNT(*) FROM posts")
    if c.fetchone()[0] == 0:
        sample_posts = [
            ("我的第一篇博客", "这是我的第一篇博客文章，用来测试Flask模板渲染功能。"),
            ("Python学习心得", "学习Python的过程中，我觉得Flask是一个非常轻量好用的Web框架。"),
            ("Web开发入门", "从HTML、CSS到Flask，Web开发的世界真的很广阔！")
        ]
        c.executemany("INSERT INTO posts (title, content) VALUES (?, ?)", sample_posts)
    
    conn.commit()
    conn.close()

# 初始化数据库
init_db()

# 首页路由
# 科技感落地页路由
@app.route('/splash')
def splash_page():
    return render_template('splash.html')

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # 使返回结果为字典形式
    c = conn.cursor()
    
    # 获取所有文章，按发布时间倒序排列
    c.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = c.fetchall()
    
    conn.close()
    
    return render_template('index.html', 
                         posts=posts,
                         current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# 文章详情页路由
@app.route('/post/<int:post_id>')
def show_post(post_id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = c.fetchone()
    
    conn.close()
    
    if post:
        return render_template('post.html', post=post)
    else:
        return "文章不存在", 404

# 写文章页面路由
@app.route('/write', methods=['GET', 'POST'])
def write_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('write.html')

# 关于页面路由
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)