from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint
from jsonschema import validate, ValidationError
import json
import uvicorn

from main_app.data_classes.BlackLittermanModelData import BlackLittermanModelData

class ModelEndpoint(HTTPEndpoint):
    async def post(self, request):
        data = await request.json()
        model_name = request.path_params['model_name']

        try:
            import os
            schema_file = os.path.join(
                os.path.dirname(__file__),
                'data_classes',
                'BlackLittermanModelDataSchema.json'
            )
            with open(schema_file, 'r') as file:
                schema = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return JSONResponse({'error': f"Schema error: {str(e)}"}, status_code=500)

        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            return JSONResponse({'error': str(e)}, status_code=400)
        result = run_model(model_name, data)
        return JSONResponse({'result': result})


async def run_model(model_name, payload):
    # Place your model running code here
    if model_name != 'BlackLitterman':
        raise Exception('Only BlackLitterman model is supported at present')

    # model_data = BlackLittermanModelData.from_json(payload)
    # todo: create model, and process

    return """
{
  "Model": "BlackLitterman",
  "ModelResults": [
    {
      "Views": [
        {
          "Weights": [
            { "asset": "stETH", "weight": 1.0 },
            { "asset": "tzBTC", "weight": -1.0 }
          ],
          "Return": 0.0125
        },
        {
          "Weights": [
            { "asset": "USDC", "weight": 1.0 }
          ],
          "Return": 0.03
        }
      ],
      "Allocations": [
        { "asset": "stETH", "weight": 0.5 },
        { "asset": "tzBTC", "weight": 0.2 },
        { "asset": "USDC", "weight": 0.3 }
      ]
    },
    {
      "Views": [
        {
          "Weights": [
            { "asset": "stETH", "weight": 1.0 },
            { "asset": "USDC", "weight": -1.0 }
          ],
          "Return": 0.02
        },
        {
          "Weights": [
            { "asset": "USDC", "weight": 1.0 }
          ],
          "Return": 0.02
        },
        {
          "Weights": [
            { "asset": "tzBTC", "weight": 1.0 }
          ],
          "Return": 0.035
        }
      ],
      "Allocations": [
        { "asset": "stETH", "weight": 0.4 },
        { "asset": "tzBTC", "weight": 0.5 },
        { "asset": "USDC", "weight": 0.1 }
      ]
    }
  ]
}
"""

routes = [
    Route('/run_model/{model_name}', ModelEndpoint),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)