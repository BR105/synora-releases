# Zynora — descargas

### Sitio web: **https://br105.github.io/synora-releases/**
Conoce Zynora, mira lo que hace y descárgalo desde la página oficial.

Distribución de **Zynora**: remapeo de ratón/teclado, macros, perfiles por app,
ecualizador de audio e iluminación RGB nativa (**Zynora Lumyx**).

> Este repositorio contiene **solo el paquete portable** para descargar.
> El código fuente es privado.

## Descargar e instalar

1. Descarga **`Zynora-0.3.0-portable.zip`** (o el ZIP de la
   [última release](https://github.com/BR105/synora-releases/releases/latest)).
2. Descomprime la carpeta (no la ejecutes desde dentro del ZIP).
3. La primera vez, ejecuta **«Abrir Zynora (primera vez).bat»** (doble clic, acepta
   el aviso de administrador): hace de confianza el certificado y abre la app.
   A partir de ahí, abre **`Zynora.exe`** directamente. Detalle en `LEEME.txt`.

Zynora es portable: no se instala. Se ejecuta en tu equipo. Para contar usuarios
envía un ping anónimo opcional (versión + id aleatorio); puedes desactivarlo con
un archivo vacío `telemetry_off` junto al `.exe`. Detalle en la
[política de privacidad](https://br105.github.io/synora-releases/privacidad.html).

## Actualizaciones

Zynora se actualiza sola: en **☁ Nube → Actualizaciones → Buscar actualizaciones**.

## Archivos en este repo

- `Zynora-X.Y.Z-portable.zip` — paquete completo (recomendado; incluye el `.exe`,
  el certificado, el `.bat` de primera vez y `LEEME.txt`).
- `synora-update.json` — manifiesto de versión (uso interno del actualizador).

El ejecutable suelto vive solo como asset de cada
[GitHub Release](https://github.com/BR105/synora-releases/releases) (lo usa el
autoactualizador). No se publica suelto en la raíz del repo.
