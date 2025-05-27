# app/principal.py

from fastapi import FastAPI, UploadFile, File, Form # Ahora importamos Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.servicios.servicio_simulacion import simular_datos_csv
from app.configuracion import configuracion

from app.servicios.endpoints import router as valores_router
from app.api.rutas.proyectos.proyectos import router_proyecto as router_proyecto

aplicacion = FastAPI()

origins = [
    "http://localhost:8001",
    "http://127.0.0.1:8001",
]

aplicacion.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

aplicacion.mount("/web", StaticFiles(directory="web"), name="web")
#Se incluyen las rutas correspondientes
aplicacion.include_router(valores_router)
aplicacion.include_router(router_proyecto)

@aplicacion.get("/", response_class=HTMLResponse)
async def read_root():
    with open("web/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@aplicacion.post("/simular/")
async def simular_datos(
    file: UploadFile = File(...),
    proyecto_id: int = Form(...),    # Nuevo parámetro del formulario
    dispositivo_id: int = Form(...) # Nuevo parámetro del formulario
):
    try:
        file_content = await file.read()
        print(f"Archivo recibido: {file.filename}, tamaño: {len(file_content)} bytes")
        print(f"IDs recibidos: Proyecto={proyecto_id}, Dispositivo={dispositivo_id}")

        # Pasa los IDs a la función de servicio
        resultados = await simular_datos_csv(file_content, proyecto_id, dispositivo_id)

        return {"message": "Simulación y carga de datos en DB completada.", "resultados": resultados}

    except ValueError as e:
        return {"message": "Error en la validación del CSV", "details": str(e)}
    except Exception as e:
        return {"message": "Error inesperado durante la simulación", "details": str(e)}
