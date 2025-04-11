import cv2
import numpy as np
image_path = r"F:\\python_work\\ovi\\demo\\soybean_mungbean.png"
def detect_beans(frame):
    # 使用传入的帧图像
    if frame is None:
        print("无效的图像帧")
        return None, 0, 0  # 返回None和计数为0
    
    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 定义黄豆的颜色范围 (HSV格式)
    # 黄豆呈现淡黄色，有些偏米色
    yellow_lower = np.array([15, 30, 150])  # 降低饱和度下限，提高亮度下限
    yellow_upper = np.array([35, 150, 255]) # 扩大色调范围
    
    # 定义绿豆的颜色范围 (HSV格式)
    # 绿豆呈现深绿色，有光泽
    green_lower = np.array([35, 40, 40])   # 降低饱和度和亮度下限
    green_upper = np.array([90, 255, 200]) # 扩大色调范围
    
    # 创建颜色掩膜
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    green_mask = cv2.inRange(hsv, green_lower, green_upper)
    
    # 形态学处理
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))  # 增大核大小
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_CLOSE, kernel)
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_OPEN, kernel, iterations=1)  # 添加开运算去除噪点
    
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # 寻找轮廓
    yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 绘制结果
    result = frame.copy()
    # 在绘制轮廓时
    for cnt in yellow_contours:
        area = cv2.contourArea(cnt)
        if area > 200:  # 增大面积阈值
            cv2.drawContours(result, [cnt], -1, (0,255,255), 2)
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.putText(result, 'Yellow Bean', (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 1)
    
    for cnt in green_contours:
        area = cv2.contourArea(cnt)
        if area > 100:
            cv2.drawContours(result, [cnt], -1, (0,255,0), 2)
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.putText(result, 'Green Bean', (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    
    # 计算豆子数量
    yellow_count = sum(1 for cnt in yellow_contours if cv2.contourArea(cnt) > 200)
    green_count = sum(1 for cnt in green_contours if cv2.contourArea(cnt) > 100)
    
    # 在图像上显示数量统计
    cv2.putText(result, f'Yellow Beans: {yellow_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
    cv2.putText(result, f'Green Beans: {green_count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    
    # 返回处理结果和豆子数量
    return result, yellow_count, green_count

if __name__ == "__main__":
    # 测试代码
    test_image = cv2.imread(image_path)
    if test_image is not None:
        result = detect_beans(test_image)
        if result is not None:
            cv2.imshow('Result', result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()