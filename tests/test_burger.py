import pytest

from praktikum.bun import Bun
from praktikum.burger import Burger
from praktikum.ingredient import Ingredient

from tests.helper import Mocks

from data import TestData

class TestBurger:

    #Проверка дефолтного значения атрибута булочка
    def test_default_bun_is_none (self, burger):
        assert burger.bun == None


    #Проверка дефолтного значения атрибута ингредиенты
    def test_default_list_of_ingredients_is_empty (self, burger):
        assert burger.ingredients == []


    #Проверка выбора булочки
    def test_set_buns_success (self, burger):
        mock_bun = Mocks.mock_bun(TestData.TEST_DATA_BUN)
        burger.set_buns(mock_bun)

        assert burger.bun == mock_bun


    #Проверка добавления одного ингредиента
    def test_add_ingredient_success(self, burger):
        mock_sauce = Mocks.mock_ingredient(TestData.TEST_DATA_SAUCE)
        burger.add_ingredient(mock_sauce)

        assert burger.ingredients[0] == mock_sauce
        assert len(burger.ingredients) == 1


    #Проверка добавления нескольких (двух) ингредиентов
    @pytest.mark.parametrize('ingredients', [
        [TestData.TEST_DATA_SAUCE, TestData.TEST_DATA_SAUCE],     # два одинаковых ингредиента (два соуса)
        [TestData.TEST_DATA_SAUCE, TestData.TEST_DATA_FILLING],     # два разных ингредиента
    ])
    def test_add_ingredients_success(self, burger, ingredients):
        first_ingredient = Mocks.mock_ingredient(ingredients[0])
        second_ingredient = Mocks.mock_ingredient(ingredients[1])
        burger.add_ingredient(first_ingredient)
        burger.add_ingredient(second_ingredient)

        assert burger.ingredients[0] == first_ingredient
        assert burger.ingredients[1] == second_ingredient
        assert len(burger.ingredients) == 2


    #Проверка удаления ингредиента (после удаления в бургере останутся ингредиенты)
    def test_remove_one_ingredient_success(self, burger):
        mock_sauce = Mocks.mock_ingredient(TestData.TEST_DATA_SAUCE)
        mock_filling = Mocks.mock_ingredient(TestData.TEST_DATA_FILLING)
        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)
        burger.remove_ingredient(0)

        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_filling


    #Проверка удаления всех ингредиентов (после удаления в бургере не остается ни одного ингредиента)
    def test_remove_all_ingredients_success(self, burger):
        mock_sauce = Mocks.mock_ingredient(TestData.TEST_DATA_SAUCE)
        burger.add_ingredient(mock_sauce)
        burger.remove_ingredient(0)

        assert len(burger.ingredients) == 0


    #Проверка невозможности удаления ингредиента с несуществующим индексом
    def test_remove_wrong_index_ingredients_failed(self, burger):
        mock_sauce = Mocks.mock_ingredient(TestData.TEST_DATA_SAUCE)
        burger.add_ingredient(mock_sauce)
        with pytest.raises(IndexError):
            burger.remove_ingredient(3)


    #Проверка перемещения ингредиентов
    def test_move_ingredient_success(self, burger):
        mock_sauce = Mocks.mock_ingredient(TestData.TEST_DATA_SAUCE)
        mock_filling = Mocks.mock_ingredient(TestData.TEST_DATA_FILLING)
        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)
        burger.move_ingredient(0, 1)

        assert burger.ingredients[0] == mock_filling
        assert burger.ingredients[1] == mock_sauce


    #Проверка невозможности перемещения ингредиента с несуществующим индексом
    def test_move_wrong_index_ingredients_failed(self, burger):
        mock_sauce = Mocks.mock_ingredient(TestData.TEST_DATA_SAUCE)
        burger.add_ingredient(mock_sauce)
        with pytest.raises(IndexError):
            burger.move_ingredient(1, 0)


    #Проверка получения стоимости бургера с разными наборами ингредиентов
    @pytest.mark.parametrize('ingredients', [
        [],     # булочки без ингредиентов
        [TestData.TEST_DATA_SAUCE],     # булочки с соусом
        [TestData.TEST_DATA_FILLING],     # булочки с начинкой
        [TestData.TEST_DATA_SAUCE, TestData.TEST_DATA_SAUCE],     # булочки с одним и тем же ингредиентом (соусом) дважды
        [TestData.TEST_DATA_SAUCE, TestData.TEST_DATA_FILLING],     # булочки с соусом и начинкой
    ])
    def test_get_price_success(self, burger, ingredients):
        mock_bun = Mocks.mock_bun(TestData.TEST_DATA_BUN)
        burger.set_buns(mock_bun)
        expected_price = mock_bun.get_price()*2
        for index in ingredients:
            ingredient = Mocks.mock_ingredient(index)
            burger.add_ingredient(ingredient)
            expected_price += index['price']

        assert burger.get_price() == expected_price


    #Проверка невозможности получения стоимости бургера без булочек
    def test_get_price_without_buns_failed(self, burger):
        mock_sauce = Mocks.mock_ingredient(TestData.TEST_DATA_SAUCE)
        burger.add_ingredient(mock_sauce)
        with pytest.raises(AttributeError):
            burger.get_price()


    #Проверка получения чека с разными наборами ингредиентов
    @pytest.mark.parametrize('ingredients', [
        [],     # булочки без ингредиентов
        [TestData.TEST_DATA_SAUCE],     # булочки с соусом
        [TestData.TEST_DATA_FILLING],     # булочки с начинкой
        [TestData.TEST_DATA_SAUCE, TestData.TEST_DATA_SAUCE],     # булочки с одним и тем же ингредиентом (соусом) дважды
        [TestData.TEST_DATA_SAUCE, TestData.TEST_DATA_FILLING],     # булочки с соусом и начинкой
    ])
    def test_get_receipt_success(self, burger, ingredients):
        mock_bun = Mocks.mock_bun(TestData.TEST_DATA_BUN)
        burger.set_buns(mock_bun)
        expected_receipt = f'(==== {mock_bun.get_name()} ====)\n'
        expected_price = mock_bun.get_price()*2
        for index in ingredients:
            ingredient = Mocks.mock_ingredient(index)
            burger.add_ingredient(ingredient)
            expected_receipt += f'= {str(index['type']).lower()} {index['name']} =\n'
            expected_price += index['price']

        expected_receipt += f'(==== {mock_bun.get_name()} ====)\n\n'
        expected_receipt += f'Price: {expected_price}'

        assert burger.get_receipt() == expected_receipt


    #Проверка невозможности получения чека без булочек
    def test_get_receipt_without_buns_failed(self, burger):
        mock_sauce = Mocks.mock_ingredient(TestData.TEST_DATA_SAUCE)
        burger.add_ingredient(mock_sauce)
        with pytest.raises(AttributeError):
            burger.get_receipt()
