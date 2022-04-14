# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH
import requests as rq
# Пакет для удобной работы с данными в формате json
import json

 
class Parser:
    def __init__(self, vacansy_name) -> None:
        self.vacansy_name = vacansy_name
    def __getPage(self, page = 0, vacansy_name = None, vacansy_description=None):
        """
        Создаем метод для получения страницы со списком вакансий.
        Аргументы:
            page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
        """
        
        # Справочник для параметров GET-запроса
        params = {
            'text': f'DESCRIPTION:{vacansy_name}', # Текст фильтра. В имени должно быть слово "Аналитик"
            #'text': f'DESCRIPTION:{vacansy_description}',
            'area': 1, # Поиск ощуществляется по вакансиям города Москва
            'page': page, # Индекс страницы поиска на HH
            'per_page': 100 # Кол-во вакансий на 1 странице
        }
        
        
        req = rq.get('https://api.hh.ru/vacancies', params) # Посылаем запрос к API
        data = req.content.decode() # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        return data
    
    def info_to_vac_list(self):
        # Считываем первые 2000 вакансий
        for page in range(0, 1): 
            # Преобразуем текст ответа запроса в справочник Python
            jsObj = [json.loads(self.__getPage(page, self.vacansy_name))]
            list_vac = []
            for vac in jsObj[0]['items']:
                vac_data = {}
                #print(jsObj[0]['items'][0]['salary']['from'])
                vac_data['name'] = vac['name']
                try:
                    vac_data['salary'] = vac['salary']['from']
                except TypeError as te:
                    vac_data['salary'] = "Не указано"
                vac_data['url'] = vac['alternate_url']
                vac_data['comp_name'] = vac['employer']['name']
                # vac_data['phone'] = vac
                list_vac.append(vac_data)
        return list_vac


