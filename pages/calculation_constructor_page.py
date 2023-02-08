import allure
from pages.base_page import BasePage
from config import current_stand
from locators.calculation_constructor_locators import CalculationConstructorLocators as CCLocators
from files.files_list import CalculationConstructorFilesList as CCFiles
from selenium.webdriver.common.by import By
from time import sleep
from random import randint

# Переменные
calculation_current_stand = current_stand + "calculation-constructor"


class CalculationConstructorPage(BasePage):

    # Функция для проверки корректная ли страница открыта
    def is_page_calculation_page(self):
        assert self.check_url(calculation_current_stand), \
             "Открыта страница, отличная от Конструктора расчетов"

    # Функция для перехода в Конструктор расчетов
    def move_to_calculation_constructor_page(self):
        assert self.check_url(current_stand), "Открыта страница, отличная от стенда экономики"
        self.click_on_visible_element(CCLocators.move_to_calculation_constructor_page_button)

    # Функция для удаления всех мастеркниг со стенда
    def delete_all_masterbooks(self):
        if not self.visible_element_present(CCLocators.first_MB):
            # Если на стенде нет МастерКниг, то пропускаем удаление
            return
        with allure.step("Подчет всех МК на стенде"):
            mb_num = CalculationConstructorPage.mb_counter(self)
        with allure.step("Удаление всех МК на стенде"):
            for k in range(mb_num):
                self.click_on_visible_element(CCLocators.additional_menu_first_MB)
                self.click_on_visible_element(CCLocators.second_button_MB)
                self.click_on_visible_element(CCLocators.confirm_delete_button_MB)
                sleep(1)
        with allure.step("Проверка остались ли МК на странице"):
            if self.visible_element_present(CCLocators.first_MB):
                assert False, "Какая-то из мастеркниг не удалилась со стенда"
        with allure.step("F5 и повторная проверка"):
            self.refresh()
            sleep(1)
            if not self.visible_element_present(CCLocators.first_MB):
                pass
            else:
                assert False, "Какая-то из мастеркниг не удалилась со стенда."

    # Функция, которая считает мастеркниги на стенде и возвращает их количество
    def mb_counter(self):
        mb_num = 0
        for i in range(1, 1001):
            mb_locator = (By.CSS_SELECTOR, '#root > div > div:nth-child(3) > div > div > div:nth-child(1) > div > div >'
                                           ' div > div.MuiGrid-root.css-rfnosa > div:nth-child(' + str(i + 1) + ')')
            if not self.visible_element_present(mb_locator):
                break
            mb_num += 1
        return mb_num

    # Функция, которая принимает название МК и список его кейсов. Проходится по всем МК, находит нужную, открывает,
    # считает кейсы, сверяет их число с ожидаемым
    def mb_checker(self, mb_name, mb_list):
        if not self.visible_element_present(CCLocators.first_MB):
            assert False, "МастерКниги отсутствуют на стенде"
        mb_num = CalculationConstructorPage.mb_counter(self)
        case_counter = 0
        # Проходимся по всем МК
        with allure.step("Проходимся по всем МК"):
            for i in range(1, mb_num + 1):
                mb_locator = (By.CSS_SELECTOR,
                              '#root > div > div:nth-child(3) > div > div > div:nth-child(1) > div > div > div > div.Mu'
                              'iGrid-root.css-rfnosa > div:nth-child(' + str(i + 1) + ') > div > div > p')
                if self.text_of_visible_element(mb_locator) == mb_name:
                    with allure.step(f"МК {mb_name} найдена, раскрываем список ее кейсов"):
                        self.click_on_visible_element((By.CSS_SELECTOR,
                                                       '#root > div.MuiBox-root.css-18cq61h > div:nth-child(3) > div > '
                                                       'div > div:nth-child(1) > div > div > div > div.MuiGrid-root.css'
                                                       '-rfnosa > div:nth-child(' + str(i + 1) +
                                                       ') > div > div:nth-child(2) > svg'))
                    if not self.visible_element_present((By.CSS_SELECTOR,
                                                         '#root > div.MuiBox-root.css-18cq61h > div:nth-child(3) > div '
                                                         '> div > div:nth-child(1) > div > div > div > div.MuiGrid-root'
                                                         '.css-rfnosa > div.MuiPaper-root.MuiPaper-elevation.MuiPaper-r'
                                                         'ounded.MuiPaper-elevation1.MuiAccordion-root.MuiAccordion-rou'
                                                         'nded.Mui-expanded.MuiAccordion-gutters.css-1wsq4x7 > div.MuiC'
                                                         'ollapse-root.MuiCollapse-vertical.MuiCollapse-entered.css-c4s'
                                                         'utr > div > div > div > div > ul > div:nth-child(1) > div > l'
                                                         'i > span')):
                        assert False, "Не найден кейс, похоже, что загрузилась пустая МК"
                    with allure.step("Проходимся по всем кейсам в МК"):
                        for j in range(1, len(mb_list)):
                            case_locator = (By.CSS_SELECTOR,
                                            '#root > div > div:nth-child(3) > div > div > div:nth-child(1) > div > div '
                                            '> div > div> div > div.MuiCollapse-root.MuiCollapse-vertical.MuiCollapse-e'
                                            'ntered.css-c4sutr > div > div > div > div > ul > div:nth-child(' +
                                            str(j) + ') > div > li > span')
                            # Сравниваем название кейса с названием из списка
                            for k in range(len(mb_list)):
                                case_name = self.text_of_visible_element(case_locator)
                                if case_name == mb_list[k]:
                                    case_counter += 1
                    with allure.step("Сверка посчитанных кейсов с ожидаемым числом"):
                        if case_counter != len(mb_list):
                            print(case_name)
                            # assert False, "Потерян один из кейсов"

                        elif case_counter == len(mb_list):
                            # Закрываем список кейсов
                            self.click_on_visible_element((By.CSS_SELECTOR,
                                                           '#root > div.MuiBox-root.css-18cq61h > div:nth-child(3) > di'
                                                           'v > div > div:nth-child(1) > div > div > div > div.MuiGrid-'
                                                           'root.css-rfnosa > div:nth-child(' + str(i + 1) +
                                                           ') > div > div:nth-child(2) > svg'))
                            pass
                else:
                    continue

    # Функция, которая принимает название МК и максимальный таймер ожидания. Загружает МК на стенд и запускает проверки
    # по всем консолидациям
    def upload_mb(self, mb_name, timer):
        # Блок, который разбирается какую консолидацию и список кейсов прикрепить в запрос к чекеру
        if mb_name == CCFiles.MB_GEE_filename:
            file, cons_list, cases_list = CCFiles.MB_GEE_dir, CCFiles.MB_GEE_consolidations, CCFiles.MB_GEE_cases
        elif mb_name == CCFiles.MB_KUV_filename:
            file, cons_list, cases_list = CCFiles.MB_KUV_dir, CCFiles.MB_KUV_consolidations, CCFiles.MB_KUV_cases
        elif mb_name == CCFiles.MB_CNT_filename:
            file, cons_list, cases_list = CCFiles.MB_CNT_dir, CCFiles.MB_CNT_consolidations, CCFiles.MB_CNT_cases
        elif mb_name == CCFiles.MB_YUUNG_filename:
            file, cons_list, cases_list = CCFiles.MB_YUUNG_dir, CCFiles.MB_YUUNG_consolidations, CCFiles.MB_YUUNG_cases
        elif mb_name == CCFiles.MB_YUUNG_BUR_filename:
            file, cons_list, cases_list = CCFiles.MB_YUUNG_BUR_dir, CCFiles.MB_YUUNG_BUR_consolidations, \
                                           CCFiles.MB_YUUNG_BUR_cases
        elif mb_name == CCFiles.MB_YAG_filename:
            file, cons_list, cases_list = CCFiles.MB_YAG_dir, CCFiles.MB_YAG_consolidations, CCFiles.MB_YAG_cases
        else:
            assert False, "Неизвестное название МК"

        with allure.step("Подсчет МК на стенде до начала загрузки"):
            mb_num = CalculationConstructorPage.mb_counter(self)
        with allure.step("Загрузка файла и ожидание его появления на фронте"):
            self.send_keys_to_hidden_element(CCLocators.upload_MB, file)
            for i in range(timer // 6):
                new_mb_num = CalculationConstructorPage.mb_counter(self)
                if new_mb_num > mb_num:
                    break
        with allure.step("Проверка что при загрузке ничего не потерялось"):
            for j in range(len(cons_list)):
                CalculationConstructorPage.mb_checker(self, cons_list[j], cases_list[j])

    # Функция выбирает случайный кейс, первые попавшиеся ФЭМ и Макру, производит расчет, скачивает полученный отчет и
    # проверяет скачался ли файл
    def calculate_random_case(self):
        with allure.step("Подсчет количества МК на стенде"):
            mb_num = CalculationConstructorPage.mb_counter(self)
        # TODO: а если в консолидации всего один кейс и он в черном списке?
        with allure.step("Поиск подходящего кейса среди случайных"):
            for i in range(1, mb_num+1):
                with allure.step("Выбор случайной консолидации"):
                    mb_num = randint(1, mb_num)
                    mb_locat = (By.CSS_SELECTOR,
                                '#root > div.MuiBox-root.css-18cq61h > div:nth-child(3) > div > div > div:nth-child(1) '
                                '> div > div > div > div.MuiGrid-root.css-rfnosa > div:nth-child(' + str(mb_num + 1) +
                                ') > div > div:nth-child(2) > svg')
                    mb_name = self.text_of_visible_element(mb_locat)
                    if mb_name in CCFiles.consolidations_black_list:
                        continue
                with allure.step(f"Раскрытие консолидации с названием {mb_name}"):
                    self.click_on_visible_element(mb_locat)
                with allure.step("Подсчет кейсов в консолидации"):
                    case_counter = 0
                    for j in range(1, 36):
                        # TODO: прописать локатор для кейса
                        if self.visible_element_present('case_locator'):
                            case_counter += 1
                        else:
                            break
                with allure.step("Выбор случайного кейса"):
                    case_num = str(randint(1, case_counter + 1))
                    case_locator = (By.CSS_SELECTOR,'' + case_num + ''
                                    )
                    case_name = self.text_of_visible_element('case_locator')
                    if case_name in CCFiles.cases_black_list:
                        print(f'Кейс с названием {case_name} находится в черном списке, подбираю другой...')
                        continue
                    else:
                        self.click_on_visible_element('case_locator')
                        break
            with allure.step("Выбор первых в списке ФЭМ и макропараметров"):
                # TODO: остановился тут
                pass
