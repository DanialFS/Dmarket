import nltk
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB




# Инициализация nltk
nltk.download('punkt')
nltk.download('stopwords')


# Предварительная обработка текста
def preprocess(text):
    if not text:
        return ''
    tokens = word_tokenize(text.lower(), language='russian')
    stop_words = set(stopwords.words('russian'))
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    # Добавим условие, чтобы игнорировать короткие слова (менее 3 символов)
    tokens = [word for word in tokens if len(word) > 2]
    return ' '.join(tokens)


training_data = [
    ("привет здравствуйте здрасте здраствуйте  здравствуйте  добрый день вечер день дела",
     'Здравствуйте, приветствую вас!\n\nМожете задавать вопросы '),
    ("как сделать оформить заказ",
     ''' <h4>КАК СДЕЛАТЬ ЗАКАЗ? </h4>
    1. Выберите товары и добавьте их в корзину <br> 
    2. Перейдите в раздел «Корзина» и нажмите «Перейти к оформлению» <br>
    3. Укажите ваши данные <br>
    4. Выберите способ доставки и укажите адрес <br>
    5. Выберите способ оплаты и нажмите «Оплатить онлайн» <br>
    6. Оплатите заказ, и он поступит в обработку <br>
    Если возникли вопросы с оформлением заказа, пишите менеджерам'''),
    ("как сделать оплату оплатить",
     ''' <h4>КАК ОПЛАТИТЬ ЗАКАЗ?</h4>
    Способ оплаты выбирается при оформлений заказа
    При онлайн оплате действует скидка -5%
    Мы принимаем оплату через: <br>
        1. Бановские карты: Visa, MasterCard <br>
        2. Kaspi Qr, Halyk QR <br>
        3. Оплата наличными курьеру '''),
    ("<h4>КАК ПОДОБРАТЬ РАЗМЕР?",
     'Таблица размеров различным брендов -> '),
    ("до встречи свидания пока давай хорошего дня вечера",
     'До встречи!'),
    ("как проверить товар оригинальность",
     '<h4>ПРОВЕРКА НА ОРИГИНАЛЬНОСТЬ</h4>'
     'Наш каждый товар имеет личный QR-Code, который идентифицирует его как оригинальный <br>'
     'Вы можете открыть камеру на вашем смартфоне и проверить <br>'
     '<h4>ПРОВЕРКА НА БРАК</h4>'
     'Перед распаковкой рекомендуется фиксировать процесс на камеру, это поможет при возможном возврате товара'),
    ("как правильно чистить правильно почистить чистит чист хорошо моют помыть мыть чистить кросы кроссы кроссовки обувь уход ",
    "Уход за кроссовками зависит от их типа и того, как они используются."),
    ("условия гарантий возврат политика гарант возврат обмен вернуть можно нет или",
     "С политикой возврата/обмена вы можете ознакомиться тут ->  {% url 'pages:agreement' %}")
]



# Предварительная обработка текста для обучающих данных
X_train = [preprocess(text) for text, label in training_data]
y_train = [label for text, label in training_data]

# Преобразование текстовых данных в векторы с помощью CountVectorizer
vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(X_train)

# Обучение модели на основе мультиномиального наивного Байеса
clf = MultinomialNB()
clf.fit(X_train_counts, y_train)


# Функция для классификации запроса пользователя
# Функция для классификации запроса пользователя
# Функция для классификации запроса пользователя
# Функция для классификации запроса пользователя
def classify_question(question):
    if not question:
        return "Извините, я не могу ответить на ваш запрос. Обратитесь в службу поддержки."

    preprocessed_question = preprocess(question)

    if not preprocessed_question:
        return "Введите ваш запрос ниже или воспользуйтесь популярными вопросами."

    # Выполняем предсказание только если вопрос не пустой
    question_counts = vectorizer.transform([preprocessed_question])
    prediction = clf.predict(question_counts)

    # Если предсказанный класс не находится в обучающем наборе данных,
    # возвращаем сообщение о неизвестном запросе
    if prediction[0] not in clf.classes_:
        return "Извините, я не понимаю ваш вопрос. Пожалуйста, попробуйте сформулировать его по-другому."

    # Если предсказанный класс находится в обучающем наборе данных, возвращаем его
    return prediction[0]


# Функция для получения ответа на вопрос
def get_answer(question):
    category = classify_question(question)
    return category


@csrf_exempt
def bot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            question_text = data.get('question', '')

            # Получение ответа на вопрос
            answer_text = get_answer(question_text)

            if answer_text:
                # Возвращение ответа в формате JSON
                return JsonResponse({'response': answer_text})
            else:
                return JsonResponse(
                    {'response': "Извините, я не могу ответить на ваш запрос. Обратитесь в службу поддержки."})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    elif request.method == 'GET':
        # Если метод GET, отображаем страницу index.html
        return render(request, 'support/support.html')
    else:
        # Возвращаем ошибку для других методов запроса
        return JsonResponse({'error': 'Only POST and GET requests are allowed'})
