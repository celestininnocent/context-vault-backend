# Context Vault Backend

FastAPI backend for Context Vault with Supabase integration. Provides RESTful endpoints for saving and retrieving context data.

## Features

- 🚀 FastAPI backend with async support
- 💾 Supabase database integration via REST API
- 🔒 Secure environment variable configuration
- 📝 Two main endpoints: POST /vault/save and GET /vault/context
- 🌐 CORS enabled for cross-origin requests
- 📦 Ready for deployment on Render, Heroku, or Vercel

## Prerequisites

- Python 3.9+
- Supabase account and project
- Git

## Supabase Setup

### 1. Create Supabase Project

1. Go to [Supabase](https://supabase.com) and create a new project
2. Wait for the project to be fully provisioned

### 2. Create Context Vault Table

Run this SQL in the Supabase SQL Editor:

```sql
CREATE TABLE context_vault (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id TEXT NOT NULL,
  context_type TEXT NOT NULL,
  context_data JSONB NOT NULL,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX idx_context_vault_user_id ON context_vault(user_id);
CREATE INDEX idx_context_vault_context_type ON context_vault(context_type);
CREATE INDEX idx_context_vault_created_at ON context_vault(created_at DESC);
```

### 3. Get API Credentials

1. Go to Project Settings > API
2. Copy your **Project URL** (SUPABASE_URL)
3. Copy your **service_role key** (SUPABASE_SERVICE_KEY) - NOT the anon key

⚠️ **Important**: Use the `service_role` key, not the `anon` key, as it has full database access.

## Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/celestininnocent/context-vault-backend.git
cd context-vault-backend
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and add your Supabase credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key-here
```

### 4. Run the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check

```bash
GET /health
```

Returns the health status of the API.

### Root Endpoint

```bash
GET /
```

Returns API information and available endpoints.

### Save Context

```bash
POST /vault/save
Content-Type: application/json

{
  "user_id": "user123",
  "context_type": "chat_history",
  "context_data": {
    "messages": [
      {"role": "user", "content": "Hello"},
      {"role": "assistant", "content": "Hi there!"}
    ]
  },
  "metadata": {
    "session_id": "abc123",
    "source": "web_app"
  }
}
```

**Response:**

```json
{
  "success": true,
  "message": "Context saved successfully",
  "data": {
    "id": "uuid-here",
    "user_id": "user123",
    "context_type": "chat_history",
    "context_data": {...},
    "metadata": {...},
    "created_at": "2025-11-04T00:00:00Z"
  }
}
```

### Get Context

```bash
GET /vault/context?user_id=user123&context_type=chat_history&limit=10
```

**Query Parameters:**
- `user_id` (optional): Filter by user ID
- `context_type` (optional): Filter by context type
- `limit` (optional, default=10): Maximum number of records to return

**Response:**

```json
{
  "success": true,
  "count": 5,
  "data": [
    {
      "id": "uuid-here",
      "user_id": "user123",
      "context_type": "chat_history",
      "context_data": {...},
      "metadata": {...},
      "created_at": "2025-11-04T00:00:00Z"
    }
  ]
}
```

## Deployment

### Option 1: Deploy to Render (Recommended)

1. **Fork or Push this Repository to GitHub**

2. **Sign up for Render** at [render.com](https://render.com)

3. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `context-vault-backend`

4. **Configure the Service**
   - **Name**: context-vault-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Add Environment Variables**
   - Go to "Environment" tab
   - Add `SUPABASE_URL` with your Supabase project URL
   - Add `SUPABASE_SERVICE_KEY` with your service role key

6. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Your API will be available at `https://your-service.onrender.com`

**OR** use the `render.yaml` file for automated deployment:

1. Update `render.yaml` with your environment variables
2. Click "New +" → "Blueprint"
3. Connect your repository and deploy

### Option 2: Deploy to Heroku

1. **Install Heroku CLI**

```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Login to Heroku**

```bash
heroku login
```

3. **Create a New Heroku App**

```bash
heroku create context-vault-backend
```

4. **Set Environment Variables**

```bash
heroku config:set SUPABASE_URL=https://your-project.supabase.co
heroku config:set SUPABASE_SERVICE_KEY=your-service-key-here
```

5. **Deploy**

```bash
git push heroku main
```

6. **Open the App**

```bash
heroku open
```

Your API will be available at `https://your-app.herokuapp.com`

### Option 3: Deploy to Vercel

1. **Install Vercel CLI**

```bash
npm i -g vercel
```

2. **Login to Vercel**

```bash
vercel login
```

3. **Deploy**

```bash
vercel
```

4. **Add Environment Variables**
   - Go to Vercel Dashboard
   - Select your project
   - Go to Settings → Environment Variables
   - Add `SUPABASE_URL` and `SUPABASE_SERVICE_KEY`

5. **Redeploy**

```bash
vercel --prod
```

Your API will be available at your Vercel domain.

**Note**: Vercel has limitations with Python and long-running processes. Render or Heroku are recommended for production use.

## Integration with Your Dashboard

### Frontend Integration Example

```javascript
// Save context
const saveContext = async (userId, contextType, contextData, metadata = {}) => {
  const response = await fetch('https://your-api-url.com/vault/save', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      context_type: contextType,
      context_data: contextData,
      metadata: metadata
    })
  });
  
  return await response.json();
};

// Get context
const getContext = async (userId, contextType = null, limit = 10) => {
  const params = new URLSearchParams({
    user_id: userId,
    limit: limit.toString()
  });
  
  if (contextType) {
    params.append('context_type', contextType);
  }
  
  const response = await fetch(`https://your-api-url.com/vault/context?${params}`);
  return await response.json();
};

// Usage
await saveContext('user123', 'chat_history', {
  messages: [{ role: 'user', content: 'Hello' }]
});

const contexts = await getContext('user123', 'chat_history');
console.log(contexts.data);
```

### Python Integration Example

```python
import httpx

API_URL = "https://your-api-url.com"

async def save_context(user_id: str, context_type: str, context_data: dict, metadata: dict = None):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/vault/save",
            json={
                "user_id": user_id,
                "context_type": context_type,
                "context_data": context_data,
                "metadata": metadata or {}
            }
        )
        return response.json()

async def get_context(user_id: str, context_type: str = None, limit: int = 10):
    params = {"user_id": user_id, "limit": limit}
    if context_type:
        params["context_type"] = context_type
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/vault/context", params=params)
        return response.json()
```

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPABASE_URL` | Yes | Your Supabase project URL |
| `SUPABASE_SERVICE_KEY` | Yes | Your Supabase service role key |
| `PORT` | No | Server port (default: 8000) |

## Testing

Test the API using curl:

```bash
# Test health endpoint
curl https://your-api-url.com/health

# Save context
curl -X POST https://your-api-url.com/vault/save \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "context_type": "test_context",
    "context_data": {"test": "data"},
    "metadata": {"source": "test"}
  }'

# Get context
curl "https://your-api-url.com/vault/context?user_id=test_user&limit=5"
```

## Project Structure

```
context-vault-backend/
├── main.py              # FastAPI application with endpoints
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
├── Procfile            # Heroku deployment config
├── render.yaml         # Render deployment config
├── vercel.json         # Vercel deployment config
└── README.md           # This file
```

## Security Considerations

- ⚠️ Never commit `.env` file to version control
- ⚠️ Use `service_role` key only on the backend, never expose it to clients
- ⚠️ In production, update CORS settings to allow only specific origins
- ⚠️ Implement authentication/authorization for production use
- ⚠️ Consider adding rate limiting for API endpoints

## Troubleshooting

### "SUPABASE_URL and SUPABASE_SERVICE_KEY must be set"
- Make sure environment variables are properly configured
- Verify `.env` file exists locally or environment variables are set on your deployment platform

### "Failed to save context"
- Verify Supabase table exists and has correct schema
- Check that `service_role` key is used, not `anon` key
- Verify network connectivity to Supabase

### "Failed to retrieve context"
- Check query parameters are correctly formatted
- Verify data exists in the database
- Check Supabase table permissions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for your own applications.

## Support

For issues or questions, please open an issue on GitHub.

## Next Steps

1. Set up your Supabase project and table
2. Deploy to your preferred platform (Render recommended)
3. Test the endpoints using the examples above
4. Integrate with your dashboard application
5. Add authentication and additional security measures for production

---

**Ready to deploy?** Follow the deployment instructions above for your preferred platform!
