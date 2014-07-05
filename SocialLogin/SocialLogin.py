from flask import Flask, render_template, request, make_response,redirect,url_for
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic,exceptions

from config import CONFIG

authomatic = Authomatic(CONFIG, 'your secret string', report_errors=False)

app = Flask(__name__)
app.config.from_pyfile('sociallogin.cfg')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/<provider_name>', methods=['GET', 'POST'])
@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    """
    Login handler, must accept both GET and POST to be able to use OpenID.
    """

    try:

        # We need response object for the WerkzeugAdapter.
        response = make_response()

        # Log the user in, pass it the adapter and the provider name.
        result = authomatic.login(WerkzeugAdapter(request, response), provider_name)

        # If there is no LoginResult object, the login procedure is still pending.
        if result:
            if result.user:
                # We need to update the user to get more info.
                result.user.update()

            # The rest happens inside the template.
            return render_template('login.html', result=result)
    except exceptions.CancellationError as e:
        return redirect(url_for('index'))
    # Don't forget to return the response.
    return response


if __name__ == '__main__':
    app.run()
