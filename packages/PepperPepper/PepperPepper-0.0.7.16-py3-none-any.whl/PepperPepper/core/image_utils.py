from ..environment import torch, cv2, plt




'''
1.visualize_grid_cells(image_path, W, H, X, Y)
将图像划分的grid cell进行可视化
image_path：图像的路径
W:设置图像的宽
H：设置图像的高
X、Y：设置grid cell的数量为X行×Y列个
'''


def visualize_grid_cells(image_path, W, H, ROW, COLUMN, Title='Resized Image with Grid Cells'):
    # 读取图像
    image = cv2.imread(image_path)

    # 如果图像为空（例如文件不存在或损坏），则退出
    if image is None:
        print(f"Error: Could not read image at {image_path}")
        return

        # 调整图像大小
    resized_image = cv2.resize(image, (W, H))

    # 划分grid cell
    cell_width = W // COLUMN
    cell_height = H // ROW

    # 遍历每个grid cell，绘制边界
    for i in range(COLUMN):
        for j in range(ROW):
            # 计算grid cell的左上角坐标
            start_x = i * cell_width
            start_y = j * cell_height
            # 计算grid cell的右下角坐标
            end_x = min((i + 1) * cell_width, W)  # 防止超出图像宽度
            end_y = min((j + 1) * cell_height, H)  # 防止超出图像高度

            # 绘制grid cell边界（使用BGR颜色，因为在OpenCV中图像是BGR格式的）
            cv2.rectangle(resized_image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

            # 显示原图与grid cell（合并到一张图像）
    plt.imshow(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
    plt.title(Title)
    plt.axis('off')
    plt.show()








