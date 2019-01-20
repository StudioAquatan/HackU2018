# SeeVo
## SeeVoとは
**投票型意見収集&授業分析補助Webアプリ**
名前の由来は、「先生から見えない生徒の声(**vo**ice)を投票(**vo**te)という行為を通して見える(**see**)ようにしよう」というコンセプトから


## 機能
このアプリはSpeaker(先生)機能とListener(生徒)機能から成り立っている

### Speaker
部屋を作成し、Speakerページに遷移することでListenerからの票をほぼリアルタイムで反映されるメーター、コメントを見ることができる．
これらのデータは講義のスライド番号に合わせて記録され，結果ページではこれらの票数の遷移がグラフ化される．

### Listener
わかった、もう知ってる、わからないの三種類の票とコメントの送信をすることができる．

## 実行
### 環境
- python 3.6.x
- pipenv 2018.7.1

### 実行方法
```bash
cd app
# 依存パッケージのインストール
pipenv install
# env_filesディレクトリ内に.envファイルを作成，編集
vi env_files
# マイグレーションを行い実行
pipenv run python manage.py migrate
pipenv run python manage.py runserver
```
`http://127.0.0.1:8000/poll`に接続する