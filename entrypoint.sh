#!/bin/sh
# entrypoint.sh

alembic upgrade head

python -m typer app.main run start-server --app