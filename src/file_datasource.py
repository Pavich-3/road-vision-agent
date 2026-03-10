from csv import reader
from datetime import datetime
from domain.aggregated_data import AggregatedData
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.acc_file = accelerometer_filename
        self.gps_file = gps_filename
        self.parking_file = parking_filename

        self.acc_reader = None
        self.gps_reader = None
        self.parking_reader = None

        self.acc_file_obj = None
        self.gps_file_obj = None
        self.parking_file_obj = None

    def startReading(self, *args, **kwargs):
        self.acc_file_obj = open(self.acc_file)
        self.gps_file_obj = open(self.gps_file)
        self.parking_file_obj = open(self.parking_file)

        self.acc_reader = reader(self.acc_file_obj)
        self.gps_reader = reader(self.gps_file_obj)
        self.parking_reader = reader(self.parking_file_obj)

        next(self.acc_reader, None)
        next(self.gps_reader, None)
        next(self.parking_reader, None)

    def stopReading(self, *args, **kwargs):
        if self.acc_file_obj:
            self.acc_file_obj.close()
            self.acc_file_obj = None

        if self.gps_file_obj:
            self.gps_file_obj.close()
            self.gps_file_obj = None

        if self.parking_file_obj:
            self.parking_file_obj.close()
            self.parking_file_obj = None

    def _restart_acc_reader(self):
        self.acc_file_obj.seek(0)
        self.acc_reader = reader(self.acc_file_obj)
        next(self.acc_reader, None)

    def _restart_gps_reader(self):
        self.gps_file_obj.seek(0)
        self.gps_reader = reader(self.gps_file_obj)
        next(self.gps_reader, None)

    def _restart_parking_reader(self):
        self.parking_file_obj.seek(0)
        self.parking_reader = reader(self.parking_file_obj)
        next(self.parking_reader, None)

    def read(self) -> AggregatedData:
        try:
            acc_row = next(self.acc_reader)
        except StopIteration:
            self._restart_acc_reader()
            acc_row = next(self.acc_reader)

        try:
            gps_row = next(self.gps_reader)
        except StopIteration:
            self._restart_gps_reader()
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

    def read_parking(self) -> Parking:
        try:
            parking_row = next(self.parking_reader)
        except StopIteration:
            self._restart_parking_reader()
            parking_row = next(self.parking_reader)

        return Parking(
            empty_count=int(parking_row[0]),
            gps=Gps(
                longitude=float(parking_row[1]),
                latitude=float(parking_row[2])
            )
        )