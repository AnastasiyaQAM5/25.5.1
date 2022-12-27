import time
from typing import Dict, Any

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class Animal:
    def __init__(self, name, age, specie):
        self.name = name
        self.age = age
        self.specie = specie


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('E:\Drivers\chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.implicitly_wait(10)
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    pytest.driver.get('http://petfriends.skillfactory.ru/my_pets')

    # находим всех животных
    time.sleep(3)

    pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr')

    tmp_locator = 'Питомцев: ' + str(len(pets))
    print('|' + tmp_locator + '|')

    # задаем путь к числу питомцев, указанному слева
    statistic = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(':')[1]

    # проверяем что количество строк с питомцами соответствует их числу слева
    assert len(pets) != statistic

    # определяем половину питомцев
    half_pets = int(statistic) / 2
    print(round(half_pets))

    images = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > th > img')

    # проверяем, что аттрибут src в фото заполнен
    for i in range(len(images) - 1):
        assert images[i].get_attribute('scr') != ''

    # проверяем, что хотя бы половина питомцев имеет фото
    assert len(images) >= round(half_pets)

    names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    species = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')

    list_of_animals = []

    iterator = 0
    while iterator < int(statistic):
        animal = Animal(names[iterator].text, ages[iterator].text, species[iterator].text)
        list_of_animals.append(animal)
        print(animal.name + '|' + animal.specie + '|' + animal.age)
        iterator += 1

    # проверяем, что у всех питомцев есть имена, породы, возраст
    for animal in list_of_animals:
        assert animal.name != ''
        assert animal.specie != ''
        assert animal.age != ''

    # проверяем, что у всех питомцев разные имена
    i = 0
    while i < len(list_of_animals):
        j = i+1
        temp_pet = list_of_animals[i]
        while j < len(list_of_animals):
            #assert temp_pet.name != list_of_animals[j].name
            j+=1
        i+=1

    # проверяем, что в списке нет повторяющихся питомцев
    i = 0
    while i < len(list_of_animals):
        j = i + 1
        temp_pet = list_of_animals[i]
        while j < len(list_of_animals):
            assert not(temp_pet.name == list_of_animals[j].name and temp_pet.specie == list_of_animals[j].specie and temp_pet.age == list_of_animals[j].age)
            j += 1
        i += 1




