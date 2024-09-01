import tkinter as tk
from tkinter import ttk
from gemini_api_module import fetch_mitigation_from_gemini

def show_popup(summary):
    window = tk.Tk()
    window.title("Notifikasi Alert")
    window.geometry("900x600")
    window.configure(bg="#f0f0f0")

    total_alerts = summary.get("total", 0)
    rule_details = summary.get("rules", {})

    header = tk.Label(window, text=f"Jumlah Rule Terpicu: {total_alerts}", font=('Helvetica', 14, 'bold'), bg="#f0f0f0")
    header.pack(pady=10)

    canvas = tk.Canvas(window, bg="#ffffff")
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#ffffff")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    def toggle_details(rule_name):
        if rule_name in details_frames:
            detail_frame = details_frames[rule_name]
            if detail_frame.winfo_ismapped():
                detail_frame.pack_forget()
                toggle_buttons.get(rule_name, tk.Button()).config(text="Detail")
            else:
                detail_frame.pack(fill=tk.X, padx=10, pady=5)
                toggle_buttons.get(rule_name, tk.Button()).config(text="Tutup")

    toggle_buttons = {}
    details_frames = {}

    for rule_name, details in rule_details.items():
        rule_frame = tk.Frame(scrollable_frame, bg="#ffffff", bd=1, relief=tk.RAISED)
        rule_frame.pack(pady=5, padx=10, fill=tk.X)

        rule_label = tk.Label(rule_frame, text=rule_name, font=('Helvetica', 12, 'bold'), bg="#ffffff")
        rule_label.pack(side=tk.LEFT, padx=5)

        toggle_button = tk.Button(rule_frame, text="Detail", command=lambda r=rule_name: toggle_details(r))
        toggle_button.pack(side=tk.RIGHT)
        toggle_buttons[rule_name] = toggle_button  # Simpan tombol di dictionary

        detail_frame = tk.Frame(scrollable_frame, bg="#ffffff")
        detail_frame.pack(pady=5, padx=10, fill=tk.X)
        detail_frame.pack_forget()  # Hide initially
        details_frames[rule_name] = detail_frame

        ids_and_ips = []
        for detail in details:
            doc_id = detail['id']
            ip = detail.get('ip', 'No IP')
            ids_and_ips.append(f"ID: {doc_id}\nIP: {ip}")

        # Fetch mitigation details for the rule
        mitigation = fetch_mitigation_from_gemini(rule_name)
        detail_text = "\n".join(ids_and_ips) + f"\n\nDetails:\n{mitigation}\n"
        detail_label = tk.Label(detail_frame, text=detail_text, justify=tk.LEFT, bg="#ffffff", wraplength=850)
        detail_label.pack(anchor="w")

    window.mainloop()
