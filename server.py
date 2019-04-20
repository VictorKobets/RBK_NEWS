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
    data.current_content = None
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
    date = str(datetime.datetime.now())
    date = date.replace(" ", "_")
    return Response(
        data.save_to_file(save_type='news'),
        mimetype="text/plain",
        headers={
            "Content-disposition":
            f"attachment; filename=RBK_news_{date}.txt"
            }
        )


@app.route('/donwload_articles', methods=['POST'])
def donwload_articles():
    date = str(datetime.datetime.now())
    date = date.replace(" ", "_")
    return Response(
        data.save_to_file(save_type='articles'),
        mimetype="text/plain",
        headers={
            "Content-disposition":
            f"attachment; filename=RBK_articles_{date}.txt"
        }
    )


if __name__ == "__main__":
    app.run()
