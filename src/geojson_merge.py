import glob
import geopandas as gpd
import pandas as pd

# GeoJSONファイルのリストを作成
files = glob.glob('./UnitedStates/*.geojson')

gdfs = []

# 各ファイルをGeoDataFrameに変換し、リストに追加
for file in files:
    print(f"Processing file: {file}")
    gdf = gpd.read_file(file)
    gdfs.append(gdf)

# 全てのGeoDataFrameをマージ
merged_gdf = gpd.GeoDataFrame(pd.concat(gdfs))

# マージしたデータを新しいgeojsonファイルに書き出す
merged_gdf.to_file("MS_BuildingFootprints_UnitedStates.geojson", driver='GeoJSON')

print("処理終了")
