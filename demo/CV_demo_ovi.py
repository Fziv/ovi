import cv2

def main():
    # 初始化摄像头
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("无法打开摄像头")
        return
    
    # 设置窗口
    cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Grayscale', cv2.WINDOW_NORMAL)
    
    while True:
        # 读取帧
        ret, frame = cap.read()
        if not ret:
            print("无法获取帧")
            break
            
        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 显示图像
        cv2.imshow('Original', frame)
        cv2.imshow('Grayscale', gray)
        
        # 按ESC退出
        if cv2.waitKey(1) == 27:
            break
            
    # 释放资源
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()