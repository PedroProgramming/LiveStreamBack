from ninja import NinjaAPI
from users.api import user_router
from channel.api import channel_router
from LiveStream.api import stream_router
from authentication.api import auth_router
from scalar_django_ninja import ScalarViewer

# Instance api
api = NinjaAPI()


# Routes for each application
api.add_router("/auth", auth_router)
api.add_router("/user", user_router)
api.add_router("/live", stream_router)
api.add_router("/channel", channel_router)
