from typer import Typer
import uvicorn

from app.config import UvicornSettings
from app.containers import Container


app = Typer()

@app.command()
def runserver() -> None:
    uvicorn_settings = UvicornSettings()
    uvicorn.run(**uvicorn_settings.dict())


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])

    app()