import pandas as pd
from ipyleaflet import Map, Marker, Polygon, FullScreenControl, LegendControl
from ipywidgets import Layout

class MapRenderer:
    def __init__(self, district_data: pd.DataFrame, points_data: pd.DataFrame):
        self.__points_data = points_data
        self.__district_data = district_data

    def get_map(self) -> Map:
        """
        Создает карту Казани с выделенными районами.
        """
        # Центр карты - медиана координат
        center_lat = self.__district_data['center'].apply(lambda x: x[0]).median()
        center_lon = self.__district_data['center'].apply(lambda x: x[1]).median()

        # Создание карты
        m = Map(center=(center_lat, center_lon), zoom=11, layout=Layout(width='100%', height='800px'))

        # Создание легенды
        legend_items = [(district, color) for district, color in zip(self.__district_data['district'], self.__district_data['color'])]
        legend = LegendControl(name="Районы", positions=['bottomright'],  legend_items=legend_items)
        m.add_control(legend)

        # Добавление полигонов районов
        for index, row in self.__district_data.iterrows():
            polygon = Polygon(
                locations=row['points'],
                color=row['color'],
                fill_color=row['color'],
                fill_opacity=0.3,
            )
            m.add_layer(polygon)

            # Добавление маркера в центре района
            marker = Marker(
                location=row['center'],
                draggable=False,
                title=row['district']
            )
            m.add_layer(marker)

        # Добавление полноэкранного режима
        m.add_control(FullScreenControl())
        return m
