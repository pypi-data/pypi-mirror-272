import wikipedia
import pyttsx3


class WikiReader:
    """
    Класс для чтения статей из Википедии.

    :param language: Язык статьи (ru или en).
    :param query: Запрос для поиска статьи.
    """

    def __init__(self):
        """
        Инициализация объекта WikiReader.

        :param language: Язык статьи (ru или en).
        :param query: Запрос для поиска статьи.
        """
        self.messages = {
            'ru': {
                'choose_language': 'Выберите язык для поиска и прочтения статьи (ru/en): ',
                'invalid_language': 'Пожалуйста, выберите корректный язык (ru/en).',
                'enter_query': 'Что вы хотите узнать?\n',
                'no_results': 'Ничего не найдено. Пожалуйста, попробуйте другой запрос.',
                'input_article_number': '\nВведите номер статьи для прочтения (или 0 для выхода): ',
                'invalid_article_number': 'Пожалуйста, введите корректный номер статьи.',
                'read_text': 'Хотите чтобы я вам прочитал текст?\n(yes/no) ',
                'http_error': 'Ошибка: превышено время ожидания запроса к Википедии.'
            },
            'en': {
                'choose_language': 'Choose language for searching and reading articles (ru/en): ',
                'invalid_language': 'Please choose a valid language (ru/en).',
                'enter_query': 'What do you want to know?\n',
                'no_results': 'Nothing found. Please try another query.',
                'input_article_number': '\nEnter the article number to read (or 0 to exit): ',
                'invalid_article_number': 'Please enter a valid article number.',
                'read_text': 'Do you want me to read the text?\n(yes/no) ',
                'http_error': 'Error: Wikipedia request timeout.'
            }
        }

        self.language = input(self.messages['en']['choose_language']).lower()
        while self.language not in ('ru', 'en'):
            print(self.messages['en']['invalid_language'])
            self.language = input(self.messages['en']['choose_language']).lower()

        self.query = input(self.messages[self.language]['enter_query'])
        try:
            wikipedia.set_lang(self.language)
            search_results = wikipedia.search(self.query)
            if not search_results:
                print(self.messages[self.language]['no_results'])
                return
            article_idx = self.select_article(search_results, self.language)
            if article_idx is None:
                return
            print("\n")
            if input(self.messages[self.language]['read_text']).lower() == 'yes':
                say = pyttsx3.init()
                say.say(self.get_article_summary(search_results[article_idx], self.language))
                print("\n")
                print(self.get_article_summary(search_results[article_idx], self.language))
                say.runAndWait()
            else:
                print(self.get_article_summary(search_results[article_idx], self.language))
        except wikipedia.exceptions.HTTPTimeoutError:
            print(self.messages[self.language]['http_error'])

    def wrap_text(self, text, line_length=150):
        """
        Обертывает текст для вывода с заданной длиной строки.

        :param text: Текст для обертывания.
        :param line_length: Максимальная длина строки.
        :return: Обернутый текст.
        """
        wrapped_text = ""
        words = text.split()
        line = ""
        for word in words:
            if len(line) + len(word) <= line_length:
                line += word + " "
            else:
                wrapped_text += line.strip() + '\n'
                line = word + " "
        wrapped_text += line.strip()
        return wrapped_text

    def get_article_summary(self, query, language):
        """
        Получает краткое описание статьи из Википедии.

        :param query: Запрос для поиска статьи.
        :return: Краткое описание статьи.
        """
        wikipedia.set_lang(language)
        try:
            summary = wikipedia.summary(query)
            return self.wrap_text(summary)
        except wikipedia.exceptions.DisambiguationError:
            return "Неоднозначный запрос. Пожалуйста, уточните ваш запрос."
        except wikipedia.exceptions.PageError:
            return "Страница не найдена. Пожалуйста, попробуйте другой запрос."

    def select_article(self, search_results, language):
        """
        Позволяет пользователю выбрать статью из списка результатов.

        :param search_results: Список результатов поиска.
        :return: Индекс выбранной статьи.
        """
        for idx, result in enumerate(search_results, start=1):
            print(f"{idx}. {result}")
        while True:
            try:
                choice = int(input(self.messages[language]['input_article_number']))
                if choice == 0:
                    return None
                elif choice < 1 or choice > len(search_results):
                    print(self.messages[language]['invalid_article_number'])
                else:
                    return choice - 1
            except ValueError:
                print("Please enter the number.")


WikiReader()
