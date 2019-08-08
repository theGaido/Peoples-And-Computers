from tkinter import *
from tkinter import Frame, messagebox, simpledialog
import tkinter as tk
import tkinter.ttk as ttk
import pyperclip
import generaldefinitions
import plkdatabase
import constants
import re

# === FUNCTIONS


def change_item_description():
    item_name = plk_tree.item(plk_tree.selection())["text"]
    if item_name not in constants.DB_TYPE_NAME_LIST:
        change_description = messagebox.askquestion("Info", "Zmienić opis?")
        if change_description == "yes":
            new_description = simpledialog.askstring(
                "Info", "Podaj nowy opis dla " + item_name + '.',
                parent=main_window)
            connection = plkdatabase.create_connection(constants.DB_NAME)
            if connection is not None:
                old_description = plkdatabase.get_description(connection, item_name)[0][0]
                plkdatabase.update_description(connection, item_name, new_description)
                now = generaldefinitions.get_time()
                info = constants.CHANGE_DESCRIPTION_INFO + now + " z [" + old_description + "] na [" + new_description + "]. \n"
                notes = plkdatabase.get_notes(connection, item_name)[0][0]
                notes = info + notes
                plkdatabase.update_notes(connection, item_name, notes)
                plkdatabase.update_modification_time(connection, item_name, now)
                update_tree_list()
                load_memo_info()
            connection.close()


def change_item_name():
    item_name = plk_tree.item(plk_tree.selection())["text"]
    if item_name not in constants.DB_TYPE_NAME_LIST:
        change_name = messagebox.askquestion("Info", "Zmienić nazwę?")
        if change_name == "yes":
            new_name = simpledialog.askstring("Info", "Podaj nową nazwę dla " + item_name + '.')
            new_name = new_name.upper()
            new_name = new_name.translate({ord(c): None for c in ' \n\t\r'})
            if new_name == "":
                messagebox.showerror("Info", "Nazwa jest pusta.")
            else:
                connection = plkdatabase.create_connection(constants.DB_NAME)
                if connection is not None:
                    plkdatabase.update_name(connection, item_name, new_name)
                    now = generaldefinitions.get_time()
                    info = constants.CHANGE_NAME_INFO + now + " z [" + item_name + "] na [" + new_name + "]. \n"
                    notes = plkdatabase.get_notes(connection, new_name)[0][0]
                    notes = info + notes
                    plkdatabase.update_notes(connection, new_name, notes)
                    plkdatabase.update_modification_time(connection, new_name, now)
                    update_tree_list()
                connection.close()


def change_item_type():
    item_name = plk_tree.item(plk_tree.selection())["text"]
    connection = plkdatabase.create_connection(constants.DB_NAME)
    if item_name not in constants.DB_TYPE_NAME_LIST:
        change_type = messagebox.askquestion("Info", "Zmienić typ dla " + item_name + "?")
        if change_type == "yes":
            old_type = plkdatabase.get_type(connection, item_name)[0][0]
            info = """Podaj nową nazwę typu.
            Dozwolone typy:
            USER dla użytkowników,
            COMPUTER dla komputerów,
            DEVICE dla urządzeń,
            PROGRAM dla programów,
            TIP dla wskazówek."""
            new_type = simpledialog.askstring(item_name + ": Zmiana typu", info)
            if new_type != "":
                new_type = str(new_type)
                new_type = new_type.upper()
                new_type = new_type.translate({ord(c): None for c in ' \n\t\r'})
                if new_type in constants.DB_TYPE_VALUE_LIST:
                    plkdatabase.update_type(connection, item_name, new_type)
                    now = generaldefinitions.get_time()
                    info = constants.CHANGE_TYPE_INFO + now + " z [" + old_type + "] na [" + new_type + "]. \n"
                    notes = plkdatabase.get_notes(connection, item_name)[0][0]
                    notes = info + notes
                    plkdatabase.update_notes(connection, item_name, notes)
                    plkdatabase.update_modification_time(connection, item_name, now)
                    load_memo_info()
                    update_tree_list()
                else:
                    messagebox.showerror("Info", "Błędny typ")
    connection.close()


def color_memo_text():
    color_tag(constants.MEMO_TAG_DATE,
              constants.REG_DATES, 0)
    color_tag(constants.MEMO_TAG_INFO,
              constants.REG_ADD_ITEM_INFO, 0)
    color_tag(constants.MEMO_TAG_INFO,
              constants.REG_CHANGE_DESCRIPTION_INFO, 0)
    color_tag(constants.MEMO_TAG_INFO,
              constants.REG_CHANGE_NAME_INFO, 0)
    color_tag(constants.MEMO_TAG_INFO,
              constants.REG_CHANGE_TYPE_INFO, 0)
    color_tag(constants.MEMO_TAG_PLK_NUMBER,
              constants.REG_PLK_NUMBER, 0)
    color_tag(constants.MEMO_TAG_COMPUTER_NAME,
              constants.REG_COMPUTER_NUMBER, 0)
    color_tag(constants.MEMO_TAG_EMAIL,
              constants.REG_EMAIL, 1)
    color_tag(constants.MEMO_TAG_WEBPAGE,
              constants.REG_WEBPAGE, 1)
    color_tag(constants.MEMO_TAG_EMILKA_APPLICATION,
              constants.REG_EMILKA_APPLICATION, 0)
    color_tag(constants.MEMO_TAG_HASHTAG,
              constants.REG_HASHTAG, 0)
    item_name = search_entry.get()
    if item_name[:2] == "->":
        item_name = item_name[2:]
        color_tag(constants.MEMO_TAG_SEARCH_STRING, item_name, 1)


def color_tag(tag_name, reg, sensitive):
    txt = plk_user_memo.get("1.0", END)
    if sensitive == 0:
        found_reg = re.findall(reg, txt)
    else:
        found_reg = re.findall(reg, txt, re.IGNORECASE)
    for fitting_text in found_reg:
        fitting_text_position = plk_user_memo.search(fitting_text, "1.0", stopindex=END)
        plk_user_memo.tag_add(tag_name, fitting_text_position, fitting_text_position + "+" + str(len(fitting_text)) + "c")


def copy_memo_to_clipboard():
    pyperclip.copy(plk_user_memo.get("1.0", END))


def explore_file_system():
    hostname = get_hostname()
    connection = plkdatabase.create_connection(constants.DB_NAME)
    if connection is not None:
        if plkdatabase.get_type(connection, hostname)[0][0] == constants.DB_COMPUTER_TYPE_NAME:
            connection.close()
            if generaldefinitions.test_connection(hostname):
                generaldefinitions.explore_host(hostname)
            else:
                messagebox.showerror("Info", hostname + " jest offline.")


def ping():
    item_name = get_hostname()
    connection = plkdatabase.create_connection(constants.DB_NAME)
    if connection is not None:
        type = plkdatabase.get_type(connection, item_name)[0][0]
        connection.close()
        if type == constants.DB_COMPUTER_TYPE_NAME or type == constants.DB_DEVICE_TYPE_NAME:
            generaldefinitions.ping_computer(item_name)


def load_memo_info():
    item_name = get_hostname()
    plk_user_memo.delete("1.0", END)
    if item_name not in constants.DB_TYPE_NAME_LIST:
        connection = plkdatabase.create_connection(constants.DB_NAME)
        if connection is not None:
            some_info = plkdatabase.get_notes(connection, item_name)[0][0]
            plk_user_memo.insert(INSERT, some_info)
            connection.close()
            color_memo_text()
    else:
        plk_user_memo.delete("1.0", END)


def memo_add_line():
    plk_user_memo.insert("1.0", " \n")
    plk_user_memo.mark_set("insert", "%d.%d" % (0,0))


def memo_add_timestamp():
    now = generaldefinitions.get_time()
    plk_user_memo.insert(INSERT, now)


def save_memo_info():
    item_name = get_hostname()
    if item_name not in constants.DB_TYPE_NAME_LIST:
        connection = plkdatabase.create_connection(constants.DB_NAME)
        if connection is not None:
            notes = plk_user_memo.get("1.0", END)
            back_notes = plkdatabase.get_notes(connection, item_name)[0][0]
            if notes[:-1] != back_notes:
                now = generaldefinitions.get_time()
                plkdatabase.update_notes(connection, item_name, notes)
                plkdatabase.update_modification_time(connection, item_name, now)
            connection.close()


def search_entry_insert_text(value):
    search_entry.delete(0, 'end')
    search_entry.insert(0, value)


def set_active_user():
    item_name = plk_tree.item(plk_tree.selection())["text"]
    if item_name in constants.DB_TYPE_NAME_LIST:
        item_name = ""
    current_item_name_label.configure(text=item_name)
    load_memo_info()


def add_item():
    item_name = name_entry.get()
    item_name = item_name.upper()
    item_name = item_name.translate({ord(c): None for c in ' \n\t\r'})
    if item_name == "":
        messagebox.showerror("Błąd", 'Pole "' + constants.ADD_NAME_LABEL_TEXT + '" nie może być puste.')
    else:
        item_description = description_entry.get()
        item_description = item_description.translate({ord(c): None for c in '\n\t\r'})
        item_type = chosen_type.get()
        if item_type == "":
            messagebox.showerror("Błąd", "Wybierz rodzaj obiektu.")
        else:
            now = generaldefinitions.get_time()
            notes = constants.ADD_ITEM_INFO + now
            sql_insert_values = (item_name, item_type, item_description, notes, now)
            connection = plkdatabase.create_connection(constants.DB_NAME)
            if connection is not None:
                id = plkdatabase.add_item(connection, sql_insert_values)
                if id is not None:
                    messagebox.showinfo("Info", "Zapis dodano do bazy")
                connection.close()
                update_tree_list()


def delete_items():
    if get_hostname() not in constants.DB_TYPE_NAME_LIST:
        do_want_delete = messagebox.askquestion("Info", "Usunąć wybrane elementy?")
        if do_want_delete == "yes":
            connection = plkdatabase.create_connection(constants.DB_NAME)
            if connection is not None:
                selected_items = plk_tree.selection()
                for selected_item in selected_items:
                    item_name = plk_tree.item(selected_item)["text"]
                    plkdatabase.delete_item(connection, item_name)
                    current_item_name_label.config(text="")
                    plk_user_memo.delete("1.0", END)
                connection.close()
                update_tree_list()


def get_hostname():
    return current_item_name_label.cget("text")


def search_item():
    item_name = search_entry.get()
    plk_user_memo.delete("1.0", END)
    set_active_user()
    if len(item_name) >= 3 and item_name != "":
        childrens = plk_tree.get_children()
        for child in childrens:
            plk_tree.delete(child)
        plk_users = plk_tree.insert("", 1, text="Użytkownicy", values=(""), open=True)
        plk_tips = plk_tree.insert("", 1, text="Wskazówki", values=(""), open=True)
        plk_programs = plk_tree.insert("", 1, text="Programy", values=(""), open=True)
        plk_devices = plk_tree.insert("", 1, text="Urządzenia", values=(""), open=True)
        plk_computers = plk_tree.insert("", 1, text="Komputery", values=(""), open=True)
        connection = plkdatabase.create_connection(constants.DB_NAME)
        if connection is not None:
            if item_name[:2] == "->":
                item_name = item_name[2:]
                rows = plkdatabase.select_all_items_with_string_in_notes(connection, item_name)
            else:
                rows = plkdatabase.select_all_items_with_string(connection, item_name)
            if rows is not None:
                for row in rows:
                    item_type, item_name, description, time = str(row).split(",")
                    item_type = item_type.translate({ord(c): None for c in "('"})
                    item_name = item_name.translate({ord(c): None for c in "(' "})
                    description = description.translate({ord(c): None for c in "'"})
                    time = time.translate({ord(c): None for c in "')"})

                    if item_type == constants.DB_USER_TYPE_NAME:
                        plk_tree.insert(plk_users, "end", text=item_name, values=(description, time))
                    elif item_type == constants.DB_COMPUTER_TYPE_NAME:
                        plk_tree.insert(plk_computers, "end", text=item_name, values=(description, time))
                    elif item_type == constants.DB_DEVICE_TYPE_NAME:
                        plk_tree.insert(plk_devices, "end", text=item_name, values=(description, time))
                    elif item_type == constants.DB_PROGRAM_TYPE_NAME:
                        plk_tree.insert(plk_programs, "end", text=item_name, values=(description, time))
                    elif item_type == constants.DB_TIP_TYPE_NAME:
                        plk_tree.insert(plk_tips, "end", text=item_name, values=(description, time))

            connection.close()
    else:
        update_tree_list()


def update_tree_list():
    childrens = plk_tree.get_children()
    for child in childrens:
        plk_tree.delete(child)
    plk_users = plk_tree.insert("", 1, text="Użytkownicy", values=(""), open=True)
    plk_tips = plk_tree.insert("", 1, text="Wskazówki", values=(""), open=True)
    plk_programs = plk_tree.insert("", 1, text="Programy", values=(""), open=True)
    plk_devices = plk_tree.insert("", 1, text="Urządzenia", values=(""), open=True)
    plk_computers = plk_tree.insert("", 1, text="Komputery", values=(""), open=True)
    connection = plkdatabase.create_connection(constants.DB_NAME)
    if connection is not None:
        rows = plkdatabase.select_all_users(connection)
        if rows is not None:
            for row in rows:
                user_name, description, time = str(row).split(",")
                user_name = user_name.translate({ord(c): None for c in "('"})
                description = description.translate({ord(c): None for c in "'"})
                time = time.translate({ord(c): None for c in "')"})
                plk_tree.insert(plk_users, "end", text=user_name, values=(description, time))
        rows = plkdatabase.select_all_computers(connection)
        if rows is not None:
            for row in rows:
                computer_name, description, time = str(row).split(",")
                computer_name = computer_name.translate({ord(c): None for c in "('"})
                description = description.translate({ord(c): None for c in "'"})
                time = time.translate({ord(c): None for c in "')"})
                plk_tree.insert(plk_computers, "end", text=computer_name, values=(description, time))
        rows = plkdatabase.select_all_devices(connection)
        if rows is not None:
            for row in rows:
                device_name, description, time = str(row).split(",")
                device_name = device_name.translate({ord(c): None for c in "('"})
                description = description.translate({ord(c): None for c in "'"})
                time = time.translate({ord(c): None for c in "')"})
                plk_tree.insert(plk_devices, "end", text=device_name, values=(description, time))
        rows = plkdatabase.select_all_programs(connection)
        if rows is not None:
            for row in rows:
                program_name, description, time = str(row).split(",")
                program_name = program_name.translate({ord(c): None for c in "('"})
                description = description.translate({ord(c): None for c in "'"})
                time = time.translate({ord(c): None for c in "')"})
                plk_tree.insert(plk_programs, "end", text=program_name, values=(description, time))
        rows = plkdatabase.select_all_tips(connection)
        if rows is not None:
            for row in rows:
                tip_name, description, time = str(row).split(",")
                tip_name = tip_name.translate({ord(c): None for c in "('"})
                description = description.translate({ord(c): None for c in "'"})
                time = time.translate({ord(c): None for c in "')"})
                plk_tree.insert(plk_tips, "end", text=tip_name, values=(description, time))
        connection.close()


# === EVENTS


def add_item_on_event(event):
    add_item()


def change_item_description_on_event(event):
    change_item_description()


def change_item_name_on_event(event):
    change_item_name()


def change_item_type_on_event(event):
    change_item_type()


def color_memo_on_event(event):
    color_memo_text()


def copy_memo_to_clipboard_on_event(event):
    copy_memo_to_clipboard()


def explore_file_system_on_event(event):
    explore_file_system()


def set_active_user_on_event(event):
    set_active_user()


def search_entry_on_return(event):
    entry_text = str(search_entry.get())
    if entry_text.startswith(constants.COMMAND_PREFIX):
        try:
            command_result = eval(entry_text[len(constants.COMMAND_PREFIX):])
        except:
            command_result = "BŁĄD"
        finally:
            search_entry.insert(INSERT, " = " + str(command_result))


def ping_on_event(event):
    ping()


def delete_items_on_event(event):
    delete_items()


def load_memo_info_on_event(event):
    load_memo_info()


def memo_add_line_on_event(event):
    memo_add_line()


def memo_add_timestamp_on_event(event):
    memo_add_timestamp()


def save_memo_info_on_event(event):
    save_memo_info()


def search_item_on_event(event):
    search_item()


def search_entry_set_command_on_event(event):
    search_entry_insert_text(constants.COMMAND_PREFIX)


def search_entry_set_searching_by_notes_on_event(event):
    search_entry_insert_text("->")


def sort_tree_on_event(event):

    def get_order(val):
        switcher = {
            "heading#0": "name",
            "heading#1": "description",
            "heading#2": "modification_time"
        }
        return switcher.get(val, "")

    region = plk_tree.identify_region(event.x, event.y)
    if region == "heading":
        name = plk_tree.identify_column(event.x)
        order = "ASC"
        if name == "#2":
            order = "DESC"
        header_name = region + name
        header_name = get_order(header_name)
        childrens = plk_tree.get_children()
        for child in childrens:
            plk_tree.delete(child)
        set_active_user()
        plk_users = plk_tree.insert("", 1, text="Użytkownicy", values=(""), open=True)
        plk_tips = plk_tree.insert("", 1, text="Wskazówki", values=(""), open=True)
        plk_programs = plk_tree.insert("", 1, text="Programy", values=(""), open=True)
        plk_devices = plk_tree.insert("", 1, text="Urządzenia", values=(""), open=True)
        plk_computers = plk_tree.insert("", 1, text="Komputery", values=(""), open=True)
        connection = plkdatabase.create_connection(constants.DB_NAME)
        if connection is not None:
            rows = plkdatabase.select_and_order_items(connection, constants.DB_USER_TYPE_NAME, header_name, order)
            if rows is not None:
                for row in rows:
                    user_name, description, time = str(row).split(",")
                    user_name = user_name.translate({ord(c): None for c in "('"})
                    description = description.translate({ord(c): None for c in "'"})
                    time = time.translate({ord(c): None for c in "')"})
                    plk_tree.insert(plk_users, "end", text=user_name, values=(description, time))
            rows = plkdatabase.select_and_order_items(connection, constants.DB_COMPUTER_TYPE_NAME, header_name, order)
            if rows is not None:
                for row in rows:
                    computer_name, description, time = str(row).split(",")
                    computer_name = computer_name.translate({ord(c): None for c in "('"})
                    description = description.translate({ord(c): None for c in "'"})
                    time = time.translate({ord(c): None for c in "')"})
                    plk_tree.insert(plk_computers, "end", text=computer_name, values=(description, time))
            rows = plkdatabase.select_and_order_items(connection, constants.DB_DEVICE_TYPE_NAME, header_name, order)
            if rows is not None:
                for row in rows:
                    device_name, description, time = str(row).split(",")
                    device_name = device_name.translate({ord(c): None for c in "('"})
                    description = description.translate({ord(c): None for c in "'"})
                    time = time.translate({ord(c): None for c in "')"})
                    plk_tree.insert(plk_devices, "end", text=device_name, values=(description, time))
            rows = plkdatabase.select_and_order_items(connection, constants.DB_PROGRAM_TYPE_NAME, header_name, order)
            if rows is not None:
                for row in rows:
                    program_name, description, time = str(row).split(",")
                    program_name = program_name.translate({ord(c): None for c in "('"})
                    description = description.translate({ord(c): None for c in "'"})
                    time = time.translate({ord(c): None for c in "')"})
                    plk_tree.insert(plk_programs, "end", text=program_name, values=(description, time))
            rows = plkdatabase.select_and_order_items(connection, constants.DB_TIP_TYPE_NAME, header_name, order)
            if rows is not None:
                for row in rows:
                    tip_name, description, time = str(row).split(",")
                    tip_name = tip_name.translate({ord(c): None for c in "('"})
                    description = description.translate({ord(c): None for c in "'"})
                    time = time.translate({ord(c): None for c in "')"})
                    plk_tree.insert(plk_tips, "end", text=tip_name, values=(description, time))
            connection.close()


# === WINDOW AND FRAMES ===

main_window = Tk()
main_window.title("Ludzie i komputery")
main_window.iconbitmap(bitmap='icon.ico')
main_window.geometry(constants.MAIN_WINDOW_SIZE)
main_window.resizable(FALSE, FALSE)
main_window.update()

top_frame = Frame(main_window, height=constants.TOP_FRAME_HEIGHT, bg=constants.TOP_FRAME_BG_COLOR)
top_frame.pack(side=TOP, fill=X)

bottom_frame = Frame(main_window, height=constants.BOTTOM_FRAME_HEIGHT, bg=constants.BOTTOM_FRAME_BG_COLOR)
bottom_frame.pack_propagate(False)
bottom_frame.pack(side=BOTTOM, fill=X)

left_frame = Frame(main_window, width=constants.LEFT_FRAME_WIDTH, bg=constants.BOTTOM_FRAME_BG_COLOR)
left_frame.pack_propagate(False)
left_frame.pack(side=LEFT, fill=Y)

right_frame = Frame(main_window, width=main_window.winfo_width()-constants.LEFT_FRAME_WIDTH, bg=constants.BOTTOM_FRAME_BG_COLOR)
right_frame.pack_propagate(False)
right_frame.pack(side=LEFT, fill=BOTH)

passwd = simpledialog.askstring("LiK", "Podaj hasło", show="*")
if passwd == generaldefinitions.generate_password():
    # === WIDGETS ===

    # - TREE STYLE

    tree_style = ttk.Style()
    tree_style.theme_use("classic")
    tree_style.configure("mystyle.Treeview",
                         highlightthickness=0,
                         padding=0,
                         bd=constants.TREE_STYLE_BD,
                         fieldbackground=constants.TREE_STYLE_BG_COLOR,
                         background=constants.TREE_STYLE_BG_COLOR,
                         foreground=constants.TREE_STYLE_FG_COLOR,
                         font=constants.TREE_STYLE_FONT)
    tree_style.configure("mystyle.Treeview.Heading",
                         padding=0,
                         background=constants.TREE_STYLE_BG_COLOR,
                         foreground=constants.TREE_STYLE_FG_COLOR,
                         font=constants.TREE_STYLE_FONT)

    # - TREEVIEW

    plk_tree_scrollbar = Scrollbar(left_frame)
    plk_tree_scrollbar.pack(side=RIGHT, fill=Y)

    plk_tree = ttk.Treeview(
        left_frame,
        style="mystyle.Treeview",
        height=constants.TREE_STYLE_HEIGHT,
        selectmode=BROWSE,
        yscrollcommand=plk_tree_scrollbar.set)
    plk_tree.bind("<Delete>", delete_items_on_event)
    plk_tree.bind("<<TreeviewSelect>>", set_active_user_on_event)
    plk_tree.bind("<Button-1>", sort_tree_on_event)
    plk_tree.bind("<Control-d>", change_item_description_on_event)
    plk_tree.bind("<Control-e>", explore_file_system_on_event)
    plk_tree.bind("<Control-n>", change_item_name_on_event)
    plk_tree.bind("<Control-t>", change_item_type_on_event)
    plk_tree.bind("<Control-p>", ping_on_event)
    plk_tree["columns"] = ("one", "two")
    plk_tree.column("#0", width=constants.TREE_STYLE_COLUMN_WIDTH, minwidth=constants.TREE_STYLE_COLUMN_MINWIDTH,
                    stretch=tk.YES)
    plk_tree.column("one", width=150, minwidth=constants.TREE_STYLE_COLUMN_MINWIDTH, stretch=tk.YES)
    plk_tree.column("two", width=constants.TREE_STYLE_COLUMN_WIDTH, minwidth=constants.TREE_STYLE_COLUMN_MINWIDTH,
                    stretch=tk.YES)
    plk_tree.heading("#0", text="Nazwa", anchor=tk.W)
    plk_tree.heading("one", text="Opis", anchor=tk.W)
    plk_tree.heading("two", text="Data modyfikacji", anchor=tk.W)
    update_tree_list()
    plk_tree.pack(fill=BOTH)
    plk_tree_scrollbar.config(command=plk_tree.yview)

    # - USER MEMO

    plk_user_memo_scrollbar = Scrollbar(right_frame)
    plk_user_memo_scrollbar.pack(side=RIGHT, fill=Y)

    plk_user_memo = Text(right_frame,
                         bd=2,
                         relief=SUNKEN,
                         height=constants.PLK_USER_MEMO_HEIGHT,
                         bg=constants.PLK_USER_MEMO_BG_COLOR,
                         fg=constants.PLK_USER_MEMO_FG_COLOR,
                         font=constants.PLK_USER_MEMO_FONT,
                         insertbackground=constants.PLK_USER_MEMO_FG_COLOR,
                         yscrollcommand=plk_user_memo_scrollbar.set)
    plk_user_memo.tag_configure(constants.MEMO_TAG_INFO, foreground=constants.MEMO_TAG_INFO_FOREGROUND_COLOR)
    plk_user_memo.tag_configure(constants.MEMO_TAG_DATE, foreground=constants.MEMO_TAG_DATE_FOREGROUND_COLOR)
    plk_user_memo.tag_configure(constants.MEMO_TAG_EMAIL, foreground=constants.MEMO_TAG_EMAIL_COLOR)
    plk_user_memo.tag_configure(constants.MEMO_TAG_EMILKA_APPLICATION, foreground=constants.MEMO_TAG_EMILKA_APPLICATION_COLOR)
    plk_user_memo.tag_configure(constants.MEMO_TAG_PLK_NUMBER, foreground=constants.MEMO_TAG_PLK_NUMBER_FOREGROUND_COLOR)
    plk_user_memo.tag_configure(constants.MEMO_TAG_COMPUTER_NAME, foreground=constants.MEMO_TAG_COMPUTER_NAME_FOREGROUND_COLOR)
    plk_user_memo.tag_configure(constants.MEMO_TAG_HASHTAG, foreground=constants.MEMO_TAG_HASHTAG_FOREGROUND_COLOR)
    plk_user_memo.tag_configure(constants.MEMO_TAG_WEBPAGE, foreground=constants.MEMO_TAG_WEBPAGE_COLOR)
    plk_user_memo.tag_configure(constants.MEMO_TAG_SEARCH_STRING,
                                foreground=constants.MEMO_TAG_SEARCH_STRING_FOREGROUND_COLOR,
                                background=constants.MEMO_TAG_SEARCH_STRING_BACKGROUND_COLOR)
    plk_user_memo.bind("<Control-n>", memo_add_line_on_event)
    plk_user_memo.bind("<Control-N>", memo_add_line_on_event)
    plk_user_memo.bind("<Control-s>", save_memo_info_on_event)
    plk_user_memo.bind("<Control-S>", save_memo_info_on_event)
    plk_user_memo.bind("<Control-t>", memo_add_timestamp_on_event)
    plk_user_memo.bind("<Control-T>", memo_add_timestamp_on_event)
    plk_user_memo.bind("<Control-z>", load_memo_info_on_event)
    plk_user_memo.bind("<Control-Z>", load_memo_info_on_event)
    plk_user_memo.bind("<Control-Shift-c>", copy_memo_to_clipboard_on_event)
    plk_user_memo.bind("<Control-Shift-C>", copy_memo_to_clipboard_on_event)
    plk_user_memo.bind("<KeyRelease>", color_memo_on_event)
    plk_user_memo.bind("<Leave>", save_memo_info_on_event)
    plk_user_memo.pack(fill=BOTH)
    plk_user_memo_scrollbar.config(command=plk_user_memo.yview)

    # - TOP FRAME TOOLS

    search_label = Label(top_frame,
                       text=constants.SEARCH_LABEL_TEXT,
                       bg=constants.TOP_FRAME_BG_COLOR,
                       fg=constants.TREE_STYLE_FG_COLOR,
                       font=constants.TREE_STYLE_FONT)
    search_label.pack(side=LEFT)

    # SEARCH ENTRY

    search_entry = Entry(
        top_frame,
        bd=2,
        width=constants.SEARCH_ENTRY_WIIDTH,
        relief=SUNKEN,
        bg=constants.PLK_USER_MEMO_BG_COLOR,
        fg=constants.PLK_USER_MEMO_FG_COLOR,
        font=constants.PLK_USER_MEMO_FONT,
        insertbackground=constants.PLK_USER_MEMO_FG_COLOR)
    search_entry.bind("<Control-c>", search_entry_set_command_on_event)
    search_entry.bind("<Control-C>", search_entry_set_command_on_event)
    search_entry.bind("<Control-s>", search_entry_set_searching_by_notes_on_event)
    search_entry.bind("<Control-S>", search_entry_set_searching_by_notes_on_event)
    search_entry.bind("<KeyRelease>", search_item_on_event)
    search_entry.bind("<Return>",search_entry_on_return)
    search_entry.pack(side=LEFT)

    name_label = Label(top_frame,
                       text=constants.ADD_NAME_LABEL_TEXT,
                       bg=constants.TOP_FRAME_BG_COLOR,
                       fg=constants.TREE_STYLE_FG_COLOR,
                       font=constants.TREE_STYLE_FONT)
    name_label.pack(side=LEFT)

    name_entry = Entry(
        top_frame,
        bd=2,
        width=constants.ADD_NAME_TEXT_WIDTH,
        relief=SUNKEN,
        bg=constants.PLK_USER_MEMO_BG_COLOR,
        fg=constants.PLK_USER_MEMO_FG_COLOR,
        font=constants.PLK_USER_MEMO_FONT,
        insertbackground=constants.PLK_USER_MEMO_FG_COLOR)
    name_entry.pack(side=LEFT)

    description_label = Label(
        top_frame,
        text=constants.ADD_DESCRIPTION_NAME,
        bg=constants.TOP_FRAME_BG_COLOR,
        fg=constants.TREE_STYLE_FG_COLOR,
        font=constants.TREE_STYLE_FONT)
    description_label.pack(side=LEFT)

    description_entry = Entry(
        top_frame,
        bd=2,
        width=constants.ADD_DESCRIPTION_WIDTH,
        relief=SUNKEN,
        bg=constants.PLK_USER_MEMO_BG_COLOR,
        fg=constants.PLK_USER_MEMO_FG_COLOR,
        font=constants.PLK_USER_MEMO_FONT,
        insertbackground=constants.PLK_USER_MEMO_FG_COLOR)
    description_entry.pack(side=LEFT)

    item_types = [("Użytkownik", constants.DB_USER_TYPE_NAME), ("Komputer", constants.DB_COMPUTER_TYPE_NAME),
                  ("Urządzenie", constants.DB_DEVICE_TYPE_NAME), ("Program", constants.DB_PROGRAM_TYPE_NAME),
                  ("Wskazówka", constants.DB_TIP_TYPE_NAME)]
    chosen_type = StringVar()
    chosen_type.set(constants.DB_USER_TYPE_NAME)

    for index, (text_type, db_type) in enumerate(item_types):
        add_item_radiobutton = Radiobutton(
            top_frame,
            height=1,
            bg=constants.BUTTON_BG_COLOR,
            fg=constants.BUTTON_FG_COLOR,
            cursor="hand2",
            indicatoron=0,
            text=text_type,
            variable=chosen_type,
            value=db_type)
        add_item_radiobutton.pack(side=LEFT)

    add_item_button = Button(
        top_frame,
        text=constants.ADD_ITEM_BUTTON_NAME,
        width=10,
        cursor="hand2",
        bg=constants.BUTTON_BG_COLOR,
        fg=constants.BUTTON_FG_COLOR,
        command=add_item)
    add_item_button.bind("<Return>", add_item_on_event)
    add_item_button.pack(side=RIGHT)

    # === BOTTOM FRAME TOOLS

    current_item_label = Label(
        bottom_frame,
        text=constants.CURRENT_USER_LABEL_NAME,
        bg=constants.BOTTOM_FRAME_BG_COLOR,
        fg=constants.PLK_USER_MEMO_FG_COLOR)
    current_item_label.pack(side=LEFT)

    current_item_name_label = Label(
        bottom_frame,
        text="",
        bg=constants.BOTTOM_FRAME_BG_COLOR,
        fg=constants.PLK_USER_MEMO_FG_COLOR)
    current_item_name_label.pack(side=LEFT)

    main_window.mainloop()
