import pandas as pd
import geopandas as gpd
import pyarrow as pa

# FlatGeobufファイルをGeoPandasのGeoDataFrameに読み込み
gdf = gpd.read_file('MS_BuildingFootprints_Ukraine.fgb')

# GeoPandasのGeoDataFrameをPandasのDataFrameに変換
df = pd.DataFrame(gdf)

# DataFrameをPyArrowのTableに変換
table = pa.Table.from_pandas(df)

# PyArrowを使用してParquetファイルに書き出し
pa.parquet.write_table(table, 'MS_BuildingFootprints_Ukraine.parquet')
