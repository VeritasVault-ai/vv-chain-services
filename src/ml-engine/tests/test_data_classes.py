import pytest
from main_app.data_classes.BlackLittermanModelData import BlackLittermanModelData


@pytest.fixture
def sample_json():
    """
    Provides a sample JSON string representing a BlackLitterman model configuration for testing.
    
    Returns:
        A multi-line JSON string containing model details, risk-free rates, and crypto market data.
    """
    return """
    {
      "Model": "BlackLitterman",
      "ModelParameters": {},
      "RiskFreeRates": [
        {
          "term": "1D",
          "rate": 0.0175
        }
      ],
      "CryptoMarketData": [
        {
          "Pool": "STETH",
          "Project": "Lido",
          "Chain": "Ethereum",
          "Metrics": [
            {
              "Date": "2025-05-03T15:30:00.123Z",
              "TVL": 123,
              "APY": 0.0523,
              "Base APY": 0.05,
              "Reward APY": 0.0023
            }
          ]
        }
      ]
    }
    """


@pytest.mark.parametrize(
    "expected_model_name,expected_risk_free_rate_term,expected_risk_free_rate_rate,expected_m1_date",
    [("BlackLitterman", "1D", 0.0175, "2025-05-03T15:30:00.123Z")],
)
def test_deserialization(sample_json: str, expected_model_name: str, expected_risk_free_rate_term: str,
                         expected_risk_free_rate_rate: str, expected_m1_date: str):
    model_data = BlackLittermanModelData.from_json(sample_json)
    assert model_data.Model == expected_model_name
    assert model_data.RiskFreeRates[0].term == expected_risk_free_rate_term
    assert model_data.RiskFreeRates[0].rate == expected_risk_free_rate_rate
    assert model_data.CryptoMarketData[0].Metrics[0].Date == expected_m1_date
