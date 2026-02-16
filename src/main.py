# Autor: Daniel Benjamin Perez Morales
# GitHub: https://github.com/D4nitrix13
# GitLab: https://gitlab.com/D4nitrix13
# Correo electrónico: danielperezdev@proton.me

from typing import Dict, Union
from fastapi import FastAPI

app: FastAPI = FastAPI()


@app.get(path="/")
async def read_root() -> Dict[str, str]:
    return {"Hello": "World"}


@app.get(path="/items/{item_id}")
async def read_item(
    item_id: int, q: Union[str, None] = None
) -> Dict[str, Union[int, str, None]]:
    return {"item_id": item_id, "q": q}
