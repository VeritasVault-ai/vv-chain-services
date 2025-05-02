# RiskBotApp

**LTV and TVL Risk Calculation Azure Function**

This Function App is part of the `vv-chain-services` repository. It receives blockchain event payloads via Azure Event Grid, enriches them, and uses a Python-based ML microservice to calculate updated LTV (Loan-to-Value) and TVL (Total Value Locked) metrics. The results are then pushed to Redis for downstream use by dashboards and alert systems.

---

## 📦 Project Structure

```
RiskBotApp/
├── RiskBotFunction.cs       # Main Azure Function triggered by Event Grid
├── RiskApiClient.cs         # HTTP client calling the Python ML API
├── Models.cs                # Data contracts for incoming/outgoing data
├── Helpers.cs               # Utility functions (e.g. sanitizers, mappers)
├── host.json                # Azure Function App host configuration
└── local.settings.json      # Local dev secrets (excluded from repo)
```

---

## ⚙️ Function Details

### Trigger:
- **EventGridTrigger** bound to new blockchain events (published via Goldsky webhook).

### Flow:
1. Deserialize and validate payload.
2. Invoke Python ML model (`/predict`) via `RiskApiClient.cs`.
3. Parse LTV/TVL predictions.
4. Push results to Redis (`redis://metrics:6379`).

---

## 🤖 ML Integration

The Python ML service is deployed as a separate container in `src/ml-engine`. It must be running and accessible by the RiskBot Function.

- **Endpoint:** `http://ml-engine:8000/predict`
- **Protocol:** HTTP POST
- **Input:** JSON body (defined in ML Pydantic schema)
- **Output:** `{ "ltv": float, "tvl": float }`

> Use `RiskApiClient.cs` to control retries and timeout logic.

---

## 🔐 Configuration

Values are stored in `local.settings.json` for local dev and injected via App Config in production:

```json
{
  "Values": {
    "ML_ENDPOINT": "http://ml-engine:8000/predict",
    "REDIS_CONNECTION_STRING": "<your-redis-url>"
  }
}
```

---

## 🧪 Testing

Unit tests live in `tests/RiskBotTests/`:
- `RiskBotFunctionTests.cs`
- `RiskApiClientTests.cs`

Use `Azure Functions Core Tools` to test locally:
```bash
func start
```

---

## 📌 Notes
- **Retry Logic:** Function retries are handled by Event Grid (max 24h) and internally by `RiskApiClient`.
- **Security:** Calls to ML engine and Redis should use Managed Identity where supported, otherwise secure keys.
- **Logging:** Use `ILogger` throughout to emit to Azure App Insights.

---

## 📈 Future Enhancements
- Add input schema validation with FluentValidation.
- Integrate feature flags via Azure App Configuration.
- Expose metrics via `/healthz` endpoint.

---

## 📞 Contacts
- Lead Engineer: `@JustAGhosT`
- ML Owner: `@mareeben`

---

*Last updated: May 2, 2025*
