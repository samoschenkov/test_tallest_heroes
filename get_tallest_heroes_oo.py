import requests


class Hero:
    def __init__(self, hero_info):
        self.info = hero_info
        self.has_job = self.check_occupation()
        self.height_num = self.get_height_num()

    def check_occupation(self):
        return self.info['work']['occupation'] != '-'

    def get_height_num(self):
        height = self.info['appearance']['height'][1]
        return int(''.join(filter(lambda x: x.isdigit(), height)))


class HeroManager:
    def __init__(self, id_start, id_end, token):
        self.id_start = id_start
        self.id_end = id_end
        self.token = token
        self.heroes = []

    def fetch_heroes(self):
        for i in range(self.id_start, self.id_end):
            url = f"https://superheroapi.com/api/{self.token}/{i}"
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception("Ошибка!")
            hero_info = response.json()
            print(hero_info)
            self.heroes.append(Hero(hero_info))

    def get_tallest_heroes(self, gender, has_job):
        filtered_heroes = [
            hero for hero in self.heroes
            if hero.info['appearance']['gender'] == gender and hero.has_job == has_job
        ]

        if not filtered_heroes:
            return None

        tallest_hero = max(filtered_heroes, key=lambda hero: hero.height_num)
        print(tallest_hero)
        return self.check_others(filtered_heroes, tallest_hero)

    def check_others(self, filtered_heroes, tallest_hero):
        height = tallest_hero.height_num
        final_list = [hero for hero in filtered_heroes if hero.height_num == height]
        num = len(final_list)
        notification_str = f'Количество героев с самым высоким ростом: {num}'
        print(notification_str)
        return final_list


def main():
    id_start = 1
    id_end = 10
    token = '' #введите свой токен
    gender = 'Male'
    has_job = True

    manager = HeroManager(id_start, id_end, token)
    manager.fetch_heroes()
    tallest_heroes = manager.get_tallest_heroes(gender, has_job)

    if tallest_heroes:
        for hero in tallest_heroes:
            print('\n')
            print(hero.info)

if __name__ == "__main__":
    main()
