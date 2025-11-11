import csv
import argparse
import sys
from typing import List, Tuple, Dict


def parse_amount(s: str) -> float:
    """Parsea una cadena numérica en formatos comunes:
    - "1234.56" -> 1234.56
    - "1.234,56" -> 1234.56
    - "1234,56" -> 1234.56
    Ignora símbolos de moneda y espacios.
    """
    if s is None:
        return 0.0
    s = str(s).strip()
    if s == '':
        return 0.0
    # eliminar símbolos de moneda y espacios
    s = s.replace('$', '').replace('€', '').replace(' ', '')

    # Si contiene tanto punto como coma, asumimos que '.' es separador de miles y ',' decimal
    if '.' in s and ',' in s:
        s = s.replace('.', '').replace(',', '.')
    else:
        # Solo coma -> coma decimal
        if ',' in s and '.' not in s:
            s = s.replace(',', '.')
        # Solo punto -> dejamos como está
    try:
        return float(s)
    except ValueError:
        # último recurso: eliminar todo excepto dígitos y punto/-, y volver a intentar
        import re
        cleaned = re.sub(r"[^0-9.\-]", '', s)
        try:
            return float(cleaned) if cleaned != '' else 0.0
        except ValueError:
            return 0.0


def procesar_csv(ruta_archivo: str, encoding: str = 'utf-8') -> Tuple[List[Dict], float, float]:
    efectivo_total = 0.0
    tarjeta_total = 0.0
    registros = []
    filas_leidas = 0
    filas_invalidas = 0

    with open(ruta_archivo, encoding=encoding, newline='') as archivo:
        lector = csv.DictReader(archivo, skipinitialspace=True)
        for fila in lector:
            filas_leidas += 1
            if not fila:
                filas_invalidas += 1
                continue
            # Usar get para evitar KeyError si cambia el encabezado
            medio = (fila.get('Medio de cobranza') or fila.get('Medio de cobro') or '').strip()
            importe_raw = fila.get('Importe') or fila.get('Importe ') or ''
            importe = parse_amount(importe_raw)

            if medio.lower() == 'caja seccional':
                efectivo_total += importe
            else:
                tarjeta_total += importe

            registros.append({
                'Nro. recibo': fila.get('Nro. recibo', ''),
                'Fecha recibo': fila.get('Fecha recibo', ''),
                'Nombre': fila.get('Nombre', ''),
                'Nota crédito': fila.get('Nota crédito', ''),
                'Referencia': fila.get('Referencia', ''),
                'Lote': '',
                'Cupon': '',
                'Importe': f"{importe:.2f}",
                'Medio de cobranza': medio,
                'Usuario alta': fila.get('Usuario alta', '')
            })

    print(f"Leídas: {filas_leidas} filas. Registros válidos: {len(registros)}. Filas inválidas/ignoras: {filas_invalidas}")
    return registros, efectivo_total, tarjeta_total


def exportar_planilla(registros: List[Dict], ruta_salida: str, encoding: str = 'utf-8') -> None:
    campos = ['Nro. recibo', 'Fecha recibo', 'Nombre', 'Nota crédito', 'Referencia',
              'Lote', 'Cupon', 'Importe', 'Medio de cobranza', 'Usuario alta']
    with open(ruta_salida, 'w', newline='', encoding=encoding) as salida:
        escritor = csv.DictWriter(salida, fieldnames=campos)
        escritor.writeheader()
        for fila in reversed(registros):
            escritor.writerow(fila)


def mostrar_resumen(efectivo: float, tarjeta: float) -> None:
    efectivo_str = f"${efectivo:.2f}" if efectivo > 0 else " $0.00"
    tarjeta_str = f"${tarjeta:.2f}" if tarjeta > 0 else " $0.00"
    print("\n--- Rendición del Día ---")
    print(f"Total Tarjeta / Aplicaciones: {tarjeta_str}")
    print(f"Total Efectivo (Caja Seccional): {efectivo_str}")


def main(argv=None):
    parser = argparse.ArgumentParser(description='Procesar CSV de rendición y exportar planilla de ingresos')
    parser.add_argument('-i', '--input', default='Reporte_Recibos3.csv', help='Archivo CSV de entrada')
    parser.add_argument('-o', '--output', default='planilla_ingreso.csv', help='Archivo CSV de salida')
    parser.add_argument('-e', '--encoding', default='utf-8', help='Encoding del archivo CSV')
    args = parser.parse_args(argv)

    try:
        registros, efectivo, tarjeta = procesar_csv(args.input, encoding=args.encoding)
    except FileNotFoundError:
        print(f"Archivo no encontrado: {args.input}")
        sys.exit(2)

    exportar_planilla(registros, args.output, encoding=args.encoding)
    mostrar_resumen(efectivo, tarjeta)


if __name__ == '__main__':
    main()
