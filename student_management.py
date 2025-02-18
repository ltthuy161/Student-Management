import json
import re
import json
import csv
import xml.etree.ElementTree as ET
import datetime
import logging

# Cấu hình logging
logging.basicConfig(filename="student_management.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Định nghĩa đường dẫn file dữ liệu
DATA_JSON = "students.json"
DATA_CSV = "students.csv"
DATA_XML = "students.xml"
VERSION = "2.0"
BUILD_DATE = datetime.datetime.now().strftime("%Y-%m-%d")

# Danh sách khoa hợp lệ
VALID_KHOA = ["Khoa Luật", "Khoa Tiếng Anh thương mại", "Khoa Tiếng Nhật", "Khoa Tiếng Pháp"]

# Danh sách tình trạng sinh viên hợp lệ
VALID_TINH_TRANG = ["Đang học", "Đã tốt nghiệp", "Đã thôi học", "Tạm dừng học"]

# Hàm tải dữ liệu từ file JSON
def load_data():
    try:
        with open(DATA_JSON, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Xuất dữ liệu sang CSV
def export_csv():
    students = load_data()
    with open(DATA_CSV, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=students[0].keys())
        writer.writeheader()
        writer.writerows(students)
    print("Xuất dữ liệu CSV thành công!")
    logging.info("Dữ liệu được xuất sang CSV")

# Nhập dữ liệu từ CSV
def import_csv():
    try:
        with open(DATA_CSV, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = list(reader)
            save_data(data)
            print("Nhập dữ liệu từ CSV thành công!")
            logging.info("Dữ liệu được nhập từ CSV")
    except FileNotFoundError:
        print("Không tìm thấy file CSV!")

# Hàm lưu dữ liệu vào file JSON
def save_data(data):
    with open(DATA_JSON, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Hàm kiểm tra định dạng email
def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

# Hàm kiểm tra số điện thoại
def is_valid_phone(phone):
    return re.match(r"^\d{10,11}$", phone)

# Hàm kiểm tra giới tính
def is_valid_gender(choice):
    return choice in ["1", "2"]

# Hàm kiểm tra khoa
def is_valid_khoa(khoa):
    return khoa in VALID_KHOA

# Hàm kiểm tra tình trạng sinh viên
def is_valid_tinh_trang(tinh_trang):
    return tinh_trang in VALID_TINH_TRANG

# Thêm sinh viên vào danh sách
def add_student():
    students = load_data()
    mssv = input("Nhập MSSV: ")
    ho_ten = input("Nhập họ tên: ")
    ngay_sinh = input("Nhập ngày sinh (YYYY-MM-DD): ")
    
    gioi_tinh = input("Nhập giới tính (1: Nữ, 2: Nam): ")
    while not is_valid_gender(gioi_tinh):
        print("Giới tính không hợp lệ! Vui lòng nhập 1 (Nữ) hoặc 2 (Nam).")
        gioi_tinh = input("Nhập giới tính (1: Nữ, 2: Nam): ")
    gioi_tinh = "Nữ" if gioi_tinh == "1" else "Nam"
    
    khoa = input("Nhập khoa: ")
    while not is_valid_khoa(khoa):
        print("Khoa không hợp lệ! Danh sách khoa hợp lệ: ", VALID_KHOA)
        khoa = input("Nhập khoa: ")
    
    khoa_hoc = input("Nhập khóa: ")
    chuong_trinh = input("Nhập chương trình: ")
    dia_chi = input("Nhập địa chỉ: ")
    email = input("Nhập email: ")
    while not is_valid_email(email):
        print("Email không hợp lệ!")
        email = input("Nhập email: ")
    
    so_dien_thoai = input("Nhập số điện thoại: ")
    while not is_valid_phone(so_dien_thoai):
        print("Số điện thoại không hợp lệ!")
        so_dien_thoai = input("Nhập số điện thoại: ")
    
    tinh_trang = input("Nhập tình trạng sinh viên: ")
    while not is_valid_tinh_trang(tinh_trang):
        print("Tình trạng sinh viên không hợp lệ! Danh sách hợp lệ: ", VALID_TINH_TRANG)
        tinh_trang = input("Nhập tình trạng sinh viên: ")
    
    students.append({
        "mssv": mssv,
        "ho_ten": ho_ten,
        "ngay_sinh": ngay_sinh,
        "gioi_tinh": gioi_tinh,
        "khoa": khoa,
        "khoa_hoc": khoa_hoc,
        "chuong_trinh": chuong_trinh,
        "dia_chi": dia_chi,
        "email": email,
        "so_dien_thoai": so_dien_thoai,
        "tinh_trang": tinh_trang
    })
    save_data(students)
    print("Thêm sinh viên thành công!")

# Xóa sinh viên
def delete_student():
    students = load_data()
    mssv = input("Nhập MSSV của sinh viên cần xóa: ")
    students = [s for s in students if s["mssv"] != mssv]
    save_data(students)
    print("Xóa sinh viên thành công!")

# Cập nhật thông tin sinh viên
def update_student():
    students = load_data()
    mssv = input("Nhập MSSV của sinh viên cần cập nhật: ")
    for student in students:
        if student["mssv"] == mssv:
            column = input("Nhập tên trường cần cập nhật (VD: ho_ten, email, khoa, ...): ")
            new_value = input(f"Nhập giá trị mới cho {column}: ")
            
            if column == "email" and not is_valid_email(new_value):
                print("Email không hợp lệ!")
                return
            if column == "so_dien_thoai" and not is_valid_phone(new_value):
                print("Số điện thoại không hợp lệ!")
                return
            if column == "khoa" and not is_valid_khoa(new_value):
                print("Khoa không hợp lệ!")
                return
            if column == "tinh_trang" and not is_valid_tinh_trang(new_value):
                print("Tình trạng sinh viên không hợp lệ!")
                return
            
            student[column] = new_value
            save_data(students)
            print("Cập nhật thành công!")
            return
    print("Không tìm thấy sinh viên!")

# Tìm kiếm sinh viên
def search_student():
    students = load_data()
    search_term = input("Nhập MSSV hoặc họ tên sinh viên cần tìm: ")
    results = [s for s in students if s["mssv"] == search_term or search_term.lower() in s["ho_ten"].lower()]
    
    if results:
        for student in results:
            print(student)
    else:
        print("Không tìm thấy sinh viên!")

# Xuất dữ liệu sang XML
def export_xml():
    students = load_data()
    root = ET.Element("students")
    for student in students:
        student_elem = ET.SubElement(root, "student")
        for key, value in student.items():
            child = ET.SubElement(student_elem, key)
            child.text = value
    tree = ET.ElementTree(root)
    tree.write(DATA_XML, encoding="utf-8", xml_declaration=True)
    print("Xuất dữ liệu XML thành công!")
    logging.info("Dữ liệu được xuất sang XML")

# Thêm chức năng hiển thị phiên bản ứng dụng
def show_version():
    print(f"Student Management System v{VERSION} - Build date: {BUILD_DATE}")
    logging.info(f"Phiên bản: {VERSION}, Ngày build: {BUILD_DATE}")


# Tìm kiếm sinh viên theo khoa
def search_by_faculty():
    students = load_data()
    khoa = input("Nhập tên khoa cần tìm: ")
    results = [s for s in students if s["khoa"].lower() == khoa.lower()]
    if results:
        for student in results:
            print(student)
    else:
        print("Không tìm thấy sinh viên thuộc khoa này!")

# Tìm theo khoa + tên sinh viên
def search_by_faculty_and_name():
    students = load_data()
    khoa = input("Nhập tên khoa cần tìm: ")
    ho_ten = input("Nhập họ tên sinh viên cần tìm: ")
    results = [s for s in students if s["khoa"].lower() == khoa.lower() and ho_ten.lower() in s["ho_ten"].lower()]
    if results:
        for student in results:
            print(student)
    else:
        print("Không tìm thấy sinh viên thuộc khoa này!")


# Menu điều khiển
def main():
    while True:
        print("\n--- QUẢN LÝ SINH VIÊN ---")
        print("1. Thêm sinh viên")
        print("2. Xóa sinh viên")
        print("3. Cập nhật thông tin sinh viên")
        print("4. Tìm kiếm sinh viên")
        print("5. Xuất dữ liệu CSV")
        print("6. Nhập dữ liệu từ CSV")
        print("7. Xuất dữ liệu XML")
        print("8. Hiển thị phiên bản ứng dụng")
        print("9. Tìm kiếm sinh viên theo khoa")
        print("10. Tìm kiếm sinh viên theo khoa và tên")
        print("11. Thoát chương trình")

        choice = input("Chọn chức năng: ")
        
        if choice == "1":
            add_student()
        elif choice == "2":
            delete_student()
        elif choice == "3":
            update_student()
        elif choice == "4":
            search_student()
        elif choice == "5":
            export_csv()
        elif choice == "6":
            import_csv()
        elif choice == "7":
            export_xml()
        elif choice == "8":
            show_version()
        elif choice == "9":
            search_by_faculty()
        elif choice == "10":
            search_by_faculty_and_name()
        elif choice == "11":
            print("Thoát chương trình!")
            break
        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()