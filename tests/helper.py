from unittest.mock import Mock

class Mocks:

    def mock_bun(bun_data):
        mock_bun = Mock()
        mock_bun.get_name.return_value = bun_data['name']
        mock_bun.get_price.return_value = bun_data['price']
        return mock_bun


    def mock_ingredient(ingredient_data):
        mock_ingredient = Mock()
        mock_ingredient.get_type.return_value = ingredient_data['type']
        mock_ingredient.get_name.return_value = ingredient_data['name']
        mock_ingredient.get_price.return_value = ingredient_data['price']
        return mock_ingredient
