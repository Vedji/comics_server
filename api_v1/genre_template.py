class Genre:
    genres = [
        "Романтика", "Драма", "Комедия", "Фэнтези", "Приключения", "Повседневность", "Киберпанк", "Психологическое",
        "Космос", "Магия", "Фантастика", "Пост-апокалипсис", "Боевик", "Трагедия", "Сверхъестественное", "Детектив"
    ]

    @staticmethod
    def get_genre_by_list(_genres: list[str]) -> str:
        line = "0" * len(Genre.genres)
        for i in _genres:
            if i.lower() in map(lambda x: x.lower(), _genres):
                index = Genre.genres.index(i.capitalize())
                line = line[: index] + "1" + line[index+1:]
        return line

    @staticmethod
    def get_manga_genre(line: str):
        if len(line) != len(Genre.genres):
            return ["Error"]
        return list(filter(
            lambda x: x is not None, [Genre.genres[i] if line[i] == "1" else None for i in range(len(line))]))

    @staticmethod
    def get_work_dict_genre():
        res = {}
        for i in range(len(Genre.genres)):
            res[i] = Genre.genres[i]
        return res

    @staticmethod
    def get_null_genre():
        return '_' * len(Genre.genres)

    @staticmethod
    def check_temp(temp: str):
        return temp.count("_") + temp.count("1") == len(Genre.genres)

    @staticmethod
    def is_english_alphabet(input_string):
        abc = "qwertyuiopasdfghjklzxcvbnm"
        for char in input_string:
            if not char.isalpha() and char != '_' and char.lower() not in abc:
                return False
        return True


if __name__ == "__main__":
    print(Genre.get_genre_by_list([
        "Трагедия"
    ]))
