import sys
import threading

from absl import flags

from mesop.colab import colab_utils
from mesop.runtime import enable_debug_mode
from mesop.server.constants import EDITOR_PACKAGE_PATH, PROD_PACKAGE_PATH
from mesop.server.logging import log_startup
from mesop.server.server import configure_flask_app
from mesop.server.static_file_serving import configure_static_file_serving


def colab_run(*, port: int = 32123, prod_mode: bool = False):
  """
  When running in Colab environment, this will launch the web server.

  Otherwise, this is a no-op.
  """
  if not colab_utils.is_running_in_colab():
    print("Not running Colab: `colab_run` is a no-op")
    return
  # Parse the flags before creating the app otherwise you will
  # get UnparsedFlagAccessError.
  #
  # This currently parses a list without any flags because typically Mesop
  # will be run with gunicorn as a WSGI app and there may be unexpected
  # flags such as "--bind".
  #
  # Example:
  # $ gunicorn --bind :8080 main:me
  #
  # We will ignore all CLI flags, but we could provide a way to override
  # Mesop defined flags in the future (e.g. enable_component_tree_diffs)
  # if necessary.
  #
  # Note: absl-py requires the first arg (program name), and will raise an error
  # if we pass an empty list.
  flags.FLAGS(sys.argv[:1])
  flask_app = configure_flask_app(prod_mode=prod_mode)
  if not prod_mode:
    enable_debug_mode()

  configure_static_file_serving(
    flask_app,
    static_file_runfiles_base=PROD_PACKAGE_PATH
    if prod_mode
    else EDITOR_PACKAGE_PATH,
  )

  log_startup(port=port)

  def run_flask_app():
    flask_app.run(host="::", port=port, use_reloader=False)

  # Launch Flask in background thread so we don't hog up the main thread
  # for regular Colab usage.
  threading.Thread(target=run_flask_app).start()
