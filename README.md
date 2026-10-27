# Bài thực hành Android: Danh sách sản phẩm

Ứng dụng Kotlin gồm hai màn hình:

- **MainActivity:** hiển thị 30 sản phẩm bằng `ArrayList<Product>`, `ProductAdapter : ArrayAdapter<Product>` và `ListView.setAdapter`. Spinner lọc theo 6 danh mục. Nút Tìm kiếm tìm theo tên hoặc mã trên **toàn bộ** sản phẩm và đưa Spinner về “Tất cả”. Tìm kiếm không phân biệt hoa thường hoặc dấu tiếng Việt.
- **ProductDetailActivity:** hiển thị tên, ảnh, mô tả, giá, danh mục và mã của sản phẩm được chọn.

Cả hai màn hình đều hiển thị **ĐÔNG ĐỨC NGUYÊN - B23DCVT311** ở phía trên.

## Dữ liệu

Nguồn dữ liệu duy nhất là [`app/src/main/assets/database.json`](app/src/main/assets/database.json). Mỗi bản ghi có `code`, `name`, `price`, `category`, `image` và `description`. Ảnh minh họa nằm trong [`app/src/main/assets/images`](app/src/main/assets/images) và đường dẫn `file:///android_asset/images/...` được lưu trong JSON. Ứng dụng đọc trực tiếp JSON từ assets nên dùng được khi không có mạng.

Script [`tools/generate_catalog.py`](tools/generate_catalog.py) tái tạo dữ liệu mẫu và ảnh; cần Python với Pillow. Ứng dụng Android không cần Python hay Pillow để chạy.

## Mở và chạy

Mở thư mục dự án bằng Android Studio, để Gradle đồng bộ rồi chạy cấu hình `app` trên thiết bị Android API 23 trở lên. Trên Windows có thể build bằng `gradlew.bat :app:assembleDebug`. APK được tạo tại `app/build/outputs/apk/debug/app-debug.apk`.
