import matplotlib.pyplot as plt
import numpy as np
import bs4
import threading
import time


class WebSite:
    def __init__(self):
        self.figs_graphic = plt.figure()
        self.file_name = 'panel/index.html'

    def drawGraphic(self, data):
        ax = self.figs_graphic.add_subplot(111)
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')
        while True:
            ax.plot(np.linspace(1, 3 * len([float(pair[1]) for pair in data]), len([float(pair[1]) for pair in data])),
                    np.array([float(pair[0]) for pair in data]), c='red', label='Temperature')
            ax.plot(np.linspace(1, 3 * len([float(pair[1]) for pair in data]), len([float(pair[1]) for pair in data])),
                    np.array([float(pair[1]) for pair in data]), c='blue', label='Humidity')

            ax.legend()
            ax.grid()
            self.figs_graphic.savefig('panel/graphic.png', transparent=True)
            ax.clear()
            time.sleep(3)

    def replaceValues(self, data):
        while True:
            if data:
                temp_now, humid_now = data[-1][0], data[-1][1]
                with open(self.file_name) as html_doc:
                    txt = html_doc.read()
                    soup = bs4.BeautifulSoup(txt, features='html.parser')

                new_value = soup.new_tag(name='div', attrs={'class': 'value-temp'})
                new_value.string = f'{temp_now} C'
                for value in soup.findAll('div', {'class': 'value-temp'}):
                    value.replace_with(new_value)

                new_value = soup.new_tag(name='div', attrs={'class': 'value-humid'})
                new_value.string = f'{humid_now} %'
                for value in soup.findAll('div', {'class': 'value-humid'}):
                    value.replace_with(new_value)
                with open(self.file_name, 'w') as html_doc:
                    html_doc.write(str(soup))
                time.sleep(3)

    def start(self, data):
        draw_thread = threading.Thread(target=self.drawGraphic, args=(data,))
        draw_thread.start()

        replacer = threading.Thread(target=self.replaceValues, args=(data,))
        replacer.start()
