# HedonicGames

## 概要
クールノー競争からなるhedonic gameにおいて、coalition-wise pessimistic coreとpartition-wise pessimistic coreに入るパーティションを探査するプログラムを作成しました。hedonic gameの分析に役立ててほしいですが、あくまでもプログラムによる結果ということで、厳密な証明はされていないことに注意してください。

## 環境のセットアップ
   `requirements.txt`をルートディレクトリに置いているので、以下のコマンドで必要なパッケージをインストールできます。

   ```bash
   pip install -r requirements.txt
   ```

## 各コードの紹介

### `n_k_partition.py`
k人提携とn-k人提携のパーティションがコアかどうかを確認し、結果を出力します。
- CLI出力：output_typeをcliに設定すると、結果がターミナルに表示されます。
- CSV出力：output_typeをcsvに設定すると、./output/n_k_progress_output.csvに結果が出力されます。

以下のコマンドで実行します。

```bash
python n_k_partition.py
```

### `coalition_wise_pessimistic_core.py`
n人集合の分割が、 coalition-wise pessimistic coreに入るかどうかの計算を行い、結果を出力します。
- CLI出力：output_typeをcliに設定すると、結果がターミナルに表示されます。
- CSV出力：output_typeをcsvに設定すると、./output/coalition_wise_pessimistic_core_output.csvに結果が出力されます。

以下のコマンドで実行します。

```bash
python coalition_wise_pessimistic_core.py
```

### `partition_wise_pessimistic_core.py`
n人集合の分割が、 partition-wise pessimistic coreに入るかどうかの計算を行い、結果を出力します。
- CLI出力：output_typeをcliに設定すると、結果がターミナルに表示されます。
- CSV出力：output_typeをcsvに設定すると、./output/partition_wise_pessimistic_core_output.csvに結果が出力されます。

以下のコマンドで実行します。

```bash
python partition_wise_pessimistic_core.py
```
