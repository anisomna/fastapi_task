#!/bin/sh

alembic upgrade head
python -m fastapi run src/main.py --host 0.0.0.0
