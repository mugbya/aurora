from sanic import Sanic

from api import bp as user_bp

from config import settings


app = Sanic(__name__)
app.blueprint(user_bp)
app.static('/static', './static')


if __name__=="__name__":
    app.run(host="0.0.0.0", port=settings.PORT, workers=settings.workers, debug=settings.DEBUG)
