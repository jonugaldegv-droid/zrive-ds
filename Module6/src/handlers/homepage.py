from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get('/', response_class=HTMLResponse)
async def homepage():
        return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8" />
        <title>Zrive DS API</title>
        <style>
            body {
                font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                background: #f5f5f5;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 700px;
                margin: 60px auto;
                background: white;
                padding: 24px 32px;
                border-radius: 12px;
                box-shadow: 0 4px 18px rgba(0,0,0,0.08);
            }
            h1 {
                margin-top: 0;
                font-size: 1.8rem;
            }
            h2 {
                margin-top: 28px;
                font-size: 1.2rem;
            }
            .meta {
                margin-top: 16px;
                color: #555;
                line-height: 1.5;
            }
            .tag {
                display: inline-block;
                margin-top: 16px;
                padding: 4px 10px;
                border-radius: 999px;
                font-size: 0.8rem;
                background: #eef2ff;
            }
            a {
                color: #2563eb;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            ul {
                margin-top: 8px;
                padding-left: 20px;
            }
            code {
                background: #f3f4f6;
                padding: 2px 6px;
                border-radius: 4px;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Zrive DS – Pricing API</h1>
            <p>
                Esta API forma parte del proyecto <strong>Zrive Applied Data Science</strong>.
                Permite estimar precios a partir del <code>user_id</code> y registrar métricas
                de uso para su análisis posterior.
            </p>

            <div class="meta">
                <p><strong>Autor:</strong> Jon Ugalde García-Vera</p>
                <p><strong>Fecha de creación:</strong> 20/11/2025</p>
            </div>

            <span class="tag">Status: en desarrollo</span>

            <h2>Endpoints disponibles</h2>
            <ul>
                <li>
                    <code>GET /status</code> – Comprobar el estado de la API.<br />
                    👉 <a href="/status">Ir a /status</a>
                </li>
                <li>
                    <code>GET /docs</code> – Documentación interactiva (Swagger UI).<br />
                    👉 <a href="/docs">Ir a /docs</a>
                </li>
                <li>
                    <code>GET /redoc</code> – Documentación alternativa (ReDoc).<br />
                    👉 <a href="/redoc">Ir a /redoc</a>
                </li>
                <!-- Ejemplo para cuando tengas el endpoint de precio -->
                <!--
                <li>
                    <code>POST /estimate_price</code> – Estimar precio a partir de un <code>user_id</code>.
                </li>
                -->
            </ul>

            <div class="meta">
                <p>
                    Para más detalles sobre los parámetros y respuestas,
                    consulta la documentación en <a href="/docs">/docs</a>.
                </p>
            </div>
        </div>
    </body>
    </html>
    """