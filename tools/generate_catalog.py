"""Generate bundled sample catalog and illustrated PNGs. Requires Pillow."""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app" / "src" / "main" / "assets"
IMAGES = ASSETS / "images"
IMAGES.mkdir(parents=True, exist_ok=True)

# category, name, price (VND), description
ITEMS = [
    ("Điện thoại", "Nova X1 128GB", 6990000, "Điện thoại màn hình 6,5 inch sắc nét, bộ nhớ 128GB và pin 5.000mAh. Phù hợp cho học tập, chụp ảnh và giải trí mỗi ngày."),
    ("Điện thoại", "Nova X1 Pro 256GB", 9990000, "Phiên bản Pro có màn hình AMOLED 120Hz, camera chính 50MP và bộ nhớ 256GB. Sạc nhanh giúp tiết kiệm thời gian."),
    ("Điện thoại", "Pixelon A5 128GB", 5490000, "Thiết kế gọn nhẹ với camera góc rộng, nhận diện khuôn mặt và thời lượng pin đủ dùng cả ngày."),
    ("Điện thoại", "Pixelon A5 Plus 256GB", 7490000, "Màn hình lớn 6,7 inch, loa kép và dung lượng lưu trữ rộng rãi cho ảnh, video và ứng dụng."),
    ("Điện thoại", "Orion Z Fold 512GB", 24990000, "Điện thoại gập với màn hình trong rộng rãi, hỗ trợ đa nhiệm và bút cảm ứng cho công việc linh hoạt."),
    ("Máy tính", "AstraBook 14", 12990000, "Laptop 14 inch mỏng nhẹ, RAM 16GB và SSD 512GB. Phù hợp cho văn phòng, học trực tuyến và di chuyển."),
    ("Máy tính", "AstraBook Air 13", 15990000, "Máy tính xách tay 13 inch có thân nhôm, bàn phím có đèn nền và pin lâu cho ngày làm việc bận rộn."),
    ("Máy tính", "Volt Gaming 15", 22990000, "Laptop chơi game màn hình 144Hz, tản nhiệt hai quạt và card đồ họa rời cho trải nghiệm mượt mà."),
    ("Máy tính", "StudioBook Pro 16", 28990000, "Màn hình 16 inch độ phân giải cao và hiệu năng mạnh cho chỉnh sửa ảnh, dựng video và lập trình."),
    ("Máy tính", "MiniDesk M2", 10990000, "Máy tính để bàn cỡ nhỏ, hoạt động êm và có nhiều cổng kết nối cho góc làm việc gọn gàng."),
    ("Âm thanh", "Tai nghe WaveBuds S", 1190000, "Tai nghe không dây nhỏ gọn với hộp sạc tiện lợi, điều khiển cảm ứng và chất âm cân bằng."),
    ("Âm thanh", "Tai nghe WaveBuds Pro", 2490000, "Tai nghe true wireless có chống ồn chủ động, chế độ xuyên âm và thời lượng nghe nhạc dài."),
    ("Âm thanh", "Tai nghe chụp tai Sonic H7", 1890000, "Đệm tai mềm, kết nối Bluetooth ổn định và micro tích hợp cho học tập hoặc làm việc từ xa."),
    ("Âm thanh", "Loa Bluetooth Pulse Mini", 990000, "Loa di động nhỏ gọn, chống nước nhẹ và phát nhạc rõ ràng cho các buổi gặp gỡ ngoài trời."),
    ("Âm thanh", "Loa Bluetooth Pulse Max", 2990000, "Loa công suất lớn với âm trầm mạnh, đèn LED và pin sạc phục vụ không gian giải trí tại nhà."),
    ("Phụ kiện", "Sạc nhanh Volt 30W", 390000, "Củ sạc USB-C công suất 30W, thiết kế nhỏ gọn và hỗ trợ sạc nhanh cho điện thoại hoặc máy tính bảng."),
    ("Phụ kiện", "Sạc dự phòng PowerGo 10000", 690000, "Pin dự phòng dung lượng 10.000mAh, có hai cổng sạc và màn hình hiển thị mức pin còn lại."),
    ("Phụ kiện", "Chuột không dây Click M3", 490000, "Chuột không dây cầm thoải mái, thao tác êm và kết nối nhanh với laptop hoặc máy tính để bàn."),
    ("Phụ kiện", "Bàn phím cơ KeyFlow 87", 1290000, "Bàn phím cơ 87 phím, đèn nền có thể điều chỉnh và kết cấu chắc chắn cho gõ văn bản hằng ngày."),
    ("Phụ kiện", "Cáp USB-C Flex 2m", 190000, "Cáp USB-C dài 2 mét với lớp bọc bền chắc, thuận tiện cho sạc và truyền dữ liệu."),
    ("Gia dụng", "Đèn bàn Lumi LED", 790000, "Đèn bàn LED có ba mức sáng, ánh sáng dịu và cần đèn linh hoạt cho góc học tập."),
    ("Gia dụng", "Quạt mini Breeze USB", 450000, "Quạt để bàn nhỏ gọn, ba tốc độ gió và cổng cấp nguồn USB phù hợp không gian cá nhân."),
    ("Gia dụng", "Máy lọc không khí Pure A1", 3490000, "Máy lọc không khí cho phòng ngủ, có bộ lọc nhiều lớp và chế độ hoạt động yên tĩnh."),
    ("Gia dụng", "Máy xay Smoothie Go", 890000, "Máy xay cầm tay tiện dụng với cốc mang đi, phù hợp chuẩn bị sinh tố hoặc đồ uống nhanh."),
    ("Gia dụng", "Robot hút bụi CleanBot S", 5990000, "Robot hút bụi tự động có cảm biến tránh vật cản và lịch dọn dẹp cho sàn nhà sạch sẽ."),
    ("Thời trang", "Balo Urban 20L", 590000, "Balo 20 lít có ngăn laptop riêng, quai đeo êm và chất liệu chống bám nước nhẹ."),
    ("Thời trang", "Túi đeo chéo Daily", 390000, "Túi đeo chéo gọn nhẹ với nhiều ngăn nhỏ để giữ điện thoại, ví và vật dụng cá nhân."),
    ("Thời trang", "Giày thể thao Move One", 1190000, "Giày thể thao đế êm, thiết kế thoáng khí cho đi bộ, tập luyện và hoạt động thường ngày."),
    ("Thời trang", "Kính mát Sunline", 490000, "Kính mát gọng nhẹ, tròng chống tia UV và kiểu dáng dễ phối với trang phục hằng ngày."),
    ("Thời trang", "Đồng hồ Classic M", 1490000, "Đồng hồ mặt tròn tối giản, dây đeo thoải mái và khả năng kháng nước khi rửa tay."),
]

COLORS = {
    "Điện thoại": (72, 102, 217),
    "Máy tính": (38, 132, 153),
    "Âm thanh": (150, 87, 196),
    "Phụ kiện": (220, 122, 68),
    "Gia dụng": (82, 155, 112),
    "Thời trang": (198, 91, 124),
}

FONT_PATH = "C:/Windows/Fonts/segoeui.ttf" if Path("C:/Windows/Fonts/segoeui.ttf").is_file() else "DejaVuSans.ttf"
FONT_BOLD_PATH = "C:/Windows/Fonts/segoeuib.ttf" if Path("C:/Windows/Fonts/segoeuib.ttf").is_file() else "DejaVuSans-Bold.ttf"
font = ImageFont.truetype(FONT_BOLD_PATH, 27)
small_font = ImageFont.truetype(FONT_PATH, 17)


def illustration(draw, category, name, color, variant):
    """Draw a recognizable product silhouette with small variations."""
    white = (255, 255, 255)
    navy = (36, 51, 74)
    pale = tuple(min(255, x + 130) for x in color)
    x_shift = (variant - 2) * 5

    if category == "Điện thoại":
        x = 212 + x_shift
        draw.rounded_rectangle((x, 38, x + 120, 226), radius=18, fill=navy)
        draw.rounded_rectangle((x + 7, 46, x + 113, 209), radius=12, fill=pale)
        draw.ellipse((x + 43, 214, x + 77, 218), fill=white)
        draw.ellipse((x + 20, 68, x + 89, 137), fill=color)
        draw.ellipse((x + 28, 77, x + 81, 130), fill=white)
        draw.ellipse((x + 38, 87, x + 70, 119), fill=color)
    elif category == "Máy tính":
        draw.rounded_rectangle((129, 50, 383, 203), radius=10, fill=navy)
        draw.rounded_rectangle((139, 60, 373, 193), radius=4, fill=pale)
        draw.polygon([(106, 207), (406, 207), (431, 229), (82, 229)], fill=navy)
        draw.rounded_rectangle((199, 213, 313, 218), radius=3, fill=white)
        draw.ellipse((225 + x_shift, 89, 285 + x_shift, 149), fill=color)
    elif category == "Âm thanh":
        if "Loa" in name:
            draw.rounded_rectangle((179, 59, 333, 223), radius=28, fill=navy)
            draw.ellipse((205, 81, 307, 183), fill=pale)
            draw.ellipse((231, 107, 281, 157), fill=color)
            draw.ellipse((247, 123, 265, 141), fill=white)
        else:
            draw.arc((168, 42, 344, 206), 180, 360, fill=navy, width=23)
            draw.rounded_rectangle((166, 125, 209, 221), radius=17, fill=navy)
            draw.rounded_rectangle((303, 125, 346, 221), radius=17, fill=navy)
            draw.rounded_rectangle((176, 145, 201, 207), radius=9, fill=pale)
            draw.rounded_rectangle((311, 145, 336, 207), radius=9, fill=pale)
    elif category == "Phụ kiện":
        if "Bàn phím" in name:
            draw.rounded_rectangle((110, 90, 402, 210), radius=14, fill=navy)
            for row in range(4):
                for col in range(11):
                    draw.rounded_rectangle((122 + col * 24, 103 + row * 24, 141 + col * 24, 120 + row * 24), radius=3, fill=pale)
        elif "Chuột" in name:
            draw.rounded_rectangle((207, 60, 305, 222), radius=48, fill=navy)
            draw.line((256, 61, 256, 126), fill=pale, width=3)
            draw.rounded_rectangle((250, 89, 262, 119), radius=6, fill=color)
        elif "Cáp" in name:
            draw.arc((144, 64, 364, 220), 5, 320, fill=navy, width=19)
            draw.rounded_rectangle((333, 158, 379, 193), radius=7, fill=navy)
            draw.rectangle((375, 165, 392, 185), fill=pale)
        else:
            draw.rounded_rectangle((193, 58, 319, 223), radius=22, fill=navy)
            draw.rounded_rectangle((206, 73, 306, 195), radius=13, fill=pale)
            draw.polygon([(263, 99), (235, 143), (256, 143), (247, 174), (281, 127), (258, 127)], fill=color)
    elif category == "Gia dụng":
        if "Đèn" in name:
            draw.polygon([(183, 62), (308, 62), (339, 137), (155, 137)], fill=navy)
            draw.rectangle((240, 137, 254, 212), fill=navy)
            draw.rounded_rectangle((195, 207, 299, 223), radius=7, fill=navy)
            draw.ellipse((225, 122, 268, 156), fill=pale)
        elif "Quạt" in name:
            draw.ellipse((177, 52, 335, 210), outline=navy, width=13)
            for box in [(233, 71, 282, 130), (198, 129, 263, 166), (257, 131, 314, 169)]:
                draw.ellipse(box, fill=pale)
            draw.ellipse((239, 117, 273, 151), fill=navy)
            draw.rectangle((250, 210, 262, 226), fill=navy)
        elif "Robot" in name:
            draw.ellipse((139, 73, 373, 226), fill=navy)
            draw.ellipse((153, 83, 359, 213), fill=pale)
            draw.ellipse((239, 126, 273, 160), fill=color)
        else:
            draw.rounded_rectangle((188, 55, 324, 225), radius=20, fill=navy)
            draw.rounded_rectangle((204, 68, 308, 173), radius=10, fill=pale)
            draw.ellipse((242, 187, 270, 215), fill=white)
    else:
        if "Balo" in name or "Túi" in name:
            draw.arc((206, 52, 306, 142), 185, 355, fill=navy, width=15)
            draw.rounded_rectangle((175, 100, 337, 225), radius=27, fill=navy)
            draw.rounded_rectangle((190, 132, 322, 201), radius=14, fill=pale)
            draw.line((255, 132, 255, 192), fill=color, width=7)
        elif "Giày" in name:
            draw.polygon([(133, 172), (203, 136), (272, 155), (323, 187), (383, 195), (390, 222), (128, 222)], fill=navy)
            draw.line((132, 212, 386, 212), fill=white, width=8)
            for x in (235, 254, 273):
                draw.line((x, 165, x + 22, 174), fill=pale, width=5)
        elif "Kính" in name:
            draw.line((115, 112, 197, 122), fill=navy, width=11)
            draw.line((315, 122, 397, 112), fill=navy, width=11)
            draw.arc((227, 109, 285, 144), 190, 350, fill=navy, width=8)
            draw.rounded_rectangle((168, 124, 236, 182), radius=23, fill=navy)
            draw.rounded_rectangle((276, 124, 344, 182), radius=23, fill=navy)
            draw.ellipse((180, 135, 224, 171), fill=pale)
            draw.ellipse((288, 135, 332, 171), fill=pale)
        else:
            draw.rounded_rectangle((230, 39, 282, 232), radius=15, fill=navy)
            draw.ellipse((187, 93, 325, 231), fill=navy)
            draw.ellipse((201, 107, 311, 217), fill=pale)
            draw.line((256, 161, 256, 125), fill=navy, width=7)
            draw.line((256, 161, 283, 177), fill=navy, width=7)


products = []
for index, (category, name, price, description) in enumerate(ITEMS, start=1):
    code = f"SP{index:03d}"
    color = COLORS[category]
    image = Image.new("RGB", (512, 360), (248, 250, 255))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((12, 12, 500, 348), radius=28, fill=(241, 245, 252))
    draw.ellipse((65, -70, 425, 290), fill=tuple(min(255, c + 150) for c in color))
    draw.ellipse((369, 26, 460, 117), fill=(255, 255, 255))
    draw.ellipse((64, 145, 110, 191), fill=(255, 255, 255))
    illustration(draw, category, name, color, (index - 1) % 5)
    draw.rounded_rectangle((24, 267, 488, 338), radius=16, fill=(255, 255, 255))
    draw.text((40, 279), name, font=font, fill=(36, 51, 74))
    draw.text((41, 311), category.upper(), font=small_font, fill=color)
    image.save(IMAGES / f"{code}.png", optimize=True)
    products.append({
        "code": code,
        "name": name,
        "price": price,
        "category": category,
        "image": f"file:///android_asset/images/{code}.png",
        "description": description,
    })

(ASSETS / "database.json").write_text(json.dumps(products, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Generated {len(products)} products and images in {ASSETS}")
