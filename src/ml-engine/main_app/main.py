from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint
from jsonschema import validate, ValidationError
from main_app.models.BlackLittermanYieldModel import BlackLittermanYieldModel
from main_app.data_classes.BlackLittermanModelData import BlackLittermanModelData
import json
import uvicorn



class ModelEndpoint(HTTPEndpoint):
    async def post(self, request):
        data = await request.json()
        model_name = request.path_params['model_name']

        schema_file = 'data_classes/BlackLittermanModelDataSchema.json'
        with open(schema_file, 'r') as file:
            schema = json.load(file)
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

    # Build model and calculate
    try:
        model_data = BlackLittermanModelData.from_json(payload)
        model = BlackLittermanYieldModel(model_data=model_data)
        results = model.calculate()
        
        return json.dumps(results)
    except Exception as e:
        print({'error': str(e)})

        # todo For mvp, return sample portfolio. Replace with above once data has been integrated.
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