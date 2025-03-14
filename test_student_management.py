import unittest
from unittest.mock import patch, mock_open
import datetime
from student_management import StudentManage

class TestStudentManage(unittest.TestCase):

    def setUp(self):
        """Khởi tạo đối tượng quản lý sinh viên cho mỗi test case"""
        self.sm = StudentManage()
        self.sm.students = [
            {
                "created_at": datetime.datetime.now().isoformat(),
                "mssv": "22127410",
                "ho_ten": "Thuý",
                "ngay_sinh": "2004-16-01",
                "gioi_tinh": "Nữ",
                "khoa": "Khoa Luật",
                "khoa_hoc": "2022",
                "chuong_trinh": "CNTT",
                "dia_chi": "Nghệ An",
                "email": "thuythanhluu161@student.university.edu.vn",
                "so_dien_thoai": "0988777665",
                "tinh_trang": "Đã tốt nghiệp"
            }
        ]

    def test_add_faculty(self):
        """Kiểm tra thêm khoa mới"""
        result = self.sm.add_faculty("Khoa Công nghệ thông tin")
        self.assertIn("đã được thêm thành công", result)

        result_existing = self.sm.add_faculty("Khoa Luật")
        self.assertIn("đã tồn tại", result_existing)

    def test_rename_faculty(self):
        """Kiểm tra đổi tên khoa"""
        result = self.sm.rename_faculty("Khoa Luật", "Khoa Pháp Luật")
        self.assertIn("đã được đổi thành", result)

        result_not_exist = self.sm.rename_faculty("Khoa Không Tồn Tại", "Khoa Mới")
        self.assertIn("không tồn tại", result_not_exist)

    def test_delete_faculty(self):
        """Kiểm tra xóa khoa (không có sinh viên trong khoa)"""
        result = self.sm.delete_falcuty("Khoa Tiếng Nhật")
        self.assertIn("đã được xóa", result)

        result_with_students = self.sm.delete_falcuty("Khoa Luật")
        self.assertIn("Không thể xóa", result_with_students)

    def test_add_student_status(self):
        """Kiểm tra thêm tình trạng sinh viên"""
        result = self.sm.add_student_status("Đang thực tập")
        self.assertIn("đã được thêm thành công", result)

    def test_rename_student_status(self):
        """Kiểm tra đổi tên tình trạng sinh viên"""
        result = self.sm.rename_student_status("Đang học", "Đang trong kỳ học")
        self.assertIn("đã được đổi thành", result)

    def test_delete_student_status(self):
        """Kiểm tra xóa tình trạng sinh viên"""
        result = self.sm.delete_student_status("Bảo lưu")
        self.assertIn("đã được xóa", result)

        result_with_students = self.sm.delete_student_status("Đang học")
        self.assertIn("Không thể xóa", result_with_students)

    def test_is_valid_email(self):
        """Kiểm tra email hợp lệ"""
        self.assertTrue(self.sm.is_valid_email("test@student.university.edu.vn"))
        self.assertFalse(self.sm.is_valid_email("test@gmail.com"))

    def test_is_valid_phone(self):
        """Kiểm tra số điện thoại hợp lệ"""
        self.assertTrue(self.sm.is_valid_phone("0912345678"))
        self.assertTrue(self.sm.is_valid_phone("+84912345678"))
        self.assertFalse(self.sm.is_valid_phone("1234567890"))
        self.assertFalse(self.sm.is_valid_phone("0123456789"))

    def test_add_student(self):
        """Kiểm tra thêm sinh viên (giả lập nhập dữ liệu)"""
        with patch("builtins.input", side_effect=[
            "22129999", "Nguyễn Văn A", "2000-01-01", "1", "Khoa Luật",
            "K23", "Cử nhân", "TP.HCM", "22129999@student.university.edu.vn", "0911222333", "Đang học"
        ]):
            self.sm.add_student()
            self.assertEqual(len(self.sm.students), 2)
            self.assertEqual(self.sm.students[1]["mssv"], "22129999")

    def test_export_html(self):
        """Kiểm tra xuất giấy xác nhận HTML"""
        confirmation_data = {
            "ho_ten": "Thuý",
            "mssv": "22127410",
            "ngay_sinh": "2004-16-01",
            "gioi_tinh": "Nữ",
            "khoa": "Khoa Luật",
            "chuong_trinh": "CNTT",
            "khoa_hoc": "2022",
            "tinh_trang": "Đã tốt nghiệp",
            "ngay_cap": datetime.datetime.now().strftime("%d/%m/%Y")
        }

        with patch("builtins.open", mock_open()) as mocked_file:
            self.sm.export_to_html(confirmation_data)
            mocked_file.assert_called_with("confirmation.html", "w", encoding="utf-8")

    def test_export_md(self):
        """Kiểm tra xuất giấy xác nhận Markdown"""
        confirmation_data = {
            "ho_ten": "Thuý",
            "mssv": "22127410",
            "ngay_sinh": "2004-16-01",
            "gioi_tinh": "Nữ",
            "khoa": "Khoa Luật",
            "chuong_trinh": "CNTT",
            "khoa_hoc": "2022",
            "tinh_trang": "Đã tốt nghiệp",
            "ngay_cap": datetime.datetime.now().strftime("%d/%m/%Y")
        }

        with patch("builtins.open", mock_open()) as mocked_file:
            self.sm.export_to_md(confirmation_data)
            mocked_file.assert_called_with("confirmation.md", "w", encoding="utf-8")

if __name__ == "__main__":
    unittest.main()