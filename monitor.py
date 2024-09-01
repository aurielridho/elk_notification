#!/usr/bin/env python3

import threading
import time
from elasticsearch_module import check_alerts
from gui_module import show_popup

def monitor_alerts():
    global running
    running = True
    while running:
        try:
            rule_details = check_alerts()
            if rule_details:
                rule_summary = {
                    "total": sum(len(details) for details in rule_details.values()),
                    "rules": rule_details
                }
                threading.Thread(target=show_popup, args=(rule_summary,), daemon=True).start()
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(60)

if __name__ == "__main__":
    monitor_alerts()
