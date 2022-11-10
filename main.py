from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import os
from PIL import Image
from PIL import ImageChops
import shutil
import html
import sys

def check_we(we: WebElement):
    """
    Проверка WebElement на файл стилей headers.css
    :return: True, если we не является блоком подключающим headers.css
    """
    return (we.get_attribute("rel") == "stylesheet") & (not ("headers.cc" in we.get_attribute("href")))


def compare_images(path_one: str, path_two: str):
    """
    Сравнение двух изображений
    :return: True, если индентичны; False, если изображения отличаются
    """
    image_one = Image.open(path_one).convert("RGB")
    image_two = Image.open(path_two).convert("RGB")
    diff = ImageChops.difference(image_one, image_two)

    return not(diff.getbbox())


def main():
    """
    Точка входа
    """
    driver = webdriver.Firefox()
    if len(sys.argv) != 2:
        print("Передайте страницу первым аргуметом")
        return
    driver.get(sys.argv[1])

    shutil.rmtree("./images")
    os.mkdir("./images")
    os.mkdir("./images/without-styles")

    # --- Configs
    # Список стилей, которые необходимо протестировать, функция check_we фильтрует итоговый список
    stylesheets_to_test = [i for i in driver.find_elements(by="tag name", value="link") if check_we(i)]
    # Элементы которые необходиимо протестировать
    elements_to_test = driver.find_elements(by="tag name", value="h2")
    # Тестируемое свойство
    property_to_test = "color"
    # ---

    stylesheet_colors = {}
    stylesheet_id_to_path = {}

    # Выключаем все тестируемые стили
    for stylesheet in stylesheets_to_test:
        driver.execute_script("arguments[0].disabled = true", stylesheet)

    # Делаем скриншоты и запоминаем оригинальные цвета заголовков
    colors = {}
    for element in elements_to_test:
        element.screenshot(f"./images/without-styles/{element.id}.png")
        colors[element.id] = element.value_of_css_property(property_to_test)
    stylesheet_colors["original"] = colors

    # Включаем по одному, делаем скриншоты, запоминаем цвета в мапу
    for stylesheet in stylesheets_to_test:
        driver.execute_script("arguments[0].disabled = false", stylesheet)
        colors = {}
        os.mkdir(f"./images/{stylesheet.id}")
        for element in elements_to_test:
            element.screenshot(f"./images/{stylesheet.id}/{element.id}.png")
            colors[element.id] = element.value_of_css_property(property_to_test)
        stylesheet_colors[stylesheet.id] = colors
        stylesheet_id_to_path[stylesheet.id] = stylesheet.get_attribute("href")
        driver.execute_script("arguments[0].disabled = true", stylesheet)
    driver.quit()
    # Сравниваем
    positive_stylesheets = []
    negative_stylesheets = []
    message = ""
    for stylesheet_name in stylesheet_colors:
        if stylesheet_name == 'original':
            continue
        positive = False
        message += f'<div id="{stylesheet_name}" class="entry tabcontent">'
        message += f"<h1>Файл стилей: {stylesheet_id_to_path[stylesheet_name]}</h1>"
        for header_name in stylesheet_colors[stylesheet_name]:
            message += f'<h2>Заголовок {header_name}</h2>'
            message += f'\n<p>Тег "color": '
            positive = stylesheet_colors[stylesheet_name][header_name] != stylesheet_colors["original"][header_name]
            if stylesheet_colors[stylesheet_name][header_name] == stylesheet_colors["original"][header_name]:
                message += f'<tagname style="color:green">совпадает</tagname> ' \
                           f'(Эталон: {stylesheet_colors["original"][header_name]}))'
            else:
                message += f'<tagname style="color:red">несовпадает</tagname> ' \
                           f'(Эталон: {stylesheet_colors["original"][header_name]}, текущий: {stylesheet_colors[stylesheet_name][header_name]})'


            message += f'</p><p>Сравнение скриншотов: '
            if compare_images(f"./images/{stylesheet_name}/{header_name}.png", f"./images/without-styles/{header_name}.png"):
                message += '<tagname style="color:green">совпадают</tagname>'
            else:
                message += '<tagname style="color:red">несовпадают</tagname>'
            message += f'</p><div style="border: 1px solid #ccc"><img src="./images/{stylesheet_name}/{header_name}.png"><br><img src="./images/without-styles/{header_name}.png"></div>'
            message += '\n'
        message += "</div>"
        if positive:
            positive_stylesheets.append(stylesheet_name)
        else:
            negative_stylesheets.append(stylesheet_name)

    with open('report.html', 'w') as f:
        positive_buttons = ""
        negative_buttons = ""
        for i in positive_stylesheets:
            positive_buttons += f'<button class="groupLinks" onclick="openEntry(event, \'{i}\')">{stylesheet_id_to_path[i]}</button>\n'
        for i in negative_stylesheets:
            negative_buttons += f'<button class="groupLinks" onclick="openEntry(event, \'{i}\')">{stylesheet_id_to_path[i]}</button>\n'
        f.write(html.html_template.format(positive_buttons, negative_buttons, message))


if __name__ == '__main__':
    main()
