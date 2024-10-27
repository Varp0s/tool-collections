import speedtest
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import FancyArrow

current_download_speed = 0
current_upload_speed = 0

def run_speedtest():
    global target_download_speed, target_upload_speed
    st = speedtest.Speedtest()
    download = st.download()
    target_download_speed = round(download / 10**6, 2)
    upload = st.upload()
    target_upload_speed = round(upload / 10**6, 2)
    
    animate_gauges() 
    result_label.config(text=f"Download Speed: {target_download_speed} Mbps") 
    result_label2.config(text=f"Upload Speed: {target_upload_speed} Mbps")

def animate_gauges():
    global current_download_speed, current_upload_speed
    if current_download_speed < target_download_speed:
        current_download_speed += 0.5 
    if current_upload_speed < target_upload_speed:
        current_upload_speed += 0.5 

    update_gauge(current_download_speed, ax_download, is_download=True)
    update_gauge(current_upload_speed, ax_upload, is_download=False)
    
    if current_download_speed < target_download_speed or current_upload_speed < target_upload_speed:
        root.after(50, animate_gauges)
    else:
        current_download_speed = target_download_speed
        current_upload_speed = target_upload_speed

def update_gauge(speed, ax, is_download=True):
    ax.clear()

    ax.set_facecolor('#444444') 

    num_colors = 100
    cmap = plt.get_cmap('cool')
    colors = cmap(np.linspace(0, 1, num_colors))
    norm = plt.Normalize(0, 100)

    ax.bar(np.linspace(0, np.pi, num_colors), 1, width=0.03, color=colors, edgecolor='white')

    ax.set_xticks(np.linspace(0, np.pi, 5)) 
    ax.set_xticklabels(['0', '25', '50', '75', '100'], fontsize=12, fontweight='bold', color='white')

    angle = np.pi * (speed / 100)
    arrow = FancyArrow(0, 0, np.cos(angle) * 1.2, np.sin(angle) * 1.2,
                       width=0.1, length_includes_head=True, color='yellow')  
    ax.add_patch(arrow)

    ax.set_ylim(0, 1.3)
    
    ax.set_yticklabels([])
    ax.set_yticks([])
    ax.spines['polar'].set_visible(False)
    ax.grid(False)

    speed_text = f"{speed:.2f} Mbps"
    ax.text(-0.2, -0.9, speed_text, ha='center', va='center', fontsize=16, color='cyan', fontweight='bold')  

    canvas.draw()

def main():
    global ax_download, ax_upload, canvas, result_label, result_label2, root

    root = tk.Tk()
    root.title("Speedtest")
    root.geometry("800x600")
    root.config(bg="#333333") 

    fig, (ax_download, ax_upload) = plt.subplots(1, 2, subplot_kw={'projection': 'polar'}, figsize=(10, 4), facecolor='#333333')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(pady=20)

    update_gauge(0, ax_download, is_download=True)  
    update_gauge(0, ax_upload, is_download=False)  
    button = ttk.Button(root, text="Run Speedtest", command=run_speedtest)
    button.pack(pady=20)

    result_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#333333", fg="white")
    result_label.pack(pady=10)

    result_label2 = tk.Label(root, text="", font=("Helvetica", 14), bg="#333333", fg="white")
    result_label2.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
