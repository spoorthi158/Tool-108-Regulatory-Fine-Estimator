\# Tool-108 — AI Service (Flask Microservice)



\## 1. Overview

This is the AI microservice for the Regulatory Fine Estimator (Tool-108).

It runs on port 5000 and provides three AI-powered endpoints using the

Groq API with the LLaMA-3.3-70b-versatile model. It accepts regulatory

violation details and returns descriptions, recommendations, and reports.



\- \*\*Port:\*\* 5000

\- \*\*Health Check:\*\* http://localhost:5000/health

\- \*\*AI Model:\*\* llama-3.3-70b-versatile (via Groq API)



\---



\## 2. Tech Stack



| Technology      | Version | Purpose                        |

|-----------------|---------|--------------------------------|

| Python          | 3.11    | Service language               |

| Flask           | 3.0.0   | Web framework                  |

| Groq API        | 0.9.0   | AI model provider              |

| flask-limiter   | 3.5.0   | Rate limiting (30 req/min)     |

| Redis           | 5.0.1   | AI response cache (15 min TTL) |

| python-dotenv   | 1.0.0   | Environment variable loader    |



\---



\## 3. Prerequisites



\- Python 3.11 or higher

\- A free Groq API key from https://console.groq.com

\- Redis (optional for local, required in Docker)

\- Docker and Docker Compose (for containerised setup)



\---



\## 4. Environment Variables



| Variable        | Required | Default     | Description                    |

|-----------------|----------|-------------|--------------------------------|

| GROQ\_API\_KEY    | Yes      | —           | Your Groq API key (gsk\_...)    |

| REDIS\_HOST      | No       | localhost   | Redis server hostname          |

| REDIS\_PORT      | No       | 6379        | Redis server port              |

| FLASK\_ENV       | No       | development | Flask environment              |

| FLASK\_PORT      | No       | 5000        | Port the service runs on       |



\---



\## 5. Setup Instructions



\### Local Setup

```bash

\# 1. Clone the repository

git clone <repo-url>

cd Tool-108/ai-service



\# 2. Create your .env file

cp .env.example .env

\# Edit .env and add your GROQ\_API\_KEY



\# 3. Install dependencies

pip install -r requirements.txt



\# 4. Run the service

python app.py



\# 5. Verify it is running

curl http://localhost:5000/health

```



\### Docker Setup

```bash

\# From the project root folder

docker-compose up --build



\# The AI service will be available at http://localhost:5000

```



\---



\## 6. API Reference



\### GET /health

Returns service status, uptime, Redis connection, and available endpoints.



\*\*curl:\*\*

```bash

curl http://localhost:5000/health

```



\*\*Success Response:\*\*

```json

{

&#x20; "status": "ok",

&#x20; "model": "llama-3.3-70b-versatile",

&#x20; "version": "1.0.0",

&#x20; "uptime\_seconds": 120,

&#x20; "redis\_connected": true,

&#x20; "endpoints": \[

&#x20;   {"path": "/describe", "method": "POST"},

&#x20;   {"path": "/recommend", "method": "POST"},

&#x20;   {"path": "/generate-report", "method": "POST"},

&#x20;   {"path": "/health", "method": "GET"}

&#x20; ],

&#x20; "timestamp": "2026-04-25T10:00:00+00:00"

}

```



\---



\### POST /describe

Accepts violation details and returns an AI-generated description with fine estimate.



\*\*curl:\*\*

```bash

curl -X POST http://localhost:5000/describe \\

&#x20; -H "Content-Type: application/json" \\

&#x20; -d '{

&#x20;   "industry": "Healthcare",

&#x20;   "regulation\_type": "HIPAA",

&#x20;   "violation\_description": "Unauthorized disclosure of patient records",

&#x20;   "severity": "High"

&#x20; }'

```



\*\*Request JSON:\*\*

```json

{

&#x20; "industry": "Healthcare",

&#x20; "regulation\_type": "HIPAA",

&#x20; "violation\_description": "Unauthorized disclosure of patient records",

&#x20; "severity": "High"

}

```



\*\*Success Response:\*\*

```json

{

&#x20; "result": "{\\"description\\": \\"...\\", \\"estimated\_fine\_min\\": 100000, \\"estimated\_fine\_max\\": 500000, \\"currency\\": \\"USD\\", \\"reasoning\\": \\"...\\"}",

&#x20; "is\_fallback": false,

&#x20; "generated\_at": "2026-04-25T10:00:00+00:00"

}

```



\*\*Fallback Response (when Groq is unavailable):\*\*

```json

{

&#x20; "error": "AI service unavailable",

&#x20; "is\_fallback": true

}

```



\---



\### POST /recommend

Returns 3 actionable recommendations for the given violation.



\*\*curl:\*\*

```bash

curl -X POST http://localhost:5000/recommend \\

&#x20; -H "Content-Type: application/json" \\

&#x20; -d '{

&#x20;   "industry": "Finance",

&#x20;   "regulation\_type": "AML",

&#x20;   "violation\_description": "Failure to report suspicious transactions",

&#x20;   "severity": "Medium"

&#x20; }'

```



\*\*Request JSON:\*\*

```json

{

&#x20; "industry": "Finance",

&#x20; "regulation\_type": "AML",

&#x20; "violation\_description": "Failure to report suspicious transactions",

&#x20; "severity": "Medium"

}

```



\*\*Success Response:\*\*

```json

{

&#x20; "recommendations": \[

&#x20;   {"action\_type": "Legal", "description": "...", "priority": "High"},

&#x20;   {"action\_type": "Operational", "description": "...", "priority": "High"},

&#x20;   {"action\_type": "Training", "description": "...", "priority": "Medium"}

&#x20; ],

&#x20; "is\_fallback": false,

&#x20; "generated\_at": "2026-04-25T10:00:00+00:00"

}

```



\*\*Fallback Response:\*\*

```json

{

&#x20; "recommendations": \[

&#x20;   {"action\_type": "Legal", "description": "Consult with a regulatory compliance attorney.", "priority": "High"},

&#x20;   {"action\_type": "Operational", "description": "Conduct an internal audit.", "priority": "High"},

&#x20;   {"action\_type": "Training", "description": "Provide mandatory compliance training.", "priority": "Medium"}

&#x20; ],

&#x20; "is\_fallback": true,

&#x20; "generated\_at": "2026-04-25T10:00:00+00:00"

}

```



\---



\### POST /generate-report

Generates a full compliance report including risk assessment and recommendations.



\*\*curl:\*\*

```bash

curl -X POST http://localhost:5000/generate-report \\

&#x20; -H "Content-Type: application/json" \\

&#x20; -d '{

&#x20;   "industry": "Banking",

&#x20;   "regulation\_type": "GDPR",

&#x20;   "violation\_description": "Customer data breach affecting 10000 records",

&#x20;   "severity": "Critical",

&#x20;   "fine\_min": 100000,

&#x20;   "fine\_max": 500000

&#x20; }'

```



\*\*Request JSON:\*\*

```json

{

&#x20; "industry": "Banking",

&#x20; "regulation\_type": "GDPR",

&#x20; "violation\_description": "Customer data breach affecting 10000 records",

&#x20; "severity": "Critical",

&#x20; "fine\_min": 100000,

&#x20; "fine\_max": 500000

}

```



\*\*Success Response:\*\*

```json

{

&#x20; "report": {

&#x20;   "title": "GDPR Compliance Violation Report",

&#x20;   "executive\_summary": "...",

&#x20;   "violation\_overview": "...",

&#x20;   "risk\_assessment": "...",

&#x20;   "recommendations": \[...],

&#x20;   "conclusion": "..."

&#x20; },

&#x20; "is\_fallback": false,

&#x20; "generated\_at": "2026-04-25T10:00:00+00:00"

}

```



\*\*Fallback Response:\*\*

```json

{

&#x20; "report": {

&#x20;   "title": "Regulatory Violation Compliance Report",

&#x20;   "executive\_summary": "A regulatory violation has been identified...",

&#x20;   "violation\_overview": "...",

&#x20;   "risk\_assessment": "...",

&#x20;   "recommendations": \[...],

&#x20;   "conclusion": "..."

&#x20; },

&#x20; "is\_fallback": true,

&#x20; "generated\_at": "2026-04-25T10:00:00+00:00"

}

```



\---



\## 7. Common Issues



| Issue                        | Cause                          | Fix                                      |

|------------------------------|--------------------------------|------------------------------------------|

| GroqError: api\_key not set   | Missing GROQ\_API\_KEY in .env   | Add your key to .env file                |

| Redis connection failed      | Redis not running              | Start Redis or use Docker Compose        |

| 429 Too Many Requests        | Rate limit exceeded            | Wait 60 seconds and retry                |

| 503 AI service unavailable   | Groq API down or key invalid   | Check key at console.groq.com            |

| 400 Invalid input detected   | Prompt injection attempt       | Remove suspicious phrases from input     |

| Port 5000 already in use     | Another process using port     | Run: python app.py with different port   |

