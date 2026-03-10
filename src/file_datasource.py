from csv import reader
from datetime import datetime
from domain.aggregated_data import AggregatedData
from domain.accelerometer import Accelerometer
from domain.gps import Gps


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str) -> None:
        self.acc_file = accelerometer_filename
        self.gps_file = gps_filename

        self.acc_reader = None
        self.gps_reader = None

        self.acc_file_obj = None
        self.gps_file_obj = None

    def startReading(self, *args, **kwargs):
        self.acc_file_obj = open(self.acc_file)
        self.gps_file_obj = open(self.gps_file)

        self.acc_reader = reader(self.acc_file_obj)
        self.gps_reader = reader(self.gps_file_obj)

    def stopReading(self, *args, **kwargs):
        if self.acc_file_obj:
            self.acc_file_obj.close()

        if self.gps_file_obj:
            self.gps_file_obj.close()

    def read(self) -> AggregatedData:
        acc_row = next(self.acc_reader)
        gps_row = next(self.gps_reader)

        accelerometer = Accelerometer(
            x=int(acc_row[0]),
            y=int(acc_row[1]),
            z=int(acc_row[2])
        )

        gps = Gps(
            longitude=float(gps_row[0]),
            latitude=float(gps_row[1])
        )

        return AggregatedData(
            accelerometer=accelerometer,
            gps=gps,
            time=datetime.now()
        )