import cv2
import numpy as np

def test_opencv_environment():
    # 测试OpenCV基本功能
    print(f"OpenCV版本: {cv2.__version__}")
    
    # 尝试创建一张测试图像代替lena.jpg
    print("创建测试图像代替lena.jpg")
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    cv2.putText(img, "OpenCV Test", (50, 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Test Image', img)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
    
    # 测试摄像头
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("错误: 无法打开摄像头")
        return
    
    print("摄像头测试 - 按ESC键退出")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("错误: 无法从摄像头获取帧")
            break
            
        cv2.imshow('Camera Test', frame)
        if cv2.waitKey(1) == 27:  # ESC键
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("OpenCV环境测试完成")

if __name__ == "__main__":
    test_opencv_environment()