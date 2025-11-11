# CajaDiaria

Proyecto pequeño en HTML/JavaScript/CSS para procesar reportes CSV generados por un sistema externo y generar una "planilla de ingresos" imprimible y descargable.

Descripción
-----------
`cajaDiaria.html` permite cargar un archivo CSV local (ej. `Reporte_Recibos3.csv`), sumar los importes por medio de cobranza (efectivo `Caja Seccional` vs tarjeta/otros), y generar:

- Un resumen en pantalla (Efectivo, Tarjeta, Total).
- Una descarga CSV para "Planilla de Ingresos".
- Una vista lista para imprimir con filas y totales.

Estado
------
- Implementado un parser CSV sencillo que soporta campos entre comillas y comillas escapadas.
- Descarga generada usando `Blob` (más fiable que data URIs).
- Interfaz mínima con botón explícito "Cargar Archivo CSV", indicadores `#rendicion` y `#fileInfo`.

Archivos relevantes
-------------------
- `cajaDiaria.html` — archivo principal: UI + lógica JS.
- `Reporte_Recibos3.csv` — ejemplo de entrada (muestra incluida en el repo).

Formato CSV esperado
--------------------
El CSV debe contener un encabezado y las columnas en el siguiente orden (ejemplo de encabezado):

```
Nro. recibo,Nombre,Nro. doc.,Medio de cobranza,Fecha recibo,Importe,Referencia,Usuario alta,Nota crédito,Estado
```

De cada fila el script usa, entre otras, estas columnas (índices):
- 0: Nro. recibo
- 1: Nombre
- 3: Medio de cobranza (ej. `Caja Seccional`, `Tarjeta`)
- 4: Fecha recibo (formato `DD-MM-YYYY` en el ejemplo)
- 5: Importe (puede usar coma o punto como separador decimal)
- 6: Referencia
- 7: Usuario alta
- 8: Nota crédito

Ejemplo de filas (muestra):

```
1192-RB-00005901,GOMEZ MARTIN EDUARDO,20345678,Caja Seccional,12-07-2023,850.00,201,jperez,,Aprobado
1192-RB-00005902,FERNANDEZ ANA MARIA,27890123,Tarjeta,12-07-2023,1450.50,305,lrodriguez,,Aprobado
```

Cómo usarlo (modo rápido)
-------------------------
1. Abrir `cajaDiaria.html` en un navegador moderno (Chrome, Firefox, Edge).
2. Hacer clic en el logo o en el botón "Cargar Archivo CSV" y seleccionar el archivo (ej. `Reporte_Recibos3.csv`).
3. En la tarjeta verás los totales en `#rendicion` y la línea `#fileInfo` con el nombre y filas procesadas.
4. Usá "Guardar para Planilla de Ingresos" para descargar `planilla_ingreso.csv` o "Imprimir Planilla" para abrir la vista de impresión.

Notas técnicas y limitaciones
----------------------------
- El parser CSV incluido es simple y soporta comillas y comillas escapadas, pero no está optimizado para archivos muy grandes (decenas de MB).
- La normalización de importes intenta convertir tanto `1234.56` como `1.234,56`, eliminando puntos como separador de miles antes de parsear. Si tus datos contienen símbolos de moneda o formatos mixtos, revisá la columna antes de procesar.
- Se inyecta HTML en la ventana de impresión: los valores provienen de archivos locales, pero siempre es buena práctica asegurarse que los datos sean confiables.

Mejoras sugeridas (futuras)
---------------------------
- Reemplazar el parser casero por [PapaParse](https://www.papaparse.com/) para mayor robustez y streaming/worker (recomendado si esperas archivos grandes).
- Añadir validaciones visuales (filas inválidas, log de errores) y previsualización de N primeras filas.
- Añadir tests unitarios para el transformador de filas y los cálculos de totales.
- Mejorar accesibilidad (aria-labels, control de foco y teclado) y estilo con CSS separado.

Subir al repositorio remoto (recordatorio)
-----------------------------------------
Si todavía no subiste el repo a GitHub, aquí tienes los comandos básicos (desde la carpeta del proyecto):

```bash
git init
git add .
git commit -m "Initial commit: cajaDiaria project"
git branch -M main
git remote add origin https://github.com/xpablodaniel/cajaDiaria.git
git push -u origin main
```

Contacto
--------
Para dudas o mejoras, indicame qué funcionalidad preferís priorizar (p. ej. PapaParse, drag & drop, tests) y lo implemento.

License
-------
Usá la licencia que prefieras; si no especificás nada, se asume uso privado. Agrego un `LICENSE` si querés (por ejemplo MIT).

CLI vs UI (resumen rápido)
-------------------------
Este proyecto incluye dos formas de procesar los reportes:

- `cajaDiaria.html` (UI en navegador): recomendado para uso interactivo y visual por parte de un operador. Permite cargar un CSV desde el equipo, ver totales al instante, descargar la planilla y emitir la impresión desde el navegador.
- `rendicion_diaria.py` (script CLI en Python): recomendado para automatización, ejecución por lotes, integración en pipelines o cron jobs. Produce la misma planilla CSV y un resumen por consola.

¿Cuál usar?
- Si necesitás una experiencia rápida y visual para un usuario que revisa y corrige datos manualmente: usá `cajaDiaria.html`.
- Si necesitás procesar archivos periódicamente, integrarlo en un servidor o ejecutar validaciones automáticas: usá `rendicion_diaria.py`.

Consistencia y mantenimiento
- Ambos flujos realizan los mismos cálculos (sumas por medio de cobranza). Es importante mantener las reglas de parseo y normalización (p. ej. `parse_amount` en Python y la lógica de JS) sincronizadas para evitar discrepancias en los totales.
- Si querés centralizar la lógica en el futuro, considerá exponer un pequeño servicio HTTP (Flask/FastAPI) que implemente la lógica de cálculo y sea consumido por la UI. Otra opción es empaquetar la lógica en una librería que ambos consuman.

Comandos de ejemplo
- Ejecutar el script Python con el CSV de ejemplo:

```bash
python3 rendicion_diaria.py -i Reporte_Recibo.csv -o planilla_ingreso.csv
```

- Abrir la interfaz web: doble clic en `cajaDiaria.html` o abrirlo en el navegador. Hacer clic en "Cargar Archivo CSV" y seleccionar el archivo.

Notas finales
- Mantené una pequeña suite de pruebas si la lógica de negocio crece (p. ej. pytest para `parse_amount` y `procesar_csv`).
- Cuando subas los cambios al repo remoto, verificá que incluyas `README.md`, `cajaDiaria.html` y `rendicion_diaria.py` para que cualquiera pueda reproducir el flujo.

