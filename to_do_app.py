import tkinter as tk
from tkinter import messagebox
from tkinter import font
import math
import threading
import time

tasks = []

# Animation variables
animation_running = False
glow_intensity = 0
glow_direction = 1

# Core functions with enhanced UX
def add_task():
    task_name = entry_task.get().strip()
    if task_name and task_name != placeholder_text:
        tasks.append({"task": task_name, "done": False})
        
        # Add with animation effect
        listbox.insert(tk.END, f"●  {task_name}")
        entry_task.delete(0, tk.END)
        entry_task.insert(0, placeholder_text)
        entry_task.config(fg='#64748b')
        
        # Flash effect for added task
        flash_add_button()
        update_listbox_colors()
        update_task_counter()
    else:
        shake_entry()

def delete_task():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        # Flash effect before deletion
        flash_delete_button()
        tasks.pop(index)
        listbox.delete(index)
        update_listbox_colors()
        update_task_counter()
    else:
        shake_button(btn_delete)

def mark_done():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        if not tasks[index]["done"]:
            tasks[index]["done"] = True
            listbox.delete(index)
            listbox.insert(index, f"✓  {tasks[index]['task']}")
            flash_done_button()
            update_listbox_colors()
            update_task_counter()
    else:
        shake_button(btn_done)

def update_listbox_colors():
    """Enhanced color update with gradient effects"""
    for i in range(listbox.size()):
        if i < len(tasks) and tasks[i]["done"]:
            listbox.itemconfig(i, {
                'bg': '#065f46', 'fg': '#6ee7b7', 
                'selectbackground': '#064e3b', 'selectforeground': '#a7f3d0'
            })
        else:
            listbox.itemconfig(i, {
                'bg': '#1e293b', 'fg': '#f1f5f9', 
                'selectbackground': '#334155', 'selectforeground': '#7dd3fc'
            })

def update_task_counter():
    """Update task counter display"""
    total = len(tasks)
    completed = sum(1 for task in tasks if task["done"])
    pending = total - completed
    
    if total == 0:
        counter_text = "No tasks yet"
        counter_color = "#64748b"
    elif pending == 0:
        counter_text = f"🎉 All {total} tasks completed!"
        counter_color = "#10b981"
    else:
        counter_text = f"{pending} pending • {completed} completed"
        counter_color = "#7dd3fc"
    
    task_counter.config(text=counter_text, fg=counter_color)

# Animation functions
def flash_add_button():
    original_bg = btn_add.cget("bg")
    btn_add.config(bg="#22c55e")
    root.after(150, lambda: btn_add.config(bg=original_bg))

def flash_delete_button():
    original_bg = btn_delete.cget("bg")
    btn_delete.config(bg="#dc2626")
    root.after(150, lambda: btn_delete.config(bg=original_bg))

def flash_done_button():
    original_bg = btn_done.cget("bg")
    btn_done.config(bg="#0ea5e9")
    root.after(150, lambda: btn_done.config(bg=original_bg))

def shake_entry():
    """Shake animation for entry field"""
    original_x = entry_task.winfo_x()
    def shake_step(step):
        if step < 10:
            offset = 5 if step % 2 == 0 else -5
            entry_task.place(x=original_x + offset, y=entry_task.winfo_y())
            root.after(50, lambda: shake_step(step + 1))
        else:
            entry_task.place(x=original_x, y=entry_task.winfo_y())
    shake_step(0)

def shake_button(button):
    """Shake animation for buttons"""
    original_bg = button.cget("bg")
    button.config(bg="#ef4444")
    root.after(100, lambda: button.config(bg=original_bg))

def create_advanced_gradient(canvas, width, height):
    """Create stunning gradient with multiple colors"""
    for i in range(height):
        ratio = i / height
        
        # Multi-stop gradient: deep blue -> purple -> dark blue
        if ratio < 0.3:
            # Deep blue to purple
            local_ratio = ratio / 0.3
            r = int(15 + (67 - 15) * local_ratio)   # 0f -> 43
            g = int(23 + (56 - 23) * local_ratio)   # 17 -> 38
            b = int(42 + (99 - 42) * local_ratio)   # 2a -> 63
        elif ratio < 0.7:
            # Purple to dark purple
            local_ratio = (ratio - 0.3) / 0.4
            r = int(67 + (88 - 67) * local_ratio)   # 43 -> 58
            g = int(56 + (28 - 56) * local_ratio)   # 38 -> 1c
            b = int(99 + (135 - 99) * local_ratio)  # 63 -> 87
        else:
            # Dark purple to very dark blue
            local_ratio = (ratio - 0.7) / 0.3
            r = int(88 + (30 - 88) * local_ratio)   # 58 -> 1e
            g = int(28 + (41 - 28) * local_ratio)   # 1c -> 29
            b = int(135 + (59 - 135) * local_ratio) # 87 -> 3b
        
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, width, i, fill=color)

def animate_glow():
    """Animated glow effect for the main frame"""
    global glow_intensity, glow_direction, animation_running
    
    if not animation_running:
        return
    
    glow_intensity += glow_direction * 2
    if glow_intensity >= 20 or glow_intensity <= 0:
        glow_direction *= -1
    
    # Update glow effect
    glow_color_intensity = int(100 + glow_intensity * 3)
    glow_color = f'#{min(255, glow_color_intensity):02x}{min(255, int(glow_color_intensity * 0.7)):02x}{min(255, int(glow_color_intensity * 1.2)):02x}'
    
    # Update the shadow frame color for glow effect
    shadow_frame.config(bg=glow_color)
    
    root.after(100, animate_glow)

def on_entry_focus_in(event):
    if entry_task.get() == placeholder_text:
        entry_task.delete(0, tk.END)
        entry_task.config(fg='#f1f5f9')

def on_entry_focus_out(event):
    if not entry_task.get():
        entry_task.insert(0, placeholder_text)
        entry_task.config(fg='#64748b')

def on_hover_enter(button, hover_color):
    button.config(bg=hover_color)

def on_hover_leave(button, normal_color):
    button.config(bg=normal_color)

# Tkinter setup
root = tk.Tk()
root.title("✨ Ultra Modern To-Do App")
root.geometry("750x600")
root.resizable(False, False)
root.configure(bg="#0f172a")

# Create stunning fonts
title_font = font.Font(family="Segoe UI", size=28, weight="bold")
subtitle_font = font.Font(family="Segoe UI", size=12, weight="normal")
button_font = font.Font(family="Segoe UI", size=11, weight="bold")
entry_font = font.Font(family="Segoe UI", size=13)
list_font = font.Font(family="Segoe UI", size=12)
counter_font = font.Font(family="Segoe UI", size=10, weight="bold")

# Advanced gradient background
canvas = tk.Canvas(root, width=750, height=600, highlightthickness=0)
canvas.pack(fill="both", expand=True)
create_advanced_gradient(canvas, 750, 600)

# Animated glow shadow
shadow_frame = tk.Frame(root, bg="#6366f1", bd=0)
shadow_frame.place(relx=0.5, rely=0.5, anchor="center", width=650, height=520)

# Main glassmorphism container
main_frame = tk.Frame(root, bg="#1e293b", bd=0, relief="flat")
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=640, height=510)

# Header section
header_frame = tk.Frame(main_frame, bg="#1e293b")
header_frame.pack(fill="x", pady=(30, 10))

title_label = tk.Label(header_frame, text="✨ TaskFlow Pro", font=title_font, 
                      bg="#1e293b", fg="#ffffff")
title_label.pack()

subtitle_label = tk.Label(header_frame, text="Organize your life with style", font=subtitle_font,
                         bg="#1e293b", fg="#94a3b8")
subtitle_label.pack(pady=(0, 10))

# Task counter
task_counter = tk.Label(header_frame, text="No tasks yet", font=counter_font,
                       bg="#1e293b", fg="#64748b")
task_counter.pack()

# Enhanced input section
input_container = tk.Frame(main_frame, bg="#334155", relief="flat", bd=0)
input_container.pack(pady=20, padx=40, fill="x")

input_frame = tk.Frame(input_container, bg="#334155")
input_frame.pack(pady=15, padx=20)

# Stylish entry with glow effect
placeholder_text = "What's on your mind today?"
entry_task = tk.Entry(input_frame, width=38, font=entry_font, 
                     bg="#475569", fg="#64748b", bd=0, relief="flat",
                     insertbackground="#7dd3fc", insertwidth=3)
entry_task.insert(0, placeholder_text)
entry_task.bind('<FocusIn>', on_entry_focus_in)
entry_task.bind('<FocusOut>', on_entry_focus_out)
entry_task.bind('<Return>', lambda e: add_task())
entry_task.pack(side=tk.LEFT, padx=(0, 15), ipady=12)

# Premium add button
btn_add = tk.Button(input_frame, text="✨ Add Task", font=button_font,
                   command=add_task, bg="#10b981", fg="#ffffff", 
                   bd=0, relief="flat", cursor="hand2",
                   activebackground="#059669", activeforeground="#ffffff")
btn_add.pack(side=tk.LEFT, ipadx=20, ipady=12)

# Hover effects for add button
btn_add.bind("<Enter>", lambda e: on_hover_enter(btn_add, "#059669"))
btn_add.bind("<Leave>", lambda e: on_hover_leave(btn_add, "#10b981"))

# Control buttons with enhanced styling
button_container = tk.Frame(main_frame, bg="#1e293b")
button_container.pack(pady=10)

btn_done = tk.Button(button_container, text="✓ Complete", font=button_font,
                    command=mark_done, bg="#3b82f6", fg="#ffffff",
                    bd=0, relief="flat", cursor="hand2", width=12,
                    activebackground="#2563eb", activeforeground="#ffffff")
btn_done.pack(side=tk.LEFT, padx=8, ipady=8)

btn_delete = tk.Button(button_container, text="🗑 Remove", font=button_font,
                      command=delete_task, bg="#ef4444", fg="#ffffff",
                      bd=0, relief="flat", cursor="hand2", width=12,
                      activebackground="#dc2626", activeforeground="#ffffff")
btn_delete.pack(side=tk.LEFT, padx=8, ipady=8)

# Hover effects
btn_done.bind("<Enter>", lambda e: on_hover_enter(btn_done, "#2563eb"))
btn_done.bind("<Leave>", lambda e: on_hover_leave(btn_done, "#3b82f6"))
btn_delete.bind("<Enter>", lambda e: on_hover_enter(btn_delete, "#dc2626"))
btn_delete.bind("<Leave>", lambda e: on_hover_leave(btn_delete, "#ef4444"))

# Premium task list container
list_container = tk.Frame(main_frame, bg="#0f172a", relief="flat", bd=0)
list_container.pack(pady=20, padx=40, fill="both", expand=True)

# Custom scrollbar
scrollbar = tk.Scrollbar(list_container, bg="#475569", troughcolor="#1e293b",
                        activebackground="#7dd3fc", width=12)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))

# Ultra-modern listbox
listbox = tk.Listbox(list_container, font=list_font, bg="#1e293b", fg="#f1f5f9",
                    bd=0, relief="flat", selectbackground="#334155",
                    selectforeground="#7dd3fc", activestyle="none",
                    yscrollcommand=scrollbar.set, cursor="hand2")
listbox.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)
scrollbar.config(command=listbox.yview)

# Footer with tips
footer_frame = tk.Frame(main_frame, bg="#1e293b")
footer_frame.pack(fill="x", pady=(0, 20))

footer_label = tk.Label(footer_frame, 
                       text="💡 Press Enter to add • Click to select • Double-click for quick actions", 
                       font=("Segoe UI", 9), bg="#1e293b", fg="#64748b")
footer_label.pack()

# Start glow animation
animation_running = True
animate_glow()

# Focus on entry by default
root.after(100, lambda: entry_task.focus())

# Initialize counter
update_task_counter()

root.mainloop()

# Stop animation when closing
animation_running = False
