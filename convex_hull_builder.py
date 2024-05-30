import pandas as pd
from shapely.geometry import Polygon, Point
from shapely.ops import cascaded_union

class ConvexHullBuilder:
    def __init__(self, points: pd.DataFrame):
        self.__points = points

    def get_convex_hull(self) -> pd.DataFrame:
        """
        Формат выходного датафрейма:
        - district
            Название района
        - points
            Список точек выпуклой оболочки района
        - center
            Кортеж центра района (lat, lon)
        - color
            Цвет оболочки района
        """
        result = []
        for district, group in self.__points.groupby('district'):
            # Преобразование координат в объекты Point
            polygon_points = [Point(row['lon'], row['lat']) for _, row in group.iterrows()]

            # Создание выпуклой оболочки из точек
            convex_hull = Polygon(polygon_points).convex_hull

            # Получение координат вершин выпуклой оболочки
            hull_points = [(point.y, point.x) for point in convex_hull.exterior.coords[:-1]]

            # Вычисление центра района
            center = convex_hull.centroid

            # Добавление информации о районе в список
            result.append({
                'district': district,
                'points': hull_points,
                'center': (center.y, center.x),
                'color': None  # Добавьте логику для назначения цветов
            })

        return pd.DataFrame(result)

# Обработка данных из таблицы
data = """
district | lat | lon
Советский р-н | 55.81157471 | 49.2607765
Ново-Савиновский р-н | 55.83168526 | 49.15672808
Приволжский р-н | 55.71752257 | 49.1222817
Кировский р-н | 55.79157857 | 49.05581216
Московский р-н | 55.81703343 | 49.09114806
Авиастроительный р-н | 55.84475643 | 49.0878232
Вахитовский р-н | 55.75989995 | 49.08043905
Верхнеуслонский р-н | 55.75396248 | 48.99221216
"""

# Разделение данных на строки
lines = data.strip().splitlines()

# Создание списка словарей для DataFrame
rows = []
for line in lines:
    district, lat, lon = line.split('|')
    rows.append({'district': district.strip(), 'lat': float(lat.strip()), 'lon': float(lon.strip())})

# Создание DataFrame
points_df = pd.DataFrame(rows)

# Создание экземпляра ConvexHullBuilder и получение выпуклых оболочек
builder = ConvexHullBuilder(points_df)
convex_hull_df = builder.get_convex_hull()

# Добавление цвета (пока просто случайным образом)
import random
colors = ['green', 'blue', 'yellow', 'red', 'pink', 'white', 'black', 'brown']
convex_hull_df['color'] = [random.choice(colors) for _ in range(len(convex_hull_df))]

print(convex_hull_df)

