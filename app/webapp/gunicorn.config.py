# Listenするアドレス
bind = '0.0.0.0:8000'

# ワーカーの数
workers = 4

# 処理がタイムアウトしたらワーカーを再起動
timeout = 30

# Dockerコンテナにするのでデーモンにしない
daemon = False

# pidファイルの場所
pidfile = '/tmp/sanple-app.pid'