import tkinter as tk
import cv2
from PIL import Image, ImageTk

window_width=960
window_height=720
video_name = '鹅飞鹤舞，苦尽甘来.mp4'

#图像转换，用于在画布中显示
def tkImage(vc):
    ref,frame = vc.read()
    cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(cvimage)
    pilImage = pilImage.resize((window_width, window_height),Image.ANTIALIAS)
    tkImage =  ImageTk.PhotoImage(image=pilImage)
    return tkImage

#图像的显示与更新
def video(video_name):
    def video_loop():
       try:
            while True:
                picture1=tkImage(vc)
                canvas.create_image(0,0,anchor='nw',image=picture1)
                win.update_idletasks()  #最重要的更新是靠这两句来实现
                win.update()
       except:
            pass
    
    vc = cv2.VideoCapture(video_name)  #读取视频
    video_loop()
    win.mainloop()
    vc.release()
    cv2.destroyAllWindows()


if __name__ == '__main__': 
    '''布局'''
    win = tk.Tk()
    win.geometry(str(window_width)+'x'+str(window_height))
    canvas = tk.Canvas(win, bg='white', width=window_width, height=window_height)
    canvas.place(x=0, y=0)

    video(video_name)