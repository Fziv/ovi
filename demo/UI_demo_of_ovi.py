# import dearpygui.dearpygui as dpg

# dpg.create_context()
# dpg.create_viewport(title='OVI UI Demo', width=600, height=300)

# with dpg.window(label="Main Window"):
#     dpg.add_text("OpenCV 现代界面")

# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()

import dearpygui.dearpygui as dpg
import cv2
import numpy as np
from threading import Thread # 线程，标准库
import time  # 添加在文件顶部
from bean_detection import detect_beans  # 导入豆子检测函数

class OpenCVApp:
    def __init__(self):
        self.cap = None # 视频捕获对象
        self.frame = None # 当前帧
        self.running = False # 运行标志
        self.bean_detection_enabled = False # 豆子检测开关
        self.yellow_count = 0 # 黄豆数量
        self.green_count = 0 # 绿豆数量
        self.init_ui() # 初始化UI

    def init_ui(self):
        dpg.create_context()
        
        # 创建纹理用于显示OpenCV图像
        with dpg.texture_registry():
            self.texture = dpg.add_raw_texture(
                width=640, height=480,  # 确保与后续resize尺寸一致
                default_value=[],
                format=dpg.mvFormat_Float_rgb
            )

        # 主窗口
        with dpg.window(label="OpenCV Integration Demo", width=800, height=600):
            # 图像显示区域
            dpg.add_image(self.texture, tag="cv_image")
            
            # 控制面板
            with dpg.group(horizontal=True):
                dpg.add_button(label="Start Camera", callback=self.start_camera)
                dpg.add_button(label="Stop Camera", callback=self.stop_camera)
                dpg.add_button(label="Toggle Bean Detection", callback=self.toggle_bean_detection)
                dpg.add_slider_int(label="Brightness", min_value=-100, max_value=100, 
                                  callback=self.adjust_brightness, tag="brightness")
            
            # 豆子数量显示区域
            with dpg.group():
                dpg.add_text("statistical results", color=(255, 255, 0))
                dpg.add_text("yellow beans: 0", tag="yellow_count_text")
                dpg.add_text("green beans: 0", tag="green_count_text")

        # 视口设置
        dpg.create_viewport(title='OVI OpenCV Integration', width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()

    def start_camera(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("无法打开摄像头")
                return
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.running = True
            Thread(target=self.update_frame, daemon=True).start()

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()

    def adjust_brightness(self, sender, data):
        if self.frame is not None:
            brightness = dpg.get_value("brightness")
            adjusted = cv2.convertScaleAbs(self.frame, alpha=1, beta=brightness)
            self.update_texture(adjusted)

    def toggle_bean_detection(self):
        self.bean_detection_enabled = not self.bean_detection_enabled

    def update_frame(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                if self.bean_detection_enabled:
                    # 进行豆子检测
                    processed_frame, yellow_count, green_count = detect_beans(frame)
                    if processed_frame is not None:
                        self.frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                        # 更新豆子数量
                        self.yellow_count = yellow_count
                        self.green_count = green_count
                        # 更新UI显示
                        dpg.set_value("yellow_count_text", f"黄豆数量: {yellow_count}")
                        dpg.set_value("green_count_text", f"绿豆数量: {green_count}")
                    else:
                        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                else:
                    self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # 清零豆子数量
                    self.yellow_count = 0
                    self.green_count = 0
                    dpg.set_value("yellow_count_text", "黄豆数量: 0")
                    dpg.set_value("green_count_text", "绿豆数量: 0")
                self.update_texture(self.frame)
            time.sleep(0.03)  # 约30FPS

    def update_texture(self, frame):
        try:
            frame = cv2.resize(frame, (640, 480))
            if frame.dtype != np.float32:
                frame = frame.astype(np.float32) / 255.0  # 显式转换为float32
            if frame.shape[2] != 3:  # 确保是3通道图像
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 确保数据是C连续的
            if not frame.flags['C_CONTIGUOUS']:
                frame = np.ascontiguousarray(frame)
            dpg.set_value(self.texture, frame.ravel())
        except Exception as e:
            print(f"纹理更新错误: {str(e)}")
            print(f"当前帧形状: {frame.shape if 'frame' in locals() else '无帧数据'}")

    def run(self):
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
        dpg.destroy_context()

if __name__ == "__main__":
    app = OpenCVApp()
    app.run()