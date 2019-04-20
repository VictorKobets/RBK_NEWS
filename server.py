from flask import Flask, render_template, url_for, redirect, Response, send_from_directory
from scrapper import Scrapy
import requests
import datetime


app = Flask(__name__)
data = Scrapy()


@app.route('/')
def window():
    '''View the main window.
    '''
    return render_template('window.html')


@app.route('/news', methods=['POST'])
def news():
    '''View windows with news.
    '''
    data.get_content(_type='news')
    return render_template('news.html', data=data.current_content)


@app.route('/articles', methods=['POST'])
def articles():
    '''View windows with articles.
    '''
    data.get_content(_type='articles')
    return render_template('articles.html', data=data.current_content)


@app.route('/ret', methods=['POST'])
def ret():
    data.current_content = None
    return redirect(url_for('window'))


@app.route('/donwload_news', methods=['POST'])
def donwload_news():
    return Response(
        data.save_to_file(save_type='news'),
        mimetype="txt",
        headers={
            "Content-disposition":
            f"attachment; filename=RBK_news{datetime.datetime.now()}.txt"
            }
        )


@app.route('/donwload_articles', methods=['POST'])
def donwload_articles():
    return Response(
        data.save_to_file(save_type='articles'),
        mimetype="txt",
        headers={
            "Content-disposition":
            f"attachment; filename=RBK_articles{datetime.datetime.now()}.txt"
        }
    )


if __name__ == "__main__":
    app.run()
