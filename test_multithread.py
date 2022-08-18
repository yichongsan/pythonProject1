import UI, UI_realtime, utils
import threading
import serial



class thread_UI(threading.Thread):
    def run(self):
        UI.main()


class thread_OpenCom(threading.Thread):
    def run(self):
        global ser
        global ser1
        try:
            ser = serial.Serial('COM5', 9600, timeout=0.5)
            ser1 = serial.Serial('COM7', 9600, timeout=0.5, parity='E', bytesize=7, stopbits=1)
        except Exception as e:
            print(e)
            return False

        if ser.isOpen() and ser1.isOpen():
            print("Open Successful")
            return True


def test():
    thread = thread_OpenCom()
    thread.start()


threadLock = threading.Lock()
if __name__ == '__main__':
    for i in range(5):
        test()


