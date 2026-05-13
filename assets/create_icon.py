#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建应用图标 - 现代集装箱装载模拟器图标
深蓝渐变背景 + 白色集装箱 + 优化箭头
"""

from PIL import Image, ImageDraw
import os, math

os.makedirs("assets", exist_ok=True)


def hex_to_rgba(hex_color, alpha=255):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) + (alpha,)


def draw_rounded_rect(draw, xy, r, fill=None, outline=None, width=1):
    """绘制圆角矩形"""
    x1, y1, x2, y2 = xy
    r = min(r, (x2 - x1) // 2, (y2 - y1) // 2)
    if r <= 0:
        draw.rectangle(xy, fill=fill, outline=outline, width=width)
        return
    # 主体
    draw.rectangle([x1 + r, y1, x2 - r, y2], fill=fill)
    draw.rectangle([x1, y1 + r, x2, y2 - r], fill=fill)
    # 四角
    draw.pieslice([x1, y1, x1 + r * 2, y1 + r * 2], 180, 270, fill=fill)
    draw.pieslice([x2 - r * 2, y1, x2, y1 + r * 2], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - r * 2, x1 + r * 2, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - r * 2, y2 - r * 2, x2, y2], 0, 90, fill=fill)
    if outline:
        draw.arc([x1, y1, x1 + r * 2, y1 + r * 2], 180, 270, fill=outline, width=width)
        draw.arc([x2 - r * 2, y1, x2, y1 + r * 2], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2 - r * 2, x1 + r * 2, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2 - r * 2, y2 - r * 2, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1 + r, y1, x2 - r, y1], fill=outline, width=width)
        draw.line([x1 + r, y2, x2 - r, y2], fill=outline, width=width)
        draw.line([x1, y1 + r, x1, y2 - r], fill=outline, width=width)
        draw.line([x2, y1 + r, x2, y2 - r], fill=outline, width=width)


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(4))


def create_gradient_bg(size):
    """创建深蓝渐变背景"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    top_color = hex_to_rgba("#1a237e")   # 深蓝
    bot_color = hex_to_rgba("#0d47a1")   # 亮蓝
    for y in range(size):
        t = y / size
        color = lerp_color(top_color, bot_color, t)
        for x in range(size):
            img.putpixel((x, y), color)
    return img


def create_icon(size):
    """创建指定尺寸的图标"""
    # 背景圆角矩形
    corner_r = int(size * 0.22)
    margin = max(1, size // 48)

    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))

    # 绘制渐变背景
    bg = create_gradient_bg(size)
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    draw_rounded_rect(mask_draw, [margin, margin, size - margin, size - margin], corner_r, fill=255)
    img = Image.composite(bg, img, mask)

    draw = ImageDraw.Draw(img)

    # --- 集装箱主体 ---
    container_w = int(size * 0.52)
    container_h = int(size * 0.44)
    cx = (size - container_w) // 2
    cy = (size - container_h) // 2 - int(size * 0.02)

    # 集装箱颜色
    body_color = (255, 255, 255, 255)
    shadow_color = (200, 210, 225, 255)
    door_color = (220, 228, 240, 255)
    accent_color = (30, 136, 229, 255)  # 蓝色强调
    corner_color = (180, 195, 215, 255)

    # 集装箱侧面 (阴影面 - 右侧)
    side_w = int(container_w * 0.15)
    draw.rectangle(
        [cx + container_w - side_w, cy, cx + container_w, cy + container_h],
        fill=shadow_color
    )

    # 集装箱主体正面
    draw.rectangle(
        [cx, cy, cx + container_w - side_w, cy + container_h],
        fill=body_color
    )

    # 集装箱顶部 (透视面)
    top_h = int(container_h * 0.18)
    top_skew = int(container_w * 0.08)
    top_color = (235, 240, 248, 255)
    top_pts = [
        (cx, cy),
        (cx + container_w - side_w, cy),
        (cx + container_w - side_w + top_skew, cy - top_h),
        (cx + top_skew, cy - top_h),
    ]
    draw.polygon(top_pts, fill=top_color)

    # 侧面顶部
    side_top_pts = [
        (cx + container_w - side_w, cy),
        (cx + container_w, cy),
        (cx + container_w, cy - top_h),
        (cx + container_w - side_w + top_skew, cy - top_h),
    ]
    draw.polygon(side_top_pts, fill=(175, 188, 210, 255))

    # --- 集装箱波纹线条 ---
    line_count = max(3, container_h // (max(4, size // 32)))
    line_spacing = container_h // (line_count + 1)
    line_color = (210, 218, 232, 200)
    for i in range(1, line_count + 1):
        ly = cy + i * line_spacing
        draw.line(
            [(cx + int(container_w * 0.05), ly),
             (cx + container_w - side_w - int(container_w * 0.05), ly)],
            fill=line_color,
            width=max(1, size // 256)
        )

    # --- 集装箱门缝 ---
    door_x = cx + (container_w - side_w) // 2
    door_line_color = (190, 200, 215, 200)
    gap = max(1, size // 512)
    draw.line(
        [(door_x - gap, cy + int(container_h * 0.08)),
         (door_x - gap, cy + container_h - int(container_h * 0.08))],
        fill=door_line_color, width=max(1, size // 192)
    )
    draw.line(
        [(door_x + gap, cy + int(container_h * 0.08)),
         (door_x + gap, cy + container_h - int(container_h * 0.08))],
        fill=door_line_color, width=max(1, size // 192)
    )

    # --- 门把手/锁杆 ---
    lock_w = max(1, size // 128)
    lock_h = int(container_h * 0.22)
    lock_color = (140, 158, 180, 255)
    for lx_off in [-int(container_w * 0.06), int(container_w * 0.06)]:
        lx = door_x + lx_off
        draw.rectangle(
            [lx - lock_w, cy + container_h // 2 - lock_h // 2,
             lx + lock_w, cy + container_h // 2 + lock_h // 2],
            fill=lock_color
        )

    # --- 角件 (集装箱八个角的方块) ---
    corner_size = max(2, size // 64)
    corners = [
        (cx, cy),  # 左上
        (cx + container_w - side_w - corner_size, cy),  # 右上(正面)
        (cx, cy + container_h - corner_size),  # 左下
        (cx + container_w - side_w - corner_size, cy + container_h - corner_size),  # 右下
    ]
    for cx_c, cy_c in corners:
        draw.rectangle(
            [cx_c, cy_c, cx_c + corner_size, cy_c + corner_size],
            fill=corner_color
        )

    # --- 蓝色优化箭头 (右下角) ---
    arrow_size = int(size * 0.2)
    arrow_margin = int(size * 0.12)
    ax = size - arrow_margin - arrow_size // 2
    ay = size - arrow_margin - arrow_size // 2

    # 圆形背景
    circle_r = arrow_size // 2 + int(size * 0.03)
    draw.ellipse(
        [ax - circle_r, ay - circle_r, ax + circle_r, ay + circle_r],
        fill=accent_color
    )

    # 向上箭头
    arrow_len = int(arrow_size * 0.6)
    arrow_thick = max(2, size // 64)
    arrow_head = int(arrow_size * 0.25)
    draw.line(
        [(ax, ay - arrow_len // 2), (ax, ay + arrow_len // 2)],
        fill=(255, 255, 255, 255), width=arrow_thick
    )
    # 箭头尖
    draw.polygon(
        [(ax - arrow_head, ay - arrow_len // 2 + arrow_head),
         (ax, ay - arrow_len // 2 - arrow_head // 3),
         (ax + arrow_head, ay - arrow_len // 2 + arrow_head)],
        fill=(255, 255, 255, 255)
    )

    return img


def create_ico():
    """创建Windows ICO文件"""
    print("创建 icon.ico...")
    images = []
    for size in [16, 32, 48, 256]:
        images.append(create_icon(size))
    images[-1].save("assets/icon.ico", format='ICO',
                    sizes=[(16, 16), (32, 32), (48, 48), (256, 256)])
    print("  -> assets/icon.ico")


def create_icns():
    """创建macOS ICNS文件"""
    print("创建 icon.icns...")
    iconset_dir = "assets/icon.iconset"
    os.makedirs(iconset_dir, exist_ok=True)

    for size in [16, 32, 128, 256, 512, 1024]:
        img = create_icon(size)
        img.save(f"{iconset_dir}/icon_{size}x{size}.png", format='PNG')
        if size >= 32:
            img_2x = create_icon(size * 2)
            img_2x.save(f"{iconset_dir}/icon_{size}x{size}@2x.png", format='PNG')

    import subprocess
    try:
        subprocess.run(['iconutil', '-c', 'icns', iconset_dir, '-o', 'assets/icon.icns'],
                       check=True, capture_output=True)
        print("  -> assets/icon.icns")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  警告: iconutil不可用")
        create_icon(1024).save("assets/icon.png", format='PNG')
        print("  -> assets/icon.png (备用)")


def create_png():
    """创建PNG图标"""
    print("创建 icon.png...")
    create_icon(1024).save("assets/icon.png", format='PNG')
    print("  -> assets/icon.png")


def create_favicon():
    """创建网站favicon"""
    print("创建 favicon.ico...")
    create_icon(32).save("assets/favicon.ico", format='ICO')
    print("  -> assets/favicon.ico")


if __name__ == "__main__":
    print("=" * 48)
    print("  生成应用图标")
    print("=" * 48)
    print()
    create_ico()
    create_icns()
    create_png()
    create_favicon()
    print()
    print("=" * 48)
    print("  图标生成完成！")
    print("=" * 48)
