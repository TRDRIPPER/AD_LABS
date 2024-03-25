from spyre import server
import pandas as pd
import matplotlib.pyplot as plt
from cl import clean, nwid
from down import Downloads

DirPath = "./csv_data"

class StockExample(server.App):
    title = "NOAA data dropdown"

    inputs = [
        {
            "type": "dropdown",
            "label": "Оберіть тип індексу для графіку",
            "options": [
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VHI", "value": "VHI"}
            ],
            "key": "data_type",
            "action_id": "update_data"
        },
        {
            "type": "dropdown",
            "label": "Оберіть область України:",
            "options": [
                {"label": "Вінницька", "value": "1"},
                {"label": "Волинська", "value": "2"},
                {"label": "Дніпропетровська", "value": "3"},
                {"label": "Донецька", "value": "4"},
                {"label": "Житомирська", "value": "5"},
                {"label": "Закарпатська", "value": "6"},
                {"label": "Запорізька", "value": "7"},
                {"label": "Івано-Франківська", "value": "8"},
                {"label": "Київська", "value": "9"},
                {"label": "Кіровоградська", "value": "10"},
                {"label": "Луганська", "value": "11"},
                {"label": "Львівська", "value": "12"},
                {"label": "Миколаївська", "value": "13"},
                {"label": "Одеська", "value": "14"},
                {"label": "Полтавська", "value": "15"},
                {"label": "Рівенська", "value": "16"},
                {"label": "Сумська", "value": "17"},
                {"label": "Тернопільська", "value": "18"},
                {"label": "Харківська", "value": "19"},
                {"label": "Херсонська", "value": "20"},
                {"label": "Хмельницька", "value": "21"},
                {"label": "Черкаська", "value": "22"},
                {"label": "Чернівецька", "value": "23"},
                {"label": "Чернігівська", "value": "24"},
                {"label": "Крим", "value": "25"}
            ],
            "key": "province",
            "action_id": "update_data"
        },
        {
            "type": "text",
            "label": "Оберіть інтервал тижнів:",
            "key": "weeks",
            "value": "1-10",
            "action_id": "update_data"
        },
        {
            "type": "text",
            "label": "Введіть інтервал років (наприклад, 1981-2024):",
            "key": "year_interval",
            "value": "1981-2024",
            "action_id": "update_data"
        }
    ]

    controls = [{"type": "hidden", "id": "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"
        },
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]

    def getData(self, params):
        province = params['province']
        weeks = params['weeks']
        year_interval = params['year_interval']
        data_type = params['data_type']
        
        try:
            df = nwid(clean(DirPath))
            df = df[df['ID'] == int(province)]
            start_week, end_week = map(int, weeks.split('-'))
            start_year, end_year = map(int, year_interval.split('-'))
            df = df[(df['week'] >= start_week) & (df['week'] <= end_week) & (df['year'] >= start_year) & (df['year'] <= end_year)]
            return df[['year', 'week', data_type]]
        except Exception as e:
            print("Error occurred while getting data:", str(e))
            return pd.DataFrame()  

    def getPlot(self, params):
        try:
            df = self.getData(params)
            data_type = params['data_type']
            start_week, end_week = map(int, params['weeks'].split('-'))
            start_year, end_year = map(int, params['year_interval'].split('-'))
            fig, ax = plt.subplots(figsize=(10, 6))
            for year in range(start_year, end_year + 1):
                df_year = df[(df['year'] == year) & (df['week'] >= start_week) & (df['week'] <= end_week)]
                if not df_year.empty:
                    ax.plot(df_year['week'], df_year[data_type], label=str(year))
            ax.set_xlabel('Week')
            ax.set_ylabel(data_type)
            ax.legend(title='Year', loc='center left', bbox_to_anchor=(1, 0.5))
            return fig
        except Exception as e:
            print("Error occurred while plotting:", str(e))
            return plt.figure()

    def getCustomCSS(self):
        css = "table {margin-left: 50px;}"  
        return css

if __name__ == "__main__":
    #Downloads()
    app = StockExample()
    app.launch(port=8081)
