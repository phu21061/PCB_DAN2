# Thư viện KiCad ME54BS12-nRF54L15

Thư viện `MinewSemi` gồm symbol và footprint liên kết sẵn, đã kiểm tra bằng KiCad 10.0.3.

## Dùng ngay trong dự án TPV3

1. Mở lại dự án `TPV3.kicad_pro` để KiCad nạp bảng thư viện mới.
2. Trong Schematic Editor, nhấn **A**, tìm `MinewSemi:ME54BS12-nRF54L15` và đặt symbol.
3. Thuộc tính Footprint đã là `MinewSemi:ME54BS12-nRF54L15`. Dùng **Update PCB from Schematic / F8** để đưa sang PCB.

Hai bảng `sym-lib-table` và `fp-lib-table` ở thư mục gốc TPV3 đã đăng ký thư viện bằng đường dẫn `${KIPRJMOD}`. Có thể di chuyển cả dự án mà không cần sửa đường dẫn. Chưa đặt linh kiện vào schematic hoặc PCB hiện có.

## Dùng cho dự án khác

Giải nén và giữ thư mục `MinewSemi` tại vị trí cố định. Trong **Preferences → Manage Symbol Libraries → Project Specific Libraries**, thêm file `MinewSemi.kicad_sym`, đặt nickname **MinewSemi**. Trong **Manage Footprint Libraries → Project Specific Libraries**, thêm thư mục `MinewSemi.pretty`, cũng đặt nickname **MinewSemi**. Giữ cùng nickname để liên kết footprint trong symbol hoạt động.

## Nội dung

- `MinewSemi.kicad_sym`: symbol một unit, 39 chân hiển thị đầy đủ; GPIO nhóm theo port, nguồn ở trên và GND ở dưới.
- `MinewSemi.pretty/ME54BS12-nRF54L15.kicad_mod`: footprint SMD 39 pad, có F.SilkS, F.Fab, F.CrtYd và rule area anten.
- `ME54BS12-nRF54L15_pinmap.csv`: bảng số pad, tín hiệu, tọa độ nhìn từ trên và kích thước land.
- `preview/`: hình PNG và SVG xuất trực tiếp từ KiCad.
- `docs/`: bản datasheet đã sử dụng.
- `generate_library.py`: mã Python tiêu chuẩn để tái tạo symbol, footprint và pinmap.
- `validation/`: kết quả kiểm tra.

## Hướng và cách dựng footprint

Footprint nhìn từ **trên**, anten hướng lên (Y âm), chân 1 ở trái phía anten. Gốc tọa độ nằm giữa thân module. Bản vẽ mặt đáy được lật ngang để khớp sơ đồ **Top View** ở trang 6; không dùng trực tiếp tọa độ mặt đáy.

Thân module 12 × 15,8 mm. Hai hàng chân cạnh có bước 1,27 mm. Land cạnh chọn 2,0 × 0,8 mm, gồm phần nằm trong thân 0,8 mm và phần nhô ra ngoài 1,2 mm. Tâm pad trong có bước X 1,5 mm và Y 1,8 mm. Cột 1 cách mép trái 2,05 mm khi nhìn từ trên; hàng F cách mép dưới 1,4 mm. Pad trong chọn hình tròn đường kính 0,8 mm theo hình học bản vẽ; bản vẽ không ghi riêng dung sai/đường kính pad trong. Khẩu độ paste của pad trong giảm 10% theo đường kính (0,72 mm), mask mở thêm 0,05 mm mỗi bên.

Đây là **land pattern tự dựng từ bản vẽ cơ khí**, không phải file CAD/land pattern do hãng phát hành. Kích thước land hàn và khẩu độ stencil là lựa chọn thiết kế được ghi rõ ở trên; cần đối chiếu module thực tế và yêu cầu lắp ráp trước khi sản xuất.

## Anten và kết nối

Rule area cấm đường mạch, via, pad, copper pour và linh kiện trên các lớp đồng. Vùng này phủ phần anten, thêm 4 mm sang hai bên và ra đầu anten. Biên phía dưới ở Y = -3,84 mm, ứng với vùng anten sâu 4,06 mm; không kéo vùng cấm xuống các chân của module. Đường bao RF trên `Dwgs.User` giúp kiểm tra vị trí khi đặt sát mép PCB. Rule area không tự tạo lỗ khoét hoặc thay đổi `Edge.Cuts`; chọn vị trí mép bo phù hợp và kiểm tra khoảng hở với vỏ máy riêng.

Nối đủ các chân GND **11, A1, A5, B5, C5**. Để hở chân **1 / RF** khi dùng anten PCB tích hợp. Symbol hiển thị chân 18 là RESET có gạch trên (active low); chân này tương ứng **NRESET** trong datasheet.

## Nguồn tham khảo

MinewSemi, **ME54BS12-nRF54L15 Datasheet K EN**, v1.0.0, ngày 2025-08-07: trang 6–7 cho pinout, trang 8 cho cơ khí và trang 9 cho anten/SMT.

https://en.minewsemi.com/file/ME54BS12-nRF54L15_Datasheet_K_EN.pdf
