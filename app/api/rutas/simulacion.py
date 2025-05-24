from fastapi import APIRouter, UploadFile, File, Form, Depends
from ...servicios.servicio_simulacion import procesar_simulacion
from ..modelos.simulacion import ConfiguracionSimulacion

router = APIRouter()

@router.post("/simular/")
async def simular_desde_csv(
    archivo_csv: UploadFile = File(..., description="Archivo CSV a simular"),
    url: str = Form(..., description="URL de destino para los datos"),
    intervalo: float = Form(..., description="Intervalo en segundos entre envíos"),
    proyecto: str = Form(..., description="ID del proyecto"),
    dispositivo: str = Form(..., description="ID del dispositivo")
):
    """
    Endpoint para simular el envío de datos desde un archivo CSV.
    """
    configuracion = ConfiguracionSimulacion(url=url, intervalo=intervalo, proyecto=proyecto, dispositivo=dispositivo)
    return await procesar_simulacion(archivo_csv, configuracion)