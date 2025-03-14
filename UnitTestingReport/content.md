# Code Coverage
Trong unit test, \verb|code coverage| là một giá trị thể hiện độ bao phủ của \verb|code| bởi các \verb|test case| được biểu thị dưới dạng %, nó cho ta thấy được tỉ lệ \verb|code| đã được thực thi bằng \verb|unit test| trên tổng số \verb|code| của một chương trình. \verb|Code coverage| được tính bằng công thức sau:

$$
\text{code coverage} = \frac{\text{items executed}}{\text{total number of code}}
$$

## Line Coverage

### Định nghĩa

\verb|Line coverage| thể hiện số câu lệnh của chưong trình đã được thực thi trong quá trình test, chúng ta có thể hiểu nôm na \verb|line coverage| ở đây chính là độ bao phủ các dòng lệnh, tức là số dòng lệnh đã được chạy qua khi test. Một dòng lệnh được tính là đã được thực thi khi chỉ một hoặc toàn bộ \verb|code| của dòng lệnh đó được thực thi, vì thế khi độ bao phủ câu lệnh không đảm bảo rằng chương trình của bạn 100% không có lỗi. 

Nói cách khác, \verb|line coverage| kiểm tra để xác định tất cả các dòng code trong thiết kế đã được thực thi trong quá trình mô phỏng hay chưa.

### Ví dụ

\pagebreak

\begin{lstlisting}[language=Python]
def foo(decision)
   a = 0
   if decision
      a = 1
   end
   a = 1 / a
   return a
end
\end{lstlisting}

Ở ví dụ trên dễ dàng đặt được 100% \verb|line coverage| bằng cách test với input \verb|foo(1)|, khi đó câu lệnh trong điều kiện \verb|if| sẽ được thực thi, tuy nhiên nếu input là giá trị 0 thì ở dòng lệnh \verb|return| sẽ xảy ra lỗi \verb|division by zero|

## Branch Coverage

### Định nghĩa

\verb|Branch Coverage Testing| là một kỹ thuật kiểm thử phần mềm tập trung vào việc kiểm tra tất cả các nhánh của cấu trúc điều kiện (\verb|if, else, switch-case|) trong mã nguồn. Mục tiêu của kỹ thuật này là đảm bảo rằng tất cả các điều kiện và nhánh trong mã đều được kiểm thử để phát hiện lỗi và cải thiện độ tin cậy của phần mềm.

\verb|Branch Coverage| được tính bằng công thức:

$$
\text{Branch Coverage} = \left( \frac{\text{Số nhánh được kiểm tra}}{\text{Tổng số nhánh}} \right) \times 100\%
$$

### Ví dụ

\begin{lstlisting}[language=Python]
def check_number(num):
    if num > 0:
        print("Positive")
    elif num < 0:
        print("Negative")
    else:
        print("Zero")
\end{lstlisting}

- Xác định các nhánh trong đoạn mã

   - Nhánh 1: \verb|if (num > 0)| → Điều kiện đúng, in "Positive Number".
	- Nhánh 2: \verb|else if (num < 0)| → Điều kiện đúng, in "Negative Number".
	- Nhánh 3: \verb|else| → Khi cả hai điều kiện trước sai, in "Zero".

- Kiểm thử với các giá trị đầu vào

| Test Case | Giá trị num | Nhánh được kiểm tra |
|:---------:|:-----------:|:-------------------:|
| TC1       | 5           | Nhánh 1             |
| TC2       | -3          | Nhánh 2             |
| TC3       | 0           | Nhánh 3             |

- Tính toán \verb|Branch Coverage|

   Với 3 test case trên, chúng ta đã kiểm tra tất cả các nhánh có thể có trong đoạn mã, do đó:

$$
\text{Branch Coverage} = \left( \frac{3}{3} \right) \times 100% = 100%
$$

- Kết luận
	- Để đạt 100% \verb|Branch Coverage|, chúng ta phải kiểm thử tất cả các nhánh có thể xảy ra trong đoạn mã.
	- Kiểm thử với số lượng test case ít hơn có thể bỏ sót một số nhánh, dẫn đến việc giảm độ bao phủ kiểm thử.

## Function Coverage

### Định nghĩa

\verb|Function Coverage| là một kỹ thuật trong kiểm thử phần mềm nhằm đo lường xem tất cả các hàm (functions) trong mã nguồn có được gọi ít nhất một lần trong quá trình kiểm thử hay không.

- Khi thực hiện kiểm thử, công cụ phân tích sẽ theo dõi các hàm nào đã được gọi và các hàm nào chưa được gọi.
- Nếu một hàm không được thực thi trong bất kỳ test case nào, có thể xảy ra lỗi tiềm ẩn vì hàm đó chưa được kiểm tra.
- \verb|Function Coverage| giúp đảm bảo rằng tất cả các hàm ít nhất đã được thực thi một lần trong quá trình kiểm thử.

Công thức tính \verb|Function Coverage|:

$$
\text{Function Coverage} = \left( \frac{\text{Số hàm được gọi}}{\text{Tổng số hàm}} \right) \times 100\%
$$

\pagebreak

### Ví dụ

Nếu một chương trình có 10 hàm nhưng chỉ có 8 hàm được gọi trong quá trình kiểm thử, \verb|Function Coverage| sẽ là:

$$
\left( \frac{8}{10} \right) \times 100\% = 80\%
$$

Có nhiều công cụ hỗ trợ đo \verb|Function Coverage| trong các ngôn ngữ lập trình khác nhau:

| Ngôn ngữ  | Công cụ đo \verb|Function Coverage| |
|--------------|--------------------------------|
| Python    | \verb|coverage.py|           |
| Java      | \verb|JaCoCo, Cobertura|     |
| C/C++     | \verb|gcov, lcov|            |
| JavaScript| \verb|Istanbul, Jest Coverage||

## Path Coverage

### Định nghĩa

\verb|Path Coverage| đảm bảo rằng tất cả các đường đi có thể có qua mã nguồn đều đã được thực thi ít nhất một lần trong quá trình kiểm thử.

- Một chương trình có thể có nhiều nhánh điều kiện (\verb|if-else, switch-case, vòng lặp for, while|).
- Một đường đi (path) là một chuỗi các câu lệnh được thực thi từ điểm bắt đầu đến điểm kết thúc của chương trình.
- \verb|Path Coverage| kiểm tra tất cả các đường đi có thể có, giúp phát hiện nhiều lỗi hơn so với \verb|Branch Coverage|.

Công thức tính \verb|Path Coverage|:

$$
\text{Path Coverage} = \left( \frac{\text{Số đường đi được kiểm tra}}{\text{Tổng số đường đi có thể có}} \right) \times 100\%
$$

### Ví dụ

\begin{lstlisting}[language=Python]
def process_list(lst):
    for num in lst:
        if num % 2 == 0:
            print("Even")
        else:
            print("Odd")
\end{lstlisting}

Các đường đi có thể có:

- Danh sách rỗng (\verb|lst = []|) → Không có vòng lặp nào chạy.
- Danh sách chỉ có số chẵn (\verb|lst = [2, 4, 6]|) → Luôn in "even".
- Danh sách chỉ có số lẻ (\verb|lst = [1, 3, 5]|) → Luôn in "odd".
- Danh sách có cả số chẵn và số lẻ (\verb|lst = [2, 3, 4]|) → Vừa in "even", vừa in "odd".

# Mức Coverage tối thiểu

Mức độ \verb|Code Coverage| phù hợp có thể khác nhau tùy thuộc vào loại kiểm thử và yêu cầu cụ thể của dự án. Dưới đây là một số hướng dẫn chung:

- Kiểm thử đơn vị (Unit Testing): Mức độ bao phủ mã lệnh thường được khuyến nghị là khoảng 90%. Điều này đảm bảo rằng hầu hết các chức năng nhỏ nhất của ứng dụng đều được kiểm tra kỹ lưỡng.  ￼
- Kiểm thử tích hợp (Integration Testing): Mức độ bao phủ có thể thấp hơn, khoảng 80%. Kiểm thử tích hợp tập trung vào việc đảm bảo các mô-đun hoặc thành phần khác nhau hoạt động cùng nhau một cách chính xác.  ￼
- Kiểm thử hệ thống (System Testing): Mức độ bao phủ thường vào khoảng 70%. Giai đoạn này kiểm tra toàn bộ hệ thống để đảm bảo rằng tất cả các yêu cầu chức năng và phi chức năng đều được đáp ứng.  

# Best Practices khi viết Unit Test

Unit Test là một phần quan trọng trong kiểm thử phần mềm, giúp đảm bảo từng thành phần nhỏ nhất của hệ thống hoạt động chính xác. Tuy nhiên, để viết unit test hiệu quả, cần tuân theo các best practices nhằm tối ưu hiệu suất, dễ bảo trì và đảm bảo chất lượng code.

## Viết Unit Test dễ bảo trì

Hạn chế phụ thuộc vào database hoặc persistent storage

- Vấn đề: Kiểm thử phụ thuộc vào database làm chậm tốc độ, khó kiểm soát dữ liệu test, và dễ bị ảnh hưởng khi môi trường thay đổi.
- Giải pháp:
	- Dùng mock dependencies thay vì database thật.
	- Nếu cần database, sử dụng in-memory database như SQLite (Python, Node.js) hoặc H2 (Java).

## Kiểm thử cả Happy case và Edge case

- Happy case: Kiểm thử các đầu vào hợp lệ, đảm bảo chức năng hoạt động đúng.
- Edge case: Kiểm thử các trường hợp bất thường như giá trị rỗng, null, số âm, dữ liệu vượt quá giới hạn.

**Cần kiểm thử cả đường đi thành công và các trường hợp lỗi để tránh bug không mong muốn**

\pagebreak

## Không viết Test trùng lặp hoặc quá phụ thuộc vào Implementation Details

- Vấn đề:
	- Test trùng lặp làm tốn tài nguyên và khó bảo trì.
	- Viết test quá chi tiết vào cách triển khai có thể gây lỗi nếu code thay đổi, dù kết quả đầu ra không đổi.
- Giải pháp:
	- Test nên tập trung vào kết quả mong đợi (expected output) hơn là cách nội bộ chương trình hoạt động.
	- Tránh test trùng lặp: Nếu một hàm đã được kiểm thử thông qua một phương thức khác, không cần kiểm thử lại.

**Cách tối ưu: Sử dụng parameterized tests để tránh trùng lặp.**

## Kiểm thử độc lập (Isolate Tests)

- Vấn đề:
	- Test không nên phụ thuộc vào trạng thái của test trước đó.
	- Nếu một test case bị lỗi, nó không được ảnh hưởng đến các test khác.
- Giải pháp:
	- Mỗi test case cần có dữ liệu riêng biệt, tránh dùng chung object hoặc trạng thái.
	- Dùng mock/stub thay vì gọi API hoặc database thật.
