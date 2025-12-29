"""
Centralized script to execute bash shell
"""

import subprocess
import logging
import json

from app.utils.settings import settings
from app.utils.schema import shell_cmd_output

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

def execute_cmd(cmd) -> shell_cmd_output:
    try:
        response = subprocess.run(cmd, capture_output=True)
        logger.debug(response.stdout.decode("utf-8"))
        logger.debug(response.stderr)
        ret_out = shell_cmd_output(cmd, response.stdout.decode("utf-8")[:-1].split("\n"), response.stderr.decode("utf-8").split("\n"))
    except Exception as e:
        logger.error(f"Exception occurred while executing. Exception is {e}")
        ret_out = shell_cmd_output(cmd, None, e.__str__().split("\n"))
    return ret_out.get_dict()

if __name__ == "__main__":
    response = execute_cmd(["ls"])
    json_response = json.dumps(response, indent=4)
    print(json_response)