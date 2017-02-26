from sanic import Sanic

from api import bp as user_bp
from db.dao_pg import setup_connection, close_connection
from config import settings

app = Sanic(__name__)
app.blueprint(user_bp)
app.static('/static', './static')


if __name__ == "__main__":
    '''
    sanic 启动时创建数据库连接池，服务正常结束时关闭连接池
    '''
    app.run(host="0.0.0.0", port=settings.PORT, workers=settings.workers, debug=settings.DEBUG,
            after_start=setup_connection, after_stop=close_connection)
