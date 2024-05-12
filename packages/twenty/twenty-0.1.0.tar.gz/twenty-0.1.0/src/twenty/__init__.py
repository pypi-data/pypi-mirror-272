import time
import tkinter as tk
from multiprocessing import Process

WORK_TIME_MINUTES = 20
REST_TIME_SECONDS = 20


def rest():
    root = tk.Tk()

    root.attributes("-fullscreen", True)

    countdown_label = tk.Label(root, font=("Helvetica", 48))
    countdown_label.pack(expand=True, fill="both")

    countdown_time = REST_TIME_SECONDS

    def update_countdown():
        nonlocal countdown_time

        if countdown_time > 0:
            countdown_label.config(text=f"Time remaining: {countdown_time} seconds")
            countdown_time -= 1
            root.after(1000, update_countdown)
        else:
            print("Time's up!")
            root.quit()

    print("Starting countdown...")
    update_countdown()

    root.mainloop()
    try:
        root.destroy()
    except tk.TclError:
        pass


def main():
    try:
        while True:
            p = Process(target=rest)
            p.start()
            p.join()
            for i in range(WORK_TIME_MINUTES):
                print(f"{WORK_TIME_MINUTES - i} miutes to next break")
                time.sleep(60)
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
