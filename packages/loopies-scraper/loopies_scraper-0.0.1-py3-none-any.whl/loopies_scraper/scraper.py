#!/usr/bin/python
from webdriver_controller import WebDriverController
from data_manager import DataManager, QueueStatus

class Scraper(WebDriverController):
    def process_list(self, data_manager: DataManager):
        with data_manager.lock:
            data_manager.queue_status.value = QueueStatus.STARTED.value

        # Your code here

        with data_manager.lock:
            data_manager.queue_status.value = QueueStatus.DONE.value

    def process_page(self):
        pass

def main():
    pass

if __name__ == "__main__":
    main()