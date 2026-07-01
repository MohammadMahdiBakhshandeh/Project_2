import sys
import random

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

BASE_GREEN = 5
MAX_GREEN = 25



class Car:

    def __init__(self):

        self.color = random.choice(

            [

                QColor("#ff4444"),

                QColor("#2196F3"),

                QColor("#4CAF50"),

                QColor("#FFC107")

            ]

        )



class TrafficLight:

    def __init__(self):

        self.state = "قرمز"

    def green(self):

        self.state = "سبز"

    def red(self):

        self.state = "قرمز"




class Lane:

    def __init__(self,name):

        self.name = name

        self.cars = []

        self.light = TrafficLight()

    def add_car(self):

        self.cars.append(Car())

    def remove_car(self):

        if self.cars:

            self.cars.pop(0)

    def count(self):

        return len(self.cars)




class Intersection:

    def __init__(self):

        self.lanes = {

            "شمال":Lane("شمال"),

            "جنوب":Lane("جنوب"),

            "شرق":Lane("شرق"),

            "غرب":Lane("غرب")

        }




class Controller:

    def __init__(self,intersection):

        self.intersection = intersection

        self.current = None

        self.timer = 0

    def adaptive(self,lane):

        return min(

            MAX_GREEN,

            BASE_GREEN +

            lane.count()*2

        )

    def select_lane(self):

        return max(

            self.intersection.lanes.values(),

            key=lambda x:x.count()

        )

    def switch(self):

        for lane in self.intersection.lanes.values():

            lane.light.red()

        lane = self.select_lane()

        lane.light.green()

        self.current = lane

        self.timer = self.adaptive(lane)

    def update(self):

        if self.current is None:

            self.switch()

            return

        self.timer -= 1

        if self.current.count():

            self.current.remove_car()

        if self.timer <= 0:

            self.switch()




class RoadWidget(QWidget):

    def __init__(self,intersection):

        super().__init__()

        self.intersection = intersection

        self.setMinimumSize(

            800,

            800

        )

    def paintEvent(self,event):

        p = QPainter(self)

        p.setRenderHint(

            QPainter.Antialiasing

        )

        w = self.width()

        h = self.height()

        center = w//2

        road = 170

        p.fillRect(

            self.rect(),

            QColor(

                "#4CAF50"

            )

        )

        p.fillRect(

            center-road//2,

            0,

            road,

            h,

            QColor(

                "#424242"

            )

        )

        p.fillRect(

            0,

            center-road//2,

            w,

            road,

            QColor(

                "#424242"

            )

        )

        p.setPen(

            QPen(

                Qt.white,

                3

            )

        )

        p.drawLine(

            center,

            0,

            center,

            h

        )

        p.drawLine(

            0,

            center,

            w,

            center

        )

        self.draw_cars(p)

        self.draw_lights(p)

    def draw_lights(self,p):

        lanes = self.intersection.lanes

        data = [

            ("شمال",390,250),

            ("جنوب",390,520),

            ("شرق",520,390),

            ("غرب",250,390)

        ]

        for name,x,y in data:

            state = lanes[name].light.state

            color = QColor("red")

            if state == "سبز":

                color = QColor("lime")

            p.setBrush(color)

            p.drawEllipse(

                x,

                y,

                25,

                25

            )

    def draw_cars(self,p):

        lanes = self.intersection.lanes

        for i,c in enumerate(

                lanes["شمال"].cars):

            p.setBrush(c.color)

            p.drawRect(

                360,

                70+i*35,

                30,

                20

            )

        for i,c in enumerate(

                lanes["جنوب"].cars):

            p.setBrush(c.color)

            p.drawRect(

                410,

                690-i*35,

                30,

                20

            )

        for i,c in enumerate(

                lanes["شرق"].cars):

            p.setBrush(c.color)

            p.drawRect(

                690-i*35,

                410,

                20,

                30

            )

        for i,c in enumerate(

                lanes["غرب"].cars):

            p.setBrush(c.color)

            p.drawRect(

                70+i*35,

                360,

                20,

                30

            )



class Window(QWidget):

    def __init__(self):

        super().__init__()

        self.intersection = Intersection()

        self.controller = Controller(

            self.intersection

        )

        self.build()

        self.timer = QTimer()

        self.timer.timeout.connect(

            self.loop

        )

        self.timer.start(1000)

    def build(self):

        self.resize(

            1200,

            850

        )

        self.setWindowTitle(

            "چهارراه هوشمند"

        )

        layout = QHBoxLayout()

        self.road = RoadWidget(

            self.intersection

        )

        panel = QVBoxLayout()

        self.info = QLabel()

        panel.addWidget(

            self.info

        )

        for n in [

            "شمال",

            "جنوب",

            "شرق",

            "غرب"

        ]:

            b = QPushButton(

                f"ورود خودرو {n}"

            )

            b.clicked.connect(

                lambda c,d=n:

                self.add_car(d)

            )

            panel.addWidget(b)

        panel.addStretch()

        layout.addWidget(

            self.road,

            3

        )

        layout.addLayout(

            panel,

            1

        )

        self.setLayout(layout)

    def add_car(self,name):

        self.intersection.lanes[

            name

        ].add_car()

        self.refresh()

    def loop(self):

        if random.random()<0.35:

            direction = random.choice(

                [

                    "شمال",

                    "جنوب",

                    "شرق",

                    "غرب"

                ]

            )

            self.intersection.lanes[

                direction

            ].add_car()

        self.controller.update()

        self.refresh()

    def refresh(self):

        current = ""

        if self.controller.current:

            current = self.controller.current.name

        txt = f"""



{current}



{self.controller.timer}



{self.intersection.lanes['شمال'].count()}


{self.intersection.lanes['جنوب'].count()}


{self.intersection.lanes['شرق'].count()}



{self.intersection.lanes['غرب'].count()}

"""

        self.info.setText(txt)

        self.road.update()




app = QApplication(sys.argv)

w = Window()

w.show()

sys.exit(app.exec_())