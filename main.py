from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb

def del_text():
    answer = mb.askokcancel('Удаление текста', 'Реально удалить?')
    if answer:
        text.delete(1.0, END)

def insert_text():
    file_name = fd.askopenfilename(
        filetypes=(("TXT files", "*.txt"),
                   ("HTML files", "*.html;*.htm"),
                   ("All files", "*.*"))
    )
    try:
        f = open(file_name)
    except (FileNotFoundError, TypeError):
        mb.showinfo("Открытие файла", "Файл не выбран!")
    else:
        s = f.read()
        text.delete(1.0, END)
        text.insert(1.0, s)
        f.close()

def extract_text():
    file_name = fd.asksaveasfilename(
        defaultextension=".txt",
        filetypes=(("TXT files", "*.txt"),
                   ("HTML files", "*.html;*.htm"),
                   ("All files", "*.*"))
    )
    try:
        f = open(file_name, 'w')
    except (FileNotFoundError, TypeError):
        mb.showinfo("Сохранение файла", "Файл не сохранен!")
    else:
        s = text.get(1.0, END)
        f.write(s)
        f.close()

# НОВАЯ ФУНКЦИЯ
def get_stats():
    content = text.get(1.0, END).rstrip('\n')
    chars = len(content)
    chars_no_space = len(''.join(content.split()))
    words = len(content.split())
    lines = len(content.splitlines())
    mb.showinfo(
        "Статистика текста",
        f"Символов (с пробелами): {chars}\n"
        f"Символов (без пробелов): {chars_no_space}\n"
        f"Слов: {words}\n"
        f"Строк: {lines}"
    )

root = Tk()
root.title("Текстовый редактор с меню")
root.geometry("600x500")

mainmenu = Menu(root)

filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Открыть", command=insert_text)
filemenu.add_command(label="Сохранить", command=extract_text)
filemenu.add_separator()
filemenu.add_command(label="Выход", command=root.quit)

editmenu = Menu(mainmenu, tearoff=0)
editmenu.add_command(label="Очистить", command=del_text)

# НОВОЕ МЕНЮ "ИНСТРУМЕНТЫ"
toolmenu = Menu(mainmenu, tearoff=0)
toolmenu.add_command(label="Статистика", command=get_stats)

mainmenu.add_cascade(label="Файл", menu=filemenu)
mainmenu.add_cascade(label="Правка", menu=editmenu)
mainmenu.add_cascade(label="Инструменты", menu=toolmenu)  # добавлено

root.config(menu=mainmenu)

text = Text(root, width=70, height=30, wrap=WORD, font=("Arial", 11))
text.pack(expand=True, fill=BOTH, padx=10, pady=10)

popupmenu = Menu(text, tearoff=0)
popupmenu.add_command(label="Очистить", command=del_text)
popupmenu.add_command(label="Статистика", command=get_stats)  # добавлено

text.bind('<Button-3>',
          lambda event: popupmenu.post(event.x_root, event.y_root))

root.mainloop()