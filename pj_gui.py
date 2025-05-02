import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mov *.avi")])
    if file_path:
        video_path_var.set(file_path)

def run_pipeline():
    video_path = video_path_var.get()
    if not video_path:
        messagebox.showerror("오류", "비디오 파일을 선택하세요.")
        return
    try:
        subprocess.run(["python", "main.py", "--video_path", video_path], check=True)   
        messagebox.showinfo("완료", "✅ 변환이 완료되었습니다!")
    except Exception as e:
        messagebox.showerror("오류", str(e))

# GUI 생성
root = tk.Tk()
root.title("비디오 자막 변환기")

video_path_var = tk.StringVar()

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

tk.Label(frame, text="비디오 파일 선택").pack(anchor="w")
entry = tk.Entry(frame, textvariable=video_path_var, width=50)
entry.pack(side="left", padx=(0, 10))
browse_btn = tk.Button(frame, text="찾아보기", command=browse_file)
browse_btn.pack(side="left")

run_btn = tk.Button(root, text="실행", command=run_pipeline, bg="green", fg="white", height=2, width=20)
run_btn.pack(pady=20)

root.mainloop()
