import requests
from bs4 import BeautifulSoup 


class News:
    def __init__(self, title, link, date, body=None):
        '''Structure describing the collected news.
        '''
        self.title = title
        self.link = link
        self.date = date
        self.body = body


class Scrapy:
    def __init__(self):
        '''Class collecting data from the RBK website.
        '''
        self.current_content = None

    def get_content(self, _type):
        '''The method collects 15 main news from the RBK website
        and returns them in the form of a list of News type objects.
        '''
        request = requests.get('http://www.rbc.ru/')
        soup = BeautifulSoup(request.text, 'lxml')
        self.current_content = list()
        # Main news  
        content = soup.find('div', 'main__big')
        data = News( 
                content.a.span.span.span.text,
                content.a['href'],
                content['data-modif-date'],
            )
        if _type == 'articles':
            data.body = self.get_body(data.link)
        self.current_content.append(data)
        # Minor news  
        for content in soup.find_all('div', 'main__feed'):
            data = News(
                    content.a.span.span.text,
                    content.a['href'],
                    content['data-modif-date']
                )
            if _type == 'articles':
                data.body = self.get_body(data.link)
            self.current_content.append(data)

    @staticmethod
    def get_body(link):
        '''Internal method collecting the body of articles.
        Get the item News returns a text string.
        '''
        result_string = ''
        request = requests.get(link)
        soup = BeautifulSoup(request.text, 'lxml')
        content = soup.find('div', 'article__text')
        for current_string in content.find_all('p'):
            result_string += current_string.text
        return result_string

    def save_to_file(self, save_type):
        '''Prepares the collected data to write to the file.
        '''
        if self.current_content is None:
            self.get_content(_type=save_type)
        send_string = ''
        for content in self.current_content:
            if save_type == 'articles':
                send_string += f'"{content.title}"' + '\n'
                send_string += content.body + '\n'
            else:
                send_string += content.title + '\n'
            send_string += content.link + '\n'
            send_string += content.date + '\n\n'
        return send_string
