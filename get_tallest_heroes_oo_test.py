import pytest
from unittest.mock import patch, MagicMock
from get_tallest_heroes_oo import Hero, HeroManager

class TestHero:
    @pytest.fixture
    def mock_hero_data(self):
        return {
            'name': 'Superman',
            'work': {'occupation': 'Reporter'},
            'appearance': {
                'height': ['6\'3"', '190 cm'],
                'gender': 'Male'
            }
        }

    def test_hero_initialization(self, mock_hero_data):
        hero = Hero(mock_hero_data)
        assert hero.info == mock_hero_data
        assert hero.has_job == True
        assert hero.height_num == 190

    def test_hero_no_job(self, mock_hero_data):
        mock_hero_data['work']['occupation'] = '-'
        hero = Hero(mock_hero_data)
        assert hero.has_job is False

    def test_hero_height_extraction(self, mock_hero_data):
        hero = Hero(mock_hero_data)
        assert hero.height_num == 190


class TestHeroManager:
    @pytest.fixture
    def mock_hero_data(TestHero):
        return {
            'name': 'Superman',
            'work': {'occupation': 'Reporter'},
            'appearance': {
                'height': ['6\'3"', '190 cm'],
                'gender': 'Male'
            }
        }

    @patch('requests.get')
    def test_fetch_heroes(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'Batman',
            'work': {'occupation': 'Vigilante'},
            'appearance': {
                'height': ['6\'2"', '188 cm'],
                'gender': 'Male'
            }
        }
        mock_get.return_value = mock_response

        manager = HeroManager(1, 2, 'dummy_token')
        manager.fetch_heroes()

        assert len(manager.heroes) == 1
        assert manager.heroes[0].info['name'] == 'Batman'

    @patch('requests.get')
    def test_fetch_heroes_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        manager = HeroManager(1, 2, 'dummy_token')

        with pytest.raises(Exception, match="Ошибка!"):
            manager.fetch_heroes()

    def test_get_tallest_heroes(self, mock_hero_data):
        manager = HeroManager(1, 10, 'dummy_token')
        manager.heroes.append(Hero(mock_hero_data))
        
        tallest_heroes = manager.get_tallest_heroes('Male', True)
        
        assert len(tallest_heroes) == 1
        assert tallest_heroes[0].info['name'] == 'Superman'
        assert tallest_heroes[0].info['appearance']['height'][1] == '190 cm'

    def test_get_tallest_heroes_multiple_tallest(self, mock_hero_data):
        manager = HeroManager(1, 10, 'dummy_token')
        manager.heroes.append(Hero(mock_hero_data))
        
        mock_hero_data['name'] = 'Batman'
        mock_hero_data['appearance']['height'][1] = '190 cm'
        manager.heroes.append(Hero(mock_hero_data))

        tallest_heroes = manager.get_tallest_heroes('Male', True)
        
        assert len(tallest_heroes) == 2

    def test_get_tallest_heroes_no_results(self):
        manager = HeroManager(1, 10, 'dummy_token')
        tallest_heroes = manager.get_tallest_heroes('Female', True)

        assert tallest_heroes is None


if __name__ == "__main__":
    pytest.main()
