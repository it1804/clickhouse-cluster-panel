#!/bin/bash
set -e

flask db init || flask db migrate && flask db upgrade

exec "$@"
