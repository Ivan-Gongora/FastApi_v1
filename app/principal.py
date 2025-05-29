# app/principal.py

from fastapi import FastAPI, UploadFile, File, Form # Ahora importamos Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# from app.servicios.servicio_simulacion import simular_datos_csv
from app.servicios.servicio_simulacion import simular_datos_csv

from app.configuracion import configuracion

from app.servicios.endpoints import router as valores_router
from app.api.rutas.proyectos.proyectos import router_proyecto as router_proyecto
from app.api.rutas.dispositivos.dispositivos import router_dispositivo as router_dispositivo
from app.api.rutas.sensores.sensores import router_sensor as router_sensor

aplicacion = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",  # <--- Make sure this is present and correct
    "http://127.0.0.1:8080",
    "http://localhost:5173",  # Keep this if you also test with Vite's default dev server
    "http://127.0.0.1:5173",
    # Add any other origins where your frontend might be hosted, e.g., "http://your-production-domain.com"
]

aplicacion.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Allows all headers
)

aplicacion.mount("/web", StaticFiles(directory="web"), name="web")
#Se incluyen las rutas correspondientes
aplicacion.include_router(valores_router)
aplicacion.include_router(router_proyecto)
aplicacion.include_router(router_dispositivo)
aplicacion.include_router(router_sensor)

aplicacion.include_router(router_proyecto, prefix="/api") # Asegúrate del prefijo /api aquí
aplicacion.include_router(router_dispositivo, prefix="/api") # Asegúrate del prefijo /api aquí
aplicacion.include_router(router_senso, prefix="/api") # Asegúrate del prefijo /api aquí


@aplicacion.get("/", response_class=HTMLResponse)
async def read_root():
    with open("web/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)



# @aplicacion.post("/simular/")
# async def simular_datos(
#     file: UploadFile = File(...),
#     proyecto_id: int = Form(...),    # Nuevo parámetro del formulario
#     dispositivo_id: int = Form(...) # Nuevo parámetro del formulario
# ):
#     try:
#         file_content = await file.read()
#         print(f"Archivo recibido: {file.filename}, tamaño: {len(file_content)} bytes")
#         print(f"IDs recibidos: Proyecto={proyecto_id}, Dispositivo={dispositivo_id}")

#         # Pasa los IDs a la función de servicio
#         resultados = await simular_datos_csv(file_content, proyecto_id, dispositivo_id)

#         return {"message": "Simulación y carga de datos en DB completada.", "resultados": resultados}

#     except ValueError as e:
#         return {"message": "Error en la validación del CSV", "details": str(e)}
#     except Exception as e:
#         return {"message": "Error inesperado durante la simulación", "details": str(e)}
# app/principal.py
from app.servicios.servicio_simulacion import extract_csv_preview


@aplicacion.post("/api/csv-preview/") # Se le añade el prefijo /api explícitamente
async def get_csv_preview(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        preview_data = await extract_csv_preview(file_content)
        return preview_data
    except Exception as e:
        return {"detail": f"Error al procesar el CSV: {e}"}, 400




@aplicacion.post("/api/simular/") # Se le añade el prefijo /api explícitamente
async def simular_datos(
    file: UploadFile = File(...),
    sensor_mappings: str = Form(...), # sensor_mappings viene como JSON string
    proyecto_id: int = Form(...),
    dispositivo_id: int = Form(...)
):
    try:
        import json # Importa json aquí si solo se usa en esta función
        parsed_sensor_mappings = json.loads(sensor_mappings)

        file_content = await file.read()
        print(f"Archivo recibido: {file.filename}, tamaño: {len(file_content)} bytes")
        print(f"IDs recibidos: Proyecto={proyecto_id}, Dispositivo={dispositivo_id}")
        # print(f"Mapeos recibidos: {parsed_sensor_mappings}") # No imprimir en producción, solo para depuración

        # Pasa los IDs de proyecto y dispositivo a simular_datos_csv
        resultados = await simular_datos_csv(
            file_content,
            parsed_sensor_mappings,
            proyecto_id,  # Nuevo parámetro
            dispositivo_id # Nuevo parámetro
        )

        return {"message": "Simulación y carga de datos en DB completada.", "resultados": resultados}

    except json.JSONDecodeError:
        return {"message": "Error en el formato JSON de los mapeos de sensores.", "details": "El string 'sensor_mappings' no es un JSON válido."}, 400
    except ValueError as e:
        return {"message": "Error en la validación del CSV o mapeo", "details": str(e)}, 400
    except Exception as e:
        print(f"Error inesperado durante la simulación: {e}") # Para depuración
        return {"message": "Error inesperado durante la simulación", "details": str(e)}, 500
