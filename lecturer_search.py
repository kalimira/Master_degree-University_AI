import re
import requests
from bs4 import BeautifulSoup as soup
from urllib.parse import urljoin
import mysql.connector
import tkinter as tk
from tkinter import *
import googletrans
from googletrans import *


button_course = False
button_lecturer = False
button_subject = False
cyrillic_translit={'\u0410': 'A', '\u0430': 'a',
    '\u0411': 'B', '\u0431': 'b',
    '\u0412': 'V', '\u0432': 'v',
    '\u0413': 'G', '\u0433': 'g',
    '\u0414': 'D', '\u0434': 'd',
    '\u0415': 'E', '\u0435': 'e',
    '\u0416': 'Zh', '\u0436': 'zh',
    '\u0417': 'Z', '\u0437': 'z',
    '\u0418': 'I', '\u0438': 'i',
    '\u0419': 'Y', '\u0439': 'y',
    '\u041a': 'K', '\u043a': 'k',
    '\u041b': 'L', '\u043b': 'l',
    '\u041c': 'M', '\u043c': 'm',
    '\u041d': 'N', '\u043d': 'n',
    '\u041e': 'O', '\u043e': 'o',
    '\u041f': 'P', '\u043f': 'p',
    '\u0420': 'R', '\u0440': 'r',
    '\u0421': 'S', '\u0441': 's',
    '\u0422': 'T', '\u0442': 't',
    '\u0423': 'U', '\u0443': 'u',
    '\u0424': 'F', '\u0444': 'f',
    '\u0425': 'Kh', '\u0445': 'kh',
    '\u0426': 'Ts', '\u0446': 'ts',
    '\u0427': 'Ch', '\u0447': 'ch',
    '\u0428': 'Sh', '\u0448': 'sh',
    '\u0429': 'Shch', '\u0449': 'shch',
    '\u042a': '"', '\u044a': '"',
    '\u042b': 'Y', '\u044b': 'y',
    '\u042c': "'", '\u044c': "'",
    '\u042d': 'E', '\u044d': 'e',
    '\u042e': 'Iu', '\u044e': 'iu',
    '\u042f': 'Ia', '\u044f': 'a'}


class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.text = tk.Text(master)        
        self.text.pack()
    def show_dict(self, d):
        for k, v in d.items():
            self.text.insert(tk.END," {} -> {}\n".format(k, v))

class window():
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Search lecturer")
        tk.Label(self.master, text="Search: ", font=('Times 20')).grid(row=0, padx=55, pady=55)
        self.e1 = tk.Entry(self.master, width=19, font=('Times 20'))
        self.e1.grid(row=0, column=1)
        self.search_lecturer()

    def search_lecturer(self):    
        btn = tk.Button(self.master, text='Course', command=lambda: self.change_value_course(), height=2, width=10,
                font=('Times 15')).grid(row=3, column=0, padx=50, sticky=tk.W, pady=12)
        btn1 = tk.Button(self.master, text='Lecturer', command=lambda: self.change_value_lecturer(), height=2, width=10,
                font=('Times 15')).grid(row=3, column=1, padx=50, sticky=tk.W, pady=12)
        btn2 = tk.Button(self.master, text='Subject', command=lambda: self.change_value_subject(), height=2, width=10,
                font=('Times 15')).grid(row=3, column=2, padx=50, sticky=tk.W, pady=12)
        tk.mainloop()
        return

    def change_value_course(self):
        global button_course
        global input
        if button_course:
            button_course=False
        if not button_course:
            input = self.e1.get()
            search_courses({'search': input})
            button_course=True

    def change_value_lecturer(self):
        global button_lecturer
        print('buton', button_lecturer)
        if button_lecturer:
            print('tuk')
            button_lecturer=False
        if not button_lecturer:
            input = self.e1.get()
            print('in', input)
            res = check_db(input)
            print('res', res)
        if not res:
            check_lecturer({'search': input})
            button_lecturer=True
        
    def change_value_subject(self):
        global button_subject
        if button_subject:
            button_subject=False
        if not button_subject:
            input = self.e1.get()
            res = search_subjects(input)
            button_subject=True


def translate_name(name):
    if "д-р" in name:
        name += " PhD"
    replace_dict = {"доц. д-р":"Assoc. Prof.", "гл. ас. д-р":"Principal Ass. Prof.", "инж.":"eng", "Програмист - инж.": "Programmer eng."}
    for key, value in replace_dict.items():
        name = name.replace(key, value)
    converted_words = ''
    for char in name:
        transchar = ''
        if char in cyrillic_translit:
            transchar = cyrillic_translit[char]
        else:
            transchar = char
        converted_words += transchar
    return converted_words

def connect_to_db():
    conn = mysql.connector.connect(host="localhost",user="root",password="robo_test_pass",database="robo_data")
    return conn

def check_db(name):
    conn = connect_to_db()
    cursor = conn.cursor()
    #name = name.capitalize()
    print('my name', name)
    query = "SELECT name FROM lecturers "
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    for elt in result:
        for word in elt:
            if name in word:
                print('every name', name)
                query = "SELECT name, cabinet, telephone, mail, subjects FROM lecturers WHERE name=%s"
                val = (word,)
                cursor.execute(query, val)
                teacher = cursor.fetchone()
                print('teacher', teacher)
                data = {"name": teacher[0], "cabinet": teacher[1], "telephone": teacher[2], "e-mail": teacher[3], "subjects": teacher[4]}
                visualisation(data)
                print('tuksss')
                cursor.close()
                return True
    cursor.close()
    return False

def visualisation(data):
    root = tk.Tk()
    app = Application(root)
    app.show_dict(data)
    app.mainloop()

def search_courses(body):
    try:
        text = requests.get("http://www.tu-plovdiv.bg/en/search.php?", params=body, verify=False)
        content = soup(text.content, 'html.parser')
        for item in content.find_all('a'):
            article = re.match(r'course.*', item['href'])
            if article:    
                item_str = str(item)
                if body['search'] in item_str.lower():
                    page = article.group(0)
                    break
        base_url = "http://www.tu-plovdiv.bg/en/"
        path = page
        url = urljoin(base_url, path)
        response = requests.get(url, verify=False)   
        page_content = soup(response.content, 'html.parser')
        header = page_content.h3.text
        name = page_content.h3.get_text()
        result = page_content.find(class_="content-body-text")
        res_txt = result.get_text()
        data = {header : res_txt}
        visualisation(data)      
    except Exception as e:
        print('The search cannot be executed because of error {}'.format(e))

def search_subjects(sub):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT name FROM lecturers WHERE subjects LIKE '%"+sub+"%'"
    cursor.execute(query)
    result = cursor.fetchall()
    lecturers = []
    for elt in result:
        lecturers.append(elt[0])
    data = {'lecturers': lecturers}
    visualisation(data)
    cursor.close()
    return False

def check_lecturer(body):
    try:
        text = requests.get("http://www.tu-plovdiv.bg/search.php", params=body, verify=False)
        content = soup(text.content, 'html.parser')
        #content_split = content.prettify
        for item in content.find_all('a'): 
            article = re.match(r'lecturers_article.*', item['href'])
            if article:
                page = article.group(0)
        base_url = "http://www.tu-plovdiv.bg/"
        path = page
        url = urljoin(base_url, path)
        response = requests.get(url, verify=False)
        page_content = soup(response.content, 'html.parser')
        name = page_content.h3.get_text()
        result = page_content.find(class_="content-body-text")
        res_txt = result.get_text()
        cabinet = re.search('Кабинет:+\s+\d*', res_txt).group(0)
        cabinet_num = re.search(r'\d+', cabinet).group(0)
        telephone = re.search('тел:+\s+(?:[\d]+-)\d+', res_txt)
        if telephone:
            telephone = telephone.group(0)
            tel_num = re.search(r'[\d]+-\d+', telephone).group(0)
        else:
            telephone = re.search('тел.:+\s+\d*', res_txt).group(0)
            tel_num = re.search(r'\d+', telephone).group(0)
        mail = re.search(r'(?<=\s)\S*@\S*', res_txt).group(0)
        subjects = re.search('Дисциплини:+.*', res_txt)
        if subjects:
            subjects = subjects.group(0)
        else:
            subjects = re.search('Водени дисциплини:+.*', res_txt)
            subjects = subjects.group(0)       
        if 'Професионални' in subjects:
            subj = subjects.split('Професионални')
            subj = subj[0].split('Лична')
            sub = subj[0]
        elif 'Интереси' in subjects:
            subj = subjects.split('Интереси')
            subj = subj[0].split('Лична')
            sub = subj[0]
        else:
            sub = subjects
            subj = sub.split('Лична')
            sub = subj[0]
        name = translate_name(name)
        subs = re.search(':+.*', sub).group(0)
        subs = subs.replace(':', '')
        translator = googletrans.Translator()
        translate = translator.translate(subs, dest='en')
        subs_translated = replace_subjects(translate.text)
        data = {"name": name, "cabinet": cabinet_num, "telephone": tel_num, "e-mail": mail, "subjects": subs_translated}
        visualisation(data)

        save_data(data)
    except Exception as e:
        print('The search cannot be executed because of error {}'.format(e))

def replace_subjects(subs):
    if 'English' in subs:
        subs = subs.replace('of English', 'En')
    if 'Gride' in subs:
        subs = subs.replace('Gride', 'Grid')
    if 'built' in subs:
        subs = subs.replace('built -in', 'Embedded')
    if 'self -study in ' in subs:
        subs = subs.replace('Training and self -study', 'Machine learning')
    return subs

def save_data(data):
    print('DATA FOR SAFE', data)
    conn = connect_to_db()
    cursor = conn.cursor()
    name = data['name']
    cabinet_num = data['cabinet']
    tel_num = data['telephone']
    mail = data['e-mail']
    subs = data['subjects']
    query = "INSERT INTO lecturers (name, cabinet, telephone, mail, subjects) VALUES(%s, %s, %s, %s, %s)"
    val = (name, cabinet_num, tel_num, mail, subs)
    cursor.execute(query, val)
    conn.commit()
    cursor.close()

def take_jokes():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT joke FROM jokes "
    cursor.execute(query)
    result = cursor.fetchall()
    jokes = []
    for elt in result:
        joke = elt[0]
        jokes.append(joke)
    conn.commit()
    cursor.close()
    return jokes
