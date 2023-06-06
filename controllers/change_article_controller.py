import json
from py_ui.change_article import Ui_ChangeArticle
from PyQt5 import QtWidgets


class ChangeArticle(QtWidgets.QMainWindow, Ui_ChangeArticle):
    def __init__(self, net, exist_articles, status, window, articles):
        try:
            super().__init__()
            self.setupUi(self)
            self.network = net
            self.exist_articles = exist_articles
            self.window = window
            self.status = status
            self.submit.clicked.connect(self.submit_pressed)
            if status == 1:
                self.fine.hide()
                self.fine_lbl.hide()
                self.loose.hide()
                self.loose_lbl.hide()
                self.submit.setText('Удалить')
            self.articles = articles
            self.articles_for_cb = {}
            self.final_articles = {}
            self.result = {}
            self.parse_articles()
            self.article.addItem('-')
            print(self.final_articles)
            for (key, value) in self.final_articles.items():
                self.article.addItem(key)
            self.article.currentIndexChanged.connect(self.article_selected)
        except Exception as e:
            print(e)

    def article_selected(self):

        if self.article.currentText() != '-':
            try:
                temp = self.final_articles[self.article.currentText()]
                self.output.setText(temp['Описание'])
                self.fine_lbl.setText('Штраф ' + str(temp['Размер штрафа']) + ' ' + 'рублей')
                self.loose_lbl.setText('Лишение прав ' + str(temp['Лишение прав']) + ' ' + 'месяцев')
            except Exception as e:
                print(e)

    def submit_pressed(self):
        all_fines = ''
        print('Boy')
        if self.article.currentText() != '-':
            print('Next door')
            if self.status == 0:

                if self.fine.text() is not None or self.loose.text() is not None:
                    if self.fine.text() is None:
                        self.fine.setText('0')
                    if self.loose.text() is None:
                        self.loose.setText('0')
                    self.result[self.article.currentText()] = {'Штраф': self.fine.text(),
                                                               'Лишение прав': self.loose.text(),
                                                               'Description':
                                                                   self.final_articles[self.article.currentText()][
                                                                       'Описание']}

                if len(self.exist_articles) == 0:
                    self.exist_articles = self.result
                else:
                    for (key, value) in self.result.items():
                        self.exist_articles[key] = value

                for (key, value) in self.exist_articles.items():
                    fine_to_string = key + ' '
                    value = str(value).replace('\'', '\"')
                    value = json.loads(value)
                    for (jk, jv) in value.items():
                        print(jk)
                        print(jv)
                        if jk == 'Штраф':
                            fine_to_string = fine_to_string + jk + ': ' + jv + ' ' + 'рублей  '
                        if jk == 'Лишение прав':
                            if jv == '':
                                jv = '0'
                            fine_to_string = fine_to_string + jk + ': ' + jv + ' ' + 'месяцев'

                    all_fines = all_fines + fine_to_string + '\n'
                self.window.textEdit.setText(all_fines)
            elif self.status == 1:
                try:
                    del self.exist_articles[self.article.currentText()]
                    self.window.added_articles = self.exist_articles
                    for (key, value) in self.exist_articles.items():
                        fine_to_string = key + ' '
                        value = str(value).replace('\'', '\"')
                        value = json.loads(value)
                        for (jk, jv) in value.items():
                            if jk == 'Штраф':
                                fine_to_string = fine_to_string + jv + ' ' + 'рублей'
                            if jk == 'Лишение прав':
                                fine_to_string = fine_to_string + jv + ' ' + 'месяцев'
                        all_fines = all_fines + fine_to_string + '\n'
                    self.window.textEdit.setText(all_fines)
                except Exception as e:
                    print(e)
        self.window.added_articles = self.exist_articles
        print(self.exist_articles)
        self.close()

    def parse_articles(self):
        for i in self.articles:
            self.articles_for_cb = {}
            json_temp = str(i).replace('None', '\'Нет\'')
            json_temp = json_temp.replace('\"', '\\"')
            json_temp = json.loads(json_temp.replace('\'', '\"'))
            for (jk, jv) in json_temp.items():
                if jk == 'article_id':
                    jk = 'Статья'
                    jv = article_type_parser(jv)
                    self.articles_for_cb[f'{jk}'] = jv
                if jk == 'description':
                    jk = 'Описание'
                    self.articles_for_cb[f'{jk}'] = jv
                if jk == 'price':
                    jk = 'Размер штрафа'
                    if 'Нет' not in jv:
                        json_price = str(jv).replace('\'', '\"')
                        json_price = json.loads(json_price)
                        jv = json_price['start'] + '-' + json_price['end']
                    self.articles_for_cb[f'{jk}'] = jv
                if jk == 'deprivation_months':
                    jk = 'Лишение прав'
                    if 'Нет' not in jv:
                        json_month = str(jv).replace('\'', '\"')
                        json_month = json.loads(json_month)
                        jv = json_month['start'] + '-' + json_month['end']
                    self.articles_for_cb[f'{jk}'] = jv
            self.final_articles[self.articles_for_cb['Статья']] = self.articles_for_cb


def article_type_parser(article):
    temp = article[1:-1]
    temp = temp.split(',')
    state = 'ст. '
    point = ' п. '
    if temp[0] != '0':
        state = state + temp[0]
    if temp[1] != '0':
        if len(state) > 4:
            state = state + '.'
        state = state + temp[1]
    if temp[2] != '0':
        if len(state) > 4:
            state = state + '.'
        state = state + temp[2]
    if temp[3] != '0':
        point = point + temp[3]
    if temp[4] != '0':
        if len(point) > 3:
            point = point + '.'
        point = point + temp[4]
    return state + ' ' + point
