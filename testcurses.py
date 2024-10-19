import curses
from DataBaseMySQL import DataBase
from config import *


def slide_one(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Парсинг логов apache")
    stdscr.addstr(2, 0, "Данная программа парсит логи apache в linux ubuntu и записывает их в Базу данных MySQL.")
    stdscr.addstr(3, 0, "Доступный функционал:")
    stdscr.addstr(4, 0, "1. Парсинг логов apache и их запись в БД")
    stdscr.addstr(5, 0, "2. Выборка из записей БД и группировка по дате")
    stdscr.addstr(6, 0, "3. Создание файла json с сохраненными данными в БД")
    stdscr.addstr(9, 0, "Нажмите \"пробел\" чтобы продолжить")
    stdscr.refresh()
    while True:
        k = stdscr.getch()
        if k == 32 or k == ord(' '):
            break   

def header_check_db(stdscr):
    stdscr.clear()
    database = user_db.get('database')
    host = user_db.get('host')
    user = user_db.get('user')
    password = user_db.get('password')
    
    db = None
    errorString = None
    try:
        db = DataBase(database, host, user, password)    
    except ConnectionError as err:
        errorString = str(err)

    stdscr.addstr(0, 0, "Статус БД - ")
    if db and db.is_connected():
        stdscr.addstr(0, 12, "Подключено\n", curses.color_pair(2))
        return db
    else:
        stdscr.addstr(0, 12, f"Отключено", curses.color_pair(1))
        stdscr.addstr(1, 0, errorString, curses.color_pair(1))

        stdscr.addstr(5, 0, "press any key...")
        stdscr.getkey()


def footer_main(stdscr):
    stdscr.addstr("\n\n")
    stdscr.addstr("1.Показать записи  ")
    stdscr.addstr("2.Выборка по дате  ")
    stdscr.addstr("3.Схоранить новые записи в бд  ")
    stdscr.addstr("4.Удалить записи в БД  ", curses.color_pair(1))
    stdscr.addstr("5.Сохранить записи в формате json  ")

    while True:
        k = stdscr.getch()
        if k == 49:
            showDB_shell(stdscr)
        if k == 50:
            pass
        if k == 51:
            pass
        if k == 52:
            DeleteDB_Sheel(stdscr)
        if k == 53:
            SaveToJSONShell(stdscr)

def showDB_shell(stdscr):
    stdscr.clear()
    db = header_check_db(stdscr)
    date_show = db.ShowData()
    stdscr.addstr(2, 0, f"Всего записей - {len(date_show)}")
    row_num = 3
    for row in date_show:
        stdscr.addstr(row_num, 0, str(row))
        row_num += 1
        if row_num == 13:
            break
    stdscr.addstr(14, 0, "Показаны последние 10 записей")
    stdscr.refresh()
    footer_main(stdscr)

def DeleteDB_Sheel(stdscr):
    stdscr.clear()
    db = header_check_db(stdscr)
    stdscr.addstr("Вы уверены? Y\\n")
    while True:
        k = stdscr.getch()
        if k == 89 or k == 121:
            db.DeleteData()
        if k == 78 or k == 110:
            break
    
    slide_main(stdscr)


def SaveToJSONShell(stdscr):
    stdscr.clear()
    db = header_check_db(stdscr)
    db.SaveToJSON()
    stdscr.addstr("Файл ")
    stdscr.addstr("database.json ", curses.color_pair(2))
    stdscr.addstr("Сохранен в файле проекта")
    stdscr.refresh()
    footer_main(stdscr)



def slide_main(stdscr):
    header_check_db(stdscr)

    footer_main(stdscr)

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.cbreak()  # Включаем режим cbreak
    stdscr.keypad(True)  # Включаем обработку специальных клавиш (например, стрелок)
    curses.noecho()
    curses.curs_set(0)
 
    #slide_one(stdscr)
    slide_main(stdscr)
    

    
    


    stdscr.refresh()
    stdscr.getkey() 



    curses.nocbreak()
    stdscr.keypad(False)
    curses.curs_set(1)
    curses.echo()
    curses.endwin()

# Запуск через специальную обертку для правильной инициализации/деинициализации curses
curses.wrapper(main)

