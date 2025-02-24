import json
import re
import csv
import xml.etree.ElementTree as ET
import datetime
import logging

# Cấu hình logging
logging.basicConfig(filename="student_management.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

DATA_JSON = "students.json"
DATA_CSV = "students.csv"
DATA_XML = "students.xml"
VERSION = "2.0"
BUILD_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
VALID_KHOA = ["Khoa Luật", "Khoa Tiếng Anh thương mại", "Khoa Tiếng Nhật", "Khoa Tiếng Pháp"]
VALID_TINH_TRANG = ["Đang học", "Bảo lưu", "Tốt nghiệp", "Đình chỉ"]

CONFIG_RULES_ENABLED = True
DELETE_TIME_LIMIT = 30  # Phút
EMAIL_DOMAIN = "@student.university.edu.vn"
PHONE_PATTERN = re.compile(r"^(\+84|0[3|5|7|8|9])[0-9]{8}$")
VALID_STATUS_TRANSITIONS = {
    "Đang học": ["Bảo lưu", "Tốt nghiệp", "Đình chỉ"],
    "Bảo lưu": ["Đang học", "Đình chỉ"],
    "Đình chỉ": [],
    "Tốt nghiệp": []
}

class StudentManage:
    def __init__(self):
        self.students = self.load_data()

    def add_faculty(self, faculty_name):
        if faculty_name not in self.VALID_KHOA:
            self.VALID_KHOA.append(faculty_name)
            return f"Khoa '{faculty_name}' đã được thêm thành công."
        return f"Khoa '{faculty_name}' đã tồn tại."

    def rename_faculty(self, old_name, new_name):
        # nếu có sinh viên trong khoa này -> không xoá được
        if student := next((s for s in self.students if s["khoa"] == old_name), None):
            return f"Không thể đổi tên khoa '{old_name}' thành '{new_name}' vì có sinh viên '{student['ho_ten']}' thuộc khoa này."
        if old_name in self.VALID_KHOA:
            self.VALID_KHOA[self.VALID_KHOA.index(old_name)] = new_name
            return f"Khoa '{old_name}' đã được đổi thành '{new_name}'."
        return f"Khoa '{old_name}' không tồn tại."
    
    def delete_falcuty(self, faculty_name):
        if student := next((s for s in self.students if s["khoa"] == faculty_name), None):
            return f"Không thể xóa khoa '{faculty_name}' vì có sinh viên '{student['ho_ten']}' thuộc khoa này."
        if faculty_name in self.VALID_KHOA:
            self.VALID_KHOA.remove(faculty_name)
            return f"Khoa '{faculty_name}' đã được xóa."
        return f"Khoa '{faculty_name}' không tồn tại."

    def add_student_status(self, status_name):
        if status_name not in self.VALID_TINH_TRANG:
            self.VALID_TINH_TRANG.append(status_name)
            return f"Tình trạng sinh viên '{status_name}' đã được thêm thành công."
        return f"Tình trạng sinh viên '{status_name}' đã tồn tại."

    def rename_student_status(self, old_name, new_name):
        if student := next((s for s in self.students if s["tinh_trang"] == old_name), None):
            return f"Không thể đổi tên tình trạng sinh viên '{old_name}' thành '{new_name}' vì có sinh viên '{student['ho_ten']}' đang ở tình trạng này."
        if old_name in self.VALID_TINH_TRANG:
            self.VALID_TINH_TRANG[self.VALID_TINH_TRANG.index(old_name)] = new_name
            return f"Tình trạng sinh viên '{old_name}' đã được đổi thành '{new_name}'."
        return f"Tình trạng sinh viên '{old_name}' không tồn tại."
    
    def delete_student_status(self, status_name):
        if student := next((s for s in self.students if s["tinh_trang"] == status_name), None):
            return f"Không thể xóa tình trạng sinh viên '{status_name}' vì có sinh viên '{student['ho_ten']}' đang ở tình trạng này."
        if status_name in self.VALID_TINH_TRANG:
            self.VALID_TINH_TRANG.remove(status_name)
            return f"Tình trạng sinh viên '{status_name}' đã được xóa."
        return f"Tình trạng sinh viên '{status_name}' không tồn tại."

    def load_data(self):
        try:
            with open(self.DATA_JSON, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def export_csv(self):
        with open(self.DATA_CSV, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.students[0].keys())
            writer.writeheader()
            writer.writerows(self.students)
        print("Xuất dữ liệu CSV thành công!")
        logging.info("Dữ liệu được xuất sang CSV")

    def import_csv(self):
        try:
            with open(self.DATA_CSV, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.students = list(reader)
                self.save_data()
                print("Nhập dữ liệu từ CSV thành công!")
                logging.info("Dữ liệu được nhập từ CSV")
        except FileNotFoundError:
            print("Không tìm thấy file CSV!")

    def save_data(self):
        with open(self.DATA_JSON, "w", encoding="utf-8") as file:
            json.dump(self.students, file, indent=4, ensure_ascii=False)

    def is_valid_email(self, email):
        return email.endswith(EMAIL_DOMAIN)

    def is_valid_phone(self, phone):
        return PHONE_PATTERN.match(phone)

    def is_valid_gender(self, choice):
        return choice in ["1", "2"]

    def is_valid_khoa(self, khoa):
        return khoa in self.VALID_KHOA

    def is_valid_tinh_trang(self, tinh_trang):
        return tinh_trang in self.VALID_TINH_TRANG

    def add_student(self):
        mssv = input("Nhập MSSV: ")
        if CONFIG_RULES_ENABLED:
            while any(s["mssv"] == mssv for s in self.students):
                print("MSSV đã tồn tại!")
                mssv = input("Nhập MSSV: ")

        ho_ten = input("Nhập họ tên: ")
        ngay_sinh = input("Nhập ngày sinh (YYYY-MM-DD): ")

        gioi_tinh = input("Nhập giới tính (1: Nữ, 2: Nam): ")
        if CONFIG_RULES_ENABLED:
            while not self.is_valid_gender(gioi_tinh):
                print("Giới tính không hợp lệ! Vui lòng nhập 1 (Nữ) hoặc 2 (Nam).")
                gioi_tinh = input("Nhập giới tính (1: Nữ, 2: Nam): ")
        gioi_tinh = "Nữ" if gioi_tinh == "1" else "Nam"

        khoa = input("Nhập khoa: ")
        if CONFIG_RULES_ENABLED:
            while not self.is_valid_khoa(khoa):
                print("Khoa không hợp lệ! Danh sách khoa hợp lệ: ", self.VALID_KHOA)
                khoa = input("Nhập khoa: ")

        khoa_hoc = input("Nhập khóa: ")
        chuong_trinh = input("Nhập chương trình: ")
        dia_chi = input("Nhập địa chỉ: ")
        email = input("Nhập email: ")
        if CONFIG_RULES_ENABLED:
            while not self.is_valid_email(email):
                print("Email không hợp lệ!")
                email = input("Nhập email: ")

        so_dien_thoai = input("Nhập số điện thoại: ")
        if CONFIG_RULES_ENABLED:
            while not self.is_valid_phone(so_dien_thoai):
                print("Số điện thoại không hợp lệ!")
                so_dien_thoai = input("Nhập số điện thoại: ")

        tinh_trang = input("Nhập tình trạng sinh viên: ")
        if CONFIG_RULES_ENABLED:
            while not self.is_valid_tinh_trang(tinh_trang):
                print("Tình trạng sinh viên không hợp lệ! Danh sách hợp lệ: ", self.VALID_TINH_TRANG)
                tinh_trang = input("Nhập tình trạng sinh viên: ")

        self.students.append({
            "created_at": datetime.datetime.now().isoformat(),
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
        self.save_data()
        print("Thêm sinh viên thành công!")

    def delete_student(self):
        current_time = datetime.datetime.now()
        mssv = input("Nhập MSSV của sinh viên cần xóa: ")
        for student in self.students:
            if student["mssv"] == mssv:
                created_at = datetime.datetime.fromisoformat(student["created_at"])
                time_diff = (current_time - created_at).total_seconds() / 60
                if time_diff > DELETE_TIME_LIMIT:
                    print("Không thể xóa sinh viên sau 30 phút kể từ khi tạo!")
                    return
                self.students.remove(student)
                self.save_data()
                print("Xóa sinh viên thành công!")
                return
        print("Không tìm thấy sinh viên!")
    
    def update_student(self):
        mssv = input("Nhập MSSV của sinh viên cần cập nhật: ")
        for student in self.students:
            if student["mssv"] == mssv:
                column = input("Nhập tên trường cần cập nhật (VD: ho_ten, email, khoa, ...): ")
                new_value = input(f"Nhập giá trị mới cho {column}: ")

                if column == "email" and not self.is_valid_email(new_value):
                    print("Email không hợp lệ!")
                    return
                if column == "so_dien_thoai" and not self.is_valid_phone(new_value):
                    print("Số điện thoại không hợp lệ!")
                    return
                if column == "khoa" and not self.is_valid_khoa(new_value):
                    print("Khoa không hợp lệ!")
                    return
                if column == "tinh_trang" and not self.is_valid_tinh_trang(new_value):
                    if new_value not in VALID_STATUS_TRANSITIONS[student["tinh_trang"]]:
                        print(f"Không thể chuyển từ {student['tinh_trang']} sang {new_value}!")
                        return

                student[column] = new_value
                self.save_data()
                print("Cập nhật thành công!")
                return
        print("Không tìm thấy sinh viên!")

    def search_student(self):
        search_term = input("Nhập MSSV hoặc họ tên sinh viên cần tìm: ")
        results = [s for s in self.students if s["mssv"] == search_term or search_term.lower() in s["ho_ten"].lower()]

        if results:
            for student in results:
                print(student)
        else:
            print("Không tìm thấy sinh viên!")

    def export_xml(self):
        root = ET.Element("students")
        for student in self.students:
            student_elem = ET.SubElement(root, "student")
            for key, value in student.items():
                child = ET.SubElement(student_elem, key)
                child.text = value
        tree = ET.ElementTree(root)
        tree.write(self.DATA_XML, encoding="utf-8", xml_declaration=True)
        print("Xuất dữ liệu XML thành công!")
        logging.info("Dữ liệu được xuất sang XML")

    def show_version(self):
        print(f"Student Management System v{self.VERSION} - Build date: {self.BUILD_DATE}")
        logging.info(f"Phiên bản: {self.VERSION}, Ngày build: {self.BUILD_DATE}")

    def search_by_faculty(self):
        khoa = input("Nhập tên khoa cần tìm: ")
        results = [s for s in self.students if s["khoa"].lower() == khoa.lower()]
        if results:
            for student in results:
                print(student)
        else:
            print("Không tìm thấy sinh viên thuộc khoa này!")

    def search_by_faculty_and_name(self):
        khoa = input("Nhập tên khoa cần tìm: ")
        ho_ten = input("Nhập họ tên sinh viên cần tìm: ")
        results = [s for s in self.students if s["khoa"].lower() == khoa.lower() and ho_ten.lower() in s["ho_ten"].lower()]
        if results:
            for student in results:
                print(student)
        else:
            print("Không tìm thấy sinh viên thuộc khoa này!")

    def main(self):
        while True:
            print("\n--- QUẢN LÝ SINH VIÊN ---")
            print("**TRƯỜNG ĐẠI HỌC [Tên Trường]**")
            print("**PHÒNG CÔNG TÁC SINH VIÊN**")
            print("📍 Địa chỉ: [Địa chỉ trường]")
            print("📞 Điện thoại: [Số điện thoại] | 📧 Email: [Email liên hệ]")
            print("---------------------------")
            
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
            print("11. Thêm khoa mới")
            print("12. Đổi tên khoa")
            print("13. Thêm tình trạng sinh viên mới")
            print("14. Đổi tên tình trạng sinh viên")
            print("15. Thoát chương trình")
            print("---------------------------")

            choice = input("Chọn chức năng: ")

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.delete_student()
            elif choice == "3":
                self.update_student()
            elif choice == "4":
                self.search_student()
            elif choice == "5":
                self.export_csv()
            elif choice == "6":
                self.import_csv()
            elif choice == "7":
                self.export_xml()
            elif choice == "8":
                self.show_version()
            elif choice == "9":
                self.search_by_faculty()
            elif choice == "10":
                self.search_by_faculty_and_name()
            elif choice == "11":
                khoa_name = input("Nhập tên khoa cần thêm: ")
                print(self.add_faculty(khoa_name))
            elif choice == "12":
                old_name = input("Nhập tên khoa cần đổi: ")
                new_name = input("Nhập tên mới: ")
                print(self.rename_faculty(old_name, new_name))
            elif choice == "13":
                status_name = input("Nhập tên tình trạng sinh viên cần thêm: ")
                print(self.add_student_status(status_name))
            elif choice == "14":
                old_name = input("Nhập tên tình trạng sinh viên cần đổi: ")
                new_name = input("Nhập tên mới: ")
                print(self.rename_student_status(old_name, new_name))
            elif choice == "15":
                print("Thoát chương trình!")
                break
            else:
                print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    sm = StudentManage()
    sm.main()
