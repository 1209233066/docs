
# --code:utf-8--

import cv2 as cv
from starlette.applications import Starlette
from starlette.websockets import WebSocket, WebSocketDisconnect
from starlette.routing import Route, WebSocketRoute
from starlette.responses import HTMLResponse
import asyncio
import pathlib
import pyaudio  # 新增：音频捕获库

# 初始化Starlette应用
app = Starlette(debug=True)

# 原摄像头初始化（修改为类成员方便管理）
class VideoStreamer:
    def __init__(self):
        # 关键修改：显式指定使用DirectShow后端（cv.CAP_DSHOW）
        self.cap = cv.VideoCapture(0, cv.CAP_DSHOW)  # 第一个摄像头为0 第二个为1
        # 新增：音频设备初始化
        self.audio = pyaudio.PyAudio()
        self.audio_stream = self.audio.open(
            format=pyaudio.paInt16,       # 16位整型格式
            channels=1,                   # 单声道
            rate=44100,                   # 采样率44.1kHz（标准音频采样率）
            input=True,                   # 输入设备（麦克风）
            frames_per_buffer=1024        # 每次读取的音频帧数
        )

    async def get_frame(self):
        # 使用线程池执行同步的OpenCV操作，避免阻塞事件循环
        loop = asyncio.get_event_loop()
        ret, frame = await loop.run_in_executor(None, self.cap.read)
        if not ret:
            return None
        # 转换为JPEG字节流（关键修改：将帧编码为适合网络传输的格式）
        _, jpeg = cv.imencode('.jpg', frame)
        return jpeg.tobytes()

    async def get_audio(self):
        """异步获取音频数据（使用线程池避免阻塞事件循环）"""
        loop = asyncio.get_event_loop()
        # 从音频流读取1024帧数据（同步操作，通过线程池异步化）
        audio_data = await loop.run_in_executor(None, self.audio_stream.read, 1024)
        return audio_data

    def release(self):
        self.cap.release()
        # 新增：释放音频资源
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.audio.terminate()

# WebSocket处理函数（关键修复）
async def video_ws(websocket: WebSocket):
    await websocket.accept()
    streamer = VideoStreamer()
    try:
        while True:
            frame_task = streamer.get_frame()
            audio_task = streamer.get_audio()
            frame, audio_data = await asyncio.gather(frame_task, audio_task)

            if not frame:
                break

            await websocket.send_bytes(b'\x00' + frame)
            await websocket.send_bytes(b'\x01' + audio_data)
            await asyncio.sleep(0.01)
    except WebSocketDisconnect:
        pass  # 客户端已主动断开，无需额外操作
    finally:
        streamer.release()
        # 新增：避免重复关闭连接的异常捕获
        try:
            await websocket.close()
        except RuntimeError:
            pass  # 忽略"已发送关闭消息"的异常

# 新增：处理首页的路由函数（关键修改）
async def homepage(request):
    # 自动定位当前脚本同目录下的1.html文件
    html_path = pathlib.Path(__file__).parent / "1.html"
    # 显式指定utf-8编码读取（解决编码错误）
    html_content = html_path.read_text(encoding="utf-8")  # 新增encoding参数
    return HTMLResponse(html_content)

# 路由配置（修改：在构造函数中传入）
routes = [
    Route("/", homepage),  # 新增：访问根路径时返回1.html
    WebSocketRoute('/ws', video_ws),

]
app = Starlette(debug=True, routes=routes)  # 关键修改点

# 启动命令提示（需要通过uvicorn运行）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
