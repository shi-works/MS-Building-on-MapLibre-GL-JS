import pandas as pd
import json
import os
import gzip
import urllib.request


def convert_geojsonl_to_geojson(geojsonl_url, output_file):
    # GeoJSONLファイルをダウンロード
    with urllib.request.urlopen(geojsonl_url) as response:
        geojsonl_data = gzip.decompress(response.read()).decode()

    # 各行を個別のjsonオブジェクトとして読み込む
    json_objects = [json.loads(line) for line in geojsonl_data.splitlines()]

    # geojson形式のファイルに書き込む
    with open(output_file, 'w') as outfile:
        # ファイルのヘッダーに追加する情報を設定
        header = {
            "type": "FeatureCollection",
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            },
            "features": []
        }

        # json_objectsをheaderの"features"リストに追加
        header["features"] = json_objects

        # header（featuresを含む）をjsonとしてoutfileに書き込む
        json.dump(header, outfile)


def main():
    # 出力したい地域の名前を設定
    location = 'Ukraine'
    # 出力ディレクトリのパスを設定
    output_directory = os.path.join(os.getcwd(), location)
    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # データセットのリンクをCSVファイルから読み込み
    dataset_links = pd.read_csv(
        "https://minedbuildings.blob.core.windows.net/global-buildings/dataset-links.csv")
    # 選択した地域のリンクのみを取得
    location_links = dataset_links[dataset_links.Location == location]
    # 総ファイル数を取得
    total_files = len(location_links)
    # 各リンクに対して処理を実行
    for i, (_, row) in enumerate(location_links.iterrows(), start=1):
        # 出力ファイルのパスを設定
        file_path = os.path.join(output_directory, f"{row.QuadKey}.geojson")
        print(f"Processing file {i} of {total_files}: {file_path}")
        # GeoJSONLをGeoJSONに変換し、ファイルに書き込む
        convert_geojsonl_to_geojson(row.Url, file_path)


if __name__ == "__main__":
    main()
