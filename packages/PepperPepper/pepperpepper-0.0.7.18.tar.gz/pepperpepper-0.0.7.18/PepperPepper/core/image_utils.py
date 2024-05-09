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





'''
2.show_images
展示图像
'''
def show_images(imgs, num_rows, num_cols, titles=None, scale=1.5, normalize = False):
    # 绘制图像列表
    figsize = (num_cols * scale, num_rows * scale)
    _, axes = plt.subplots(num_rows, num_cols, figsize=figsize)
    axes = axes.flatten()
    for i, (ax, img) in enumerate(zip(axes, imgs)):
        if torch.is_tensor(img):
            # 图像张量
            if img.dim() == 3:
                img = img.permute(1, 2, 0)  # 将通道维度移动到最后的位置
            if normalize:
                img = img.numpy().clip(0, 1)  # 归一化到0-1范围，并裁剪超出范围的值
            ax.imshow(img)

        else:
            # PIL图像
            ax.imshow(img)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        if titles:
            ax.set_title(titles[i])
    return axes





'''
3.box_corner_to_center(boxes)
    summary: it transform the box corners to center
'''
def box_corner_to_center(boxes):
    x1, y1, x2, y2 = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    w = x2 - x1
    h = y2 - y1
    boxes = torch.stack([cx, cy, w, h], axis=-1)
    return boxes





'''
4.bbox_to_rect
    summary: it draw bounding box rectangle
'''
def bbox_to_rect(bbox, color):
    return plt.Rectangle(xy=(bbox[0], bbox[1]),width=bbox[2]-bbox[0],height=bbox[3]-bbox[1],fill=False,edgecolor=color,linewidth=2)


'''
5.show_boxes(axes, bboxes, labels=None, colors=None)
    summary: it show the box corners
    
'''
def show_boxes(axes, bboxes, labels, colors=None):
    """显示所有的边框"""
    def _make_list(obj, default_values=None):
        if obj is None:
            obj = default_values
        elif not isinstance(obj, (list, tuple)):
            obj = [obj]
        return obj

    labels = _make_list(labels)
    colors = _make_list(colors,['b', 'g', 'r', 'm', 'c' ])
    for i, bbox in enumerate(bboxes):
        color = colors[i % len(colors)]
        rect = bbox_to_rect(bbox.detach().numpy(), color)
        axes.add_patch(rect)
        if labels and len(labels)>i:
            text_color = 'k' if color== 'w' else 'w'
            axes.text(rect.xy[0],rect.xy[1],labels[i],va='center',ha='center',color=text_color,fontsize=9,bbox=dict(facecolor=color, lw=0))


# 5.visualize_bounding_boxes
def visualize_bounding_boxes(image, bounding_boxes, labels):
    """
    Visualizes bounding boxes on an image.

    Parameters:
        image (numpy.ndarray): The input image.
        bounding_boxes (list): A list of bounding boxes in the format [xmin, ymin, xmax, ymax].
        labels (list): A list of labels corresponding to each bounding box.
    """
    # Create figure and axes
    fig, ax = plt.subplots()

    # Display the image
    ax.imshow(image)

    # Add bounding boxes
    for bbox, label in zip(bounding_boxes, labels):
        xmin, ymin, xmax, ymax = bbox
        # Convert relative coordinates to absolute coordinates
        xmin_abs = xmin * image.shape[1]
        ymin_abs = ymin * image.shape[0]
        xmax_abs = xmax * image.shape[1]
        ymax_abs = ymax * image.shape[0]
        width = xmax_abs - xmin_abs
        height = ymax_abs - ymin_abs
        # Create a Rectangle patch
        rect = plt.Rectangle((xmin_abs, ymin_abs), width, height, fill=False, edgecolor='red', linewidth=2)
        ax.add_patch(rect)
        # Add label
        ax.text(xmin_abs, ymin_abs, label, color='red', fontsize=12, verticalalignment='top')

    plt.show()







