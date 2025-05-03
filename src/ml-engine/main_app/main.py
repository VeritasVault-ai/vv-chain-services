from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint
import uvicorn
import json


class ModelEndpoint(HTTPEndpoint):
    async def post(self, request):
        data = await request.json()
        model_name = request.path_params['model_name']

        result = run_model(model_name, data)
        return JSONResponse({'result': result})


async def run_model(model_name, payload):
    # Place your model running code here
    data = json.loads(payload)
    print(data)


routes = [
    Route('/run_model/{model_name}', ModelEndpoint),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)