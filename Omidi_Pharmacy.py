import tkinter
from cProfile import label
from logging import root
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

window = Tk()
window.title("Omidi Pharmacy")
window.geometry("800x800")
window.resizable(False, False)
window.config(bg="#E8F5F9")

conn = sqlite3.connect("Omidi_Pharmacy.db")
cursor = conn.cursor()


def create_patient():
    def save():
        nameE = entry_name.get()
        phoneE = entry_phone.get()
        if nameE and phoneE:
            cursor.execute("INSERT INTO Patients (name, phone) VALUES (?, ?)", (nameE, phoneE))
            conn.commit()
            messagebox.showinfo("موفق", "بیمار با موفقیت اضافه شد")
            patient_window.destroy()
        else:
            messagebox.showwarning("خطا", "لطفا همه فیلدها را پر کنید")

    patient_window = Toplevel(window, height=300, width=400, bg='#E8F5F9')
    patient_window.pack_propagate(False)
    (Label(patient_window, text=" :نام بیمار", font=("Arial", 12), anchor="e", justify="right")
     .pack(pady=20))

    entry_name = Entry(patient_window)

    entry_name.pack(pady=20)
    (Label(patient_window, text=" :شماره تماس بیمار", font=("Arial", 12), anchor="e", justify="right")
     .pack(pady=20))
    entry_phone = Entry(patient_window)
    entry_phone.pack(pady=20)
    (Button(patient_window, text="ذخیره", command=save)
     .pack(pady=20))


def patient_login():
    def searchDb():
        phoneE = entry_user_phone.get()
        if phoneE:
            cursor.execute("SELECT patientID FROM Patients WHERE phone=?", (phoneE,))
            result = cursor.fetchone()

            if result:
                messagebox.showinfo("موفق", "بیمار وارد شد")
                global patientid
                patientid = result[0]
                patient_login_window.place_forget()
            else:
                messagebox.showwarning("خطا", "بیمار یافت نشد")

    patient_login_window = Frame(window, bg="lightgray", width=400, height=200)
    patient_login_window.pack_propagate(False)
    patient_login_window.place(x=200, y=200)

    Label(patient_login_window, text="شماره تلفن بیمار:").pack(pady=5)
    entry_user_phone = Entry(patient_login_window)
    entry_user_phone.pack(pady=5)

    Button(patient_login_window, text="ورود", command=searchDb).pack(pady=10)

    def cancel():
        patient_login_window.place_forget()

    Button(patient_login_window, text="انصراف", command=cancel).pack(pady=10)


def delete_patient():
    def removeDb():
        phoneE = entry_user_phone.get()
        if phoneE:
            cursor.execute("DELETE FROM Patients WHERE phone=?", (phoneE,))
            conn.commit()
            if cursor.rowcount == 0:
                messagebox.showwarning("خطا", "بیمار با این شماره تلفن یافت نشد")
            else:
                messagebox.showinfo("موفق", "بیمار با موفقیت حذف شد")

                delete_patient_window.place_forget()

    delete_patient_window = Frame(window, bg="#B3E5FC", width=400, height=200)
    delete_patient_window.pack_propagate(False)
    delete_patient_window.place(x=200, y=200)
    Label(delete_patient_window, text="شماره تلفن بیمار:").pack(pady=5)
    entry_user_phone = Entry(delete_patient_window)
    entry_user_phone.pack(pady=5)

    Button(delete_patient_window, text="حذف", command=removeDb).pack(pady=10)

    def cancel():
        delete_patient_window.place_forget()

    Button(delete_patient_window, text="انصرالف", command=cancel).pack(pady=10)


def edit_patient():
    def update_user():
        phone_id = entry_phone_id.get()
        name = entry_name.get()
        phone = entry_phone.get()
        if phone_id and name and phone:
            cursor.execute("UPDATE Patients SET name=?, phone=? WHERE phone=?", (name, phone, phone_id))
            conn.commit()
            if cursor.rowcount == 0:
                messagebox.showwarning("خطا", "بیمار با این شماره تلفن یافت نشد!")
            else:
                messagebox.showinfo("موفق", "بیمار با موفقیت ویرایش شد!")
                edit_patient_window.destroy()
        else:
            messagebox.showwarning("خطا", "لطفا همه فیلدها را پر کنید!")

    edit_patient_window = Toplevel(window)
    edit_patient_window.title("ویرایش بیمار")
    edit_patient_window.geometry("300x300")

    Label(edit_patient_window, text="شماره تلفن بیمار").pack(pady=5)
    entry_phone_id = Entry(edit_patient_window)
    entry_phone_id.pack(pady=5)

    Label(edit_patient_window, text="نام جدید:").pack(pady=5)
    entry_name = Entry(edit_patient_window)
    entry_name.pack(pady=5)

    Label(edit_patient_window, text="شماره تماس جدید:").pack(pady=5)
    entry_phone = Entry(edit_patient_window)
    entry_phone.pack(pady=5)

    Button(edit_patient_window, text="ویرایش", command=update_user).pack(pady=10)


def add_medicine():
    def save_medicine():
        name = entry_name.get()
        price = entry_price.get()
        if name and price:
            cursor.execute("INSERT INTO Medicine (name, price) VALUES (?, ?)", (name, float(price)))
            conn.commit()
            messagebox.showinfo("موفق", "دارو با موفقیت اضافه شد!")
            add_medicine_window.destroy()
        else:
            messagebox.showwarning("خطا", "لطفا همه فیلدها را پر کنید!")

    add_medicine_window = Toplevel(window)
    add_medicine_window.title("افزودن دارو")
    add_medicine_window.geometry("300x200")

    Label(add_medicine_window, text="نام دارو:").pack(pady=5)
    entry_name = Entry(add_medicine_window)
    entry_name.pack(pady=5)

    Label(add_medicine_window, text="قیمت:").pack(pady=5)
    entry_price = Entry(add_medicine_window)
    entry_price.pack(pady=5)

    Button(add_medicine_window, text="ذخیره", command=save_medicine).pack(pady=10)


def search_medicine():
    def find_medicine():
        medicine_name = entry_medicine_name.get()
        cursor.execute("SELECT name, price FROM Medicine WHERE name=?", (medicine_name,))
        result = cursor.fetchone()
        if result:
            messagebox.showinfo("اطلاعات دارو", f"نام دارو: {result[0]}\nقیمت:{result[1]}")
        else:
            messagebox.showwarning("خطا", "دارویی با این نام پیدا نشد!")

    search_medicine_window = Toplevel(window)
    search_medicine_window.title("جستجوی دارو")
    search_medicine_window.geometry("300x150")

    Label(search_medicine_window, text="نام دارو:").pack(pady=5)

    entry_medicine_name = Entry(search_medicine_window)
    entry_medicine_name.pack(pady=5)

    Button(search_medicine_window, text="جستجو", command=find_medicine).pack(pady=10)


def delete_medicine():
    def remove_medicine():
        medicine_id = entry_medicine_id.get()
        if medicine_id:
            cursor.execute("DELETE FROM Medicine WHERE name=?", (medicine_id,))
            conn.commit()
            if cursor.rowcount == 0:
                messagebox.showwarning("خطا", "دارویی با این نام وجود ندارد!")
            else:
                messagebox.showinfo("موفق", "دارو با موفقیت حذف شد!")
            delete_medicine_window.destroy()
        else:
            messagebox.showwarning("خطا", "لطفا نام دارو را وارد کنید!")

    delete_medicine_window = Toplevel(window)
    delete_medicine_window.title("حذف دارو")
    delete_medicine_window.geometry("300x150")

    Label(delete_medicine_window, text="نام دارو:").pack(pady=5)
    entry_medicine_id = Entry(delete_medicine_window)
    entry_medicine_id.pack(pady=5)

    Button(delete_medicine_window, text="حذف", command=remove_medicine).pack(pady=10)


def edit_medicine():
    def update_medicine():
        old_medicine_name = entry_medicine_name.get()
        name = entry_name.get()
        price = entry_price.get()
        if old_medicine_name and name and price:
            cursor.execute("UPDATE Medicine SET name=?, price=? WHERE name=?", (name, float(price), old_medicine_name))
            conn.commit()
            messagebox.showinfo("موفق", "دارو با موفقیت ویرایش شد!")
            delete_medicine_window.destroy()
        else:
            messagebox.showwarning("خطا", "لطفا همه فیلدها را پر کنید!")

    delete_medicine_window = Toplevel(window)
    delete_medicine_window.title("ویرایش دارو")
    delete_medicine_window.geometry("300x300")

    Label(delete_medicine_window, text="نام دارو :").pack(pady=5)
    entry_medicine_name = Entry(delete_medicine_window)
    entry_medicine_name.pack(pady=5)

    Label(delete_medicine_window, text="نام جدید:").pack(pady=5)
    entry_name = Entry(delete_medicine_window)
    entry_name.pack(pady=5)

    Label(delete_medicine_window, text="قیمت جدید:").pack(pady=5)
    entry_price = Entry(delete_medicine_window)
    entry_price.pack(pady=5)

    Button(delete_medicine_window, text="ویرایش", command=update_medicine).pack(pady=10)


def add_sale():
    sale_window = Toplevel(window)
    sale_window.title("ثبت فروش دارو")
    sale_window.geometry("630x650")

    cursor.execute("SELECT name, price FROM Medicine")
    menu = cursor.fetchall()
    medicine_prices = {name: price for name, price in menu}

    Label(sale_window, text="انتخاب دارو:").pack(pady=5)
    combo_medicine = ttk.Combobox(sale_window, values=list(medicine_prices.keys()))
    combo_medicine.pack(pady=5)

    Label(sale_window, text="قیمت:").pack(pady=5)
    label_price = Label(sale_window, text="")
    label_price.pack(pady=5)

    def update_price(event):
        medicine_name = combo_medicine.get()
        if medicine_name in medicine_prices:
            label_price.config(text=f"{medicine_prices[medicine_name]}")

    combo_medicine.bind("<<ComboboxSelected>>", update_price)

    def remove_item():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("خطا", "لطفا یک سطر را انتخاب کنید")
            return
        item = selected[0]
        values = tree.item(item, 'values')
        value_cast = (values[0], int(values[1]), float(values[2]))
        tree.delete(item)
        sale_items.remove(value_cast)
        total = sum(item[2] for item in sale_items)
        totallbl.configure(text=total)

    def add_to_list():
        medicine_name = combo_medicine.get()
        quantity = int(entry_quantity.get())
        price = medicine_prices[medicine_name]
        total_price = quantity * price
        sale_items.append((medicine_name, quantity, total_price))
        total = sum(item[2] for item in sale_items)
        totallbl.configure(text=total)
        tree.insert('', END, values=[medicine_name, quantity, total_price])

    def get_medicineID(medicine):
        cursor.execute("SELECT medicineID FROM Medicine WHERE name=?", (medicine,))
        menu1 = cursor.fetchone()
        return menu1[0]

    def submit_sale():
        total = totallbl.cget("text")
        messagebox.showinfo("فروش", f"جمع کل: {total}")

        cursor.execute(
            "INSERT INTO Sales (patientID, total_price) VALUES (?, ?)",
            (patientid, total)
        )

        sale_id = cursor.lastrowid

        for item in sale_items:
            medicineid = get_medicineID(item[0])

            cursor.execute(
                "INSERT INTO Sale_Item (saleID, medicineID, quantity, price) VALUES (?,?,?,?)",
                (sale_id, medicineid, item[1], item[2])
                )
            conn.commit()
            sale_window.destroy()

    Label(sale_window, text="تعداد:").pack(pady=5)
    entry_quantity = Entry(sale_window)
    entry_quantity.pack(pady=5)

    Button(sale_window, text="افزودن به لیست فروش", command=add_to_list).pack(pady=10)

    f = Frame(sale_window, width=450)
    f.pack(fill=BOTH, expand=1)
    f.grid_rowconfigure(0, weight=3)
    f.grid_rowconfigure(1, weight=1)

    columns = ('medicine', 'quantity', 'fee')
    tree = ttk.Treeview(f, columns=columns, show='headings')
    tree.heading('medicine', text="نام دارو")
    tree.heading('quantity', text="تعداد")
    tree.heading('fee', text="قیمت")
    tree.grid(pady=5, padx=10)

    f10 = Frame(f, width=450)
    f10.grid(row=1, column=0, padx=10)

    # f10 = Frame(sale_window)
    # f10.pack(pady=10)

    rb = Button(f10, text="حذف", width=20, bg="red", command=remove_item)
    rb.grid(row=0, column=0, padx=10, sticky='snwe')
    Button(f10, text="ثبت فروش", width=20, bg="#4CAF50", command=submit_sale).grid(row=0, column=1, padx=10)

    sale_items = []
    totallbl = Label(f10, text="-----------", background="light Blue", width=20)
    totallbl.grid(row=0, column=2, sticky='snwe', padx=10)

def show_medicines():
    medicine_window = Toplevel(window)
    medicine_window.title("لیست داروها")
    medicine_window.geometry("500x400")

    columns = ("name", "price")

    tree = ttk.Treeview(medicine_window, columns=columns, show="headings")

    tree.heading("name", text="نام دارو")
    tree.heading("price", text="قیمت")

    tree.column("name", width=250)
    tree.column("price", width=150)

    tree.pack(fill=BOTH, expand=True)

    cursor.execute("SELECT name, price FROM Medicine")

    medicines = cursor.fetchall()

    for medicine in medicines:
        tree.insert("", END, values=medicine)

def show_patients():
    patient_window = Toplevel(window)
    patient_window.title("لیست بیماران")
    patient_window.geometry("500x400")

    columns = ("name", "phone")

    tree = ttk.Treeview(patient_window, columns=columns, show="headings")

    tree.heading("name", text="نام بیمار")
    tree.heading("phone", text="شماره تماس")

    tree.column("name", width=220)
    tree.column("phone", width=220)

    tree.pack(fill=BOTH, expand=True)

    cursor.execute("SELECT name, phone FROM Patients")

    patients = cursor.fetchall()

    for patient in patients:
        tree.insert("", END, values=patient)

def count_medicines():
    cursor.execute("SELECT COUNT(*) FROM Medicine")
    total = cursor.fetchone()[0]

    messagebox.showinfo(
        "تعداد داروها",
        f"تعداد کل داروهای ثبت شده:\n{total}"
    )

def total_sales():
    cursor.execute("SELECT SUM(total_price) FROM Sales")
    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    messagebox.showinfo(
        "مجموع فروش",
        f"مجموع فروش داروها:\n{total} تومان"
    )

def about_program():
    messagebox.showinfo(
        "درباره برنامه",
        "سیستم مدیریت داروخانه\n\n"
        "نام پروژه: مدیریت داروخانه\n"
        "زبان برنامه نویسی: Python\n"
        "پایگاه داده: SQLite\n\n"
        "تهیه کننده:\n"
        "راضیه امیدی"
    )

def search_patient():
    def find_patient():
        patient_name = entry_patient_name.get()

        cursor.execute("SELECT name, phone FROM Patients WHERE name=?", (patient_name,))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo(
                "اطلاعات بیمار",
                f"نام بیمار: {result[0]}\nشماره تماس: {result[1]}"
            )
        else:
            messagebox.showwarning("خطا", "بیماری با این نام پیدا نشد!")

    search_patient_window = Toplevel(window)
    search_patient_window.title("جستجوی بیمار")
    search_patient_window.geometry("300x150")

    Label(search_patient_window, text="نام بیمار:").pack(pady=5)

    entry_patient_name = Entry(search_patient_window)
    entry_patient_name.pack(pady=5)

    Button(search_patient_window, text="جستجو", command=find_patient).pack(pady=10)

def search_price():
    def find_price():
        price = entry_price.get()

        if price:
            cursor.execute("SELECT name, price FROM Medicine WHERE price=?", (float(price),))
            result = cursor.fetchall()

            if result:
                text = ""
                for medicine in result:
                    text += f"{medicine[0]}     {medicine[1]}\n"

                messagebox.showinfo("نتیجه جستجو", text)
            else:
                messagebox.showwarning("خطا", "دارویی با این قیمت پیدا نشد!")

    search_price_window = Toplevel(window)
    search_price_window.title("جستجو بر اساس قیمت")
    search_price_window.geometry("300x180")

    Label(search_price_window, text="قیمت دارو:").pack(pady=5)

    entry_price = Entry(search_price_window)
    entry_price.pack(pady=5)

    Button(search_price_window, text="جستجو", command=find_price).pack(pady=10)


def count_patients():
    cursor.execute("SELECT COUNT(*) FROM Patients")
    total = cursor.fetchone()[0]

    messagebox.showinfo(
        "تعداد بیماران",
        f"تعداد کل بیماران ثبت شده:\n{total}"
    )

def count_sales():
    cursor.execute("SELECT COUNT(*) FROM Sales")
    total = cursor.fetchone()[0]

    messagebox.showinfo(
        "تعداد فروش",
        f"تعداد کل فروش‌های ثبت شده:\n{total}"
    )

def delete_all_sales():
    answer = messagebox.askyesno(
        "حذف فروش‌ها",
        "آیا از حذف تمام فروش‌ها مطمئن هستید؟"
    )

    if answer:
        cursor.execute("DELETE FROM Sale_Item")
        cursor.execute("DELETE FROM Sales")
        conn.commit()

        messagebox.showinfo(
            "موفق",
            "تمام فروش‌ها حذف شدند."
        )

bg_image = PhotoImage(file="pharmacy.png")
bg_label = Label(window, image=bg_image, width=400, height=600)
bg_label.pack(fill=BOTH, expand=True, side=TOP)

menubar = Menu(window)
window.configure(menu=menubar)
user_menu = Menu(menubar, tearoff=0)
user_menu.add_command(label="ورود بیمار", command=patient_login)
user_menu.add_command(label="ثبت بیمار جدید", command=create_patient)
user_menu.add_command(label="نمایش لیست بیماران", command=show_patients)
user_menu.add_command(label="تعداد کل بیماران", command=count_patients)
user_menu.add_command(label="جستجوی بیمار", command=search_patient)
user_menu.add_command(label="ویرایش بیمار", command=edit_patient)
user_menu.add_command(label="حذف بیمار", command=delete_patient)
menubar.add_cascade(label="بیماران", menu=user_menu)

medicine_menu = Menu(menubar, tearoff=0)
medicine_menu.add_command(label="ثبت دارو جدید", command=add_medicine)
medicine_menu.add_command(label="جستجوی دارو", command=search_medicine)
medicine_menu.add_command(label="جستجو بر اساس قیمت", command=search_price)
medicine_menu.add_command(label="ویرایش دارو", command=edit_medicine)
medicine_menu.add_command(label="حذف دارو", command=delete_medicine)
medicine_menu.add_command(label="نمایش لیست داروها", command=show_medicines)
medicine_menu.add_command(label="تعداد کل داروها", command=count_medicines)
menubar.add_cascade(label="دارو", menu=medicine_menu)

sale_menu = Menu(menubar, tearoff=0)
sale_menu.add_command(label="ثبت فروش", command=add_sale)
menubar.add_cascade(label="فروش دارو", menu=sale_menu)

report_menu = Menu(menubar, tearoff=0)
report_menu.add_command(label="مجموع فروش", command=total_sales)
report_menu.add_command(label="تعداد کل فروش‌ها", command=count_sales)
report_menu.add_command(label="حذف تمام فروش‌ها", command=delete_all_sales)
menubar.add_cascade(label="گزارش", menu=report_menu)

help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="درباره برنامه", command=about_program)
menubar.add_cascade(label="راهنما", menu=help_menu)

window.mainloop()
