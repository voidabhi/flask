from teleflask.server import TeleflaskComplete
from teleflask.messages import TextMessage

from somewhere import API_KEY  # I import it from some file which is kept private, not in git.
# Just set API_KEY = "your-api-key".

app = TeleflaskComplete(__name__, API_KEY)  # instead of writing:  app = Flask(__name__)


@app.route("/")
def index():
    return "This is a normal Flask page."

# Register the /start command
@app.command("start")
def start(update, text):
    return TextMessage("<b>Hello!</b> Thanks for using @" + app.username + "!", parse_mode="html")


# register a function to be called for updates.
@app.on_update
def foo(update):
    from pytgbot.api_types.receivable.updates import Update
    assert isinstance(update, Update)
    if not update.message:
        return
    if update.message.new_chat_member:
        return TextMessage("Welcome!")
