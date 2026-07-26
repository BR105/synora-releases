# Zynora — descargas

### Sitio web: **https://br105.github.io/synora-releases/**
Conoce Zynora, mira lo que hace y descárgalo desde la página oficial.

Distribución de **Zynora**: remapeo de ratón/teclado, macros, perfiles por app,
ecualizador de audio e iluminación RGB nativa (**Zynora Lumyx**).

> Este repositorio publica el **paquete portable** (sin código fuente).
> Para usuarios: mejor descarga desde la [página oficial](https://br105.github.io/synora-releases/)
> (un solo ZIP con todo dentro).

## Descargar e instalar

**Opción A (recomendada):** en la web, pulsa **Descargar gratis**. Se baja un ZIP;
al descomprimirlo ya ves `Zynora.exe` (no hay otro ZIP dentro).

**Opción B:** si descargas este repositorio desde GitHub («Code → Download ZIP»),
al descomprimir también verás `Zynora.exe` en la carpeta (junto al `.bat` y
`LEEME.txt`).

1. No ejecutes nada desde dentro del ZIP: extráelo a una carpeta con permiso
   de escritura (p. ej. el Escritorio).
2. La primera vez, ejecuta **«Abrir Zynora (primera vez).bat»** (doble clic, acepta
   el aviso de administrador): hace de confianza el certificado y abre la app.
3. A partir de ahí, abre **`Zynora.exe`** directamente. Detalle en `LEEME.txt`.

Zynora es portable: no se instala. Se ejecuta en tu equipo. Para contar usuarios
envía un ping anónimo opcional (versión + id aleatorio); puedes desactivarlo con
un archivo vacío `telemetry_off` junto al `.exe`. Detalle en la
[política de privacidad](https://br105.github.io/synora-releases/privacidad.html).

## Actualizaciones

Zynora se actualiza sola: en **☁ Nube → Actualizaciones → Buscar actualizaciones**.

## Archivos

| Archivo | Para qué |
|---------|----------|
| `Zynora.exe` | La aplicación |
| `Abrir Zynora (primera vez).bat` | Primera ejecución (confía el certificado) |
| `Zynora.cer` / `LEEME.txt` | Certificado y guía |
| `synora-update.json` | Manifiesto del autoactualizador |
| `docs/` | Sitio web (GitHub Pages), incluye el ZIP de descarga de la web |

El autoactualizador descarga el `.exe` desde el
[GitHub Release](https://github.com/BR105/synora-releases/releases/latest), no desde un ZIP anidado en el repo.
