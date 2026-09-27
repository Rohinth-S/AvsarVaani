import uvicorn
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tasks.cron_jobs import deadline_reminder_loop, yutori_polling_loop
from routers import whatsapp_webhook, yutori_webhook, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the background checking loops when the server boots
    reminder_task = asyncio.create_task(deadline_reminder_loop())
    polling_task = asyncio.create_task(yutori_polling_loop())
    yield
    reminder_task.cancel()
    polling_task.cancel()

app = FastAPI(
    title="AvsarVaani API",
    description="Multilingual WhatsApp-based AI Opportunity Copilot Backend",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(whatsapp_webhook.router)
app.include_router(yutori_webhook.router)
app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
