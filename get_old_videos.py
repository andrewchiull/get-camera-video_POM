from datetime import datetime, timedelta
import logging

from main import Main

def main(days_before):
    date = datetime(year=2021, month=9, day=25) - timedelta(days=days_before)
    Yunlin = Main(date=date, location='Yunlin')
    Yunlin.main()
    Yunlin.driver.quit()

    Chiayi = Main(date=date, location='Chiayi')
    Chiayi.main()
    Chiayi.driver.quit()

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)s | %(message)s',
        level=logging.INFO
    )

    for i in range(2, 29):
        main(days_before=i)