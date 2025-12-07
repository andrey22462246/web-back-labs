from flask import Blueprint, render_template, request, redirect, session, abort, jsonify

lab7 = Blueprint('lab7',__name__)

films = [
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Два заключённых, банкир Энди Дюфрейн и вор Эллис Бойд «Рэд» Реддинг, становятся друзьями в тюрьме Шоушенк, находя утешение и искупление через простые человеческие добродетели.",
    },
    {
        "title": "The Godfather",
        "title_ru": "Крёстный отец",
        "year": 1972,
        "description": "Стареющий глава преступного клана Корлеоне передаёт контроль над своей империей своему неохотному сыну Майклу, втягивая его в мир мафии, насилия и власти.",
    },
    {
        "title": "The Dark Knight",
        "title_ru": "Тёмный рыцарь",
        "year": 2008,
        "description": "Когда угроза по имени Джокер сеет хаос в Готэме, Бэтмен сталкивается с одним из самых серьёзных испытаний — как физических, так и моральных — в своей борьбе с несправедливостью.",
    },
    {
        "title": "Pulp Fiction",
        "title_ru": "Криминальное чтиво",
        "year": 1994,
        "description": "Жизни двух наёмных убийц, боксёра, гангстера и его жены переплетаются в четырёх историях о насилии, случайностях и искуплении.",
    },
    {
        "title": "Inception",
        "title_ru": "Начало",
        "year": 2010,
        "description": "Вор, специализирующийся на краже секретов из подсознания с помощью технологии доступа к снам, получает задание внедрить идею в разум наследника крупной корпорации.",
    },
]

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if (id >= 0 and id < len(films)):
        return films[id]
    else:   
        abort(404)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if not (0 <= id < len(films)):
        return abort(404)

    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if 0 <= id < len(films):
        film = request.get_json()
        if film['description'] == '':
            return {'description': 'Заполните описание'}, 400
        films[id] = film
        return films[id]
    else:
        return abort(404)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    if film['description'] == '':
            return {'description': 'Заполните описание'}, 400
    films.append(film)  
    return jsonify({"id": len(films) - 1}), 201
