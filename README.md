# ⚡ C-TRONICS SGC — Sistema de Gestión Comercial

> Una herramienta sencilla para que una tienda de electrónica gestione su día a día.
> Proyecto del **Curso Integrador II — Universidad Tecnológica del Perú (UTP)**.

**🔗 Pruébalo en vivo:** https://t22ania.github.io/ctronics-sgc/
**👤 Acceso de demostración:** usuario `admin` · contraseña `admin123`

![CI](https://github.com/t22ania/ctronics-sgc/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/t22ania/ctronics-sgc/actions/workflows/cd.yml/badge.svg)

---

C-TRONICS SGC nació para resolver un problema muy concreto: que una tienda de electrónica pueda
llevar sus **productos, ventas, clientes e inventario** desde un solo lugar, sin complicaciones.

Todo funciona dentro del navegador. No hace falta instalar nada, ni montar un servidor, ni siquiera
tener internet: la información se guarda de forma automática en el propio equipo. Y aunque por
dentro es un único archivo (`c-tronics.html`) hecho con HTML, CSS y JavaScript, por fuera se siente
como un panel administrativo completo.

## ✨ Qué puedes hacer con él

- 🛒 **Vender al instante** con un punto de venta (POS) que calcula el IGV, descuenta el stock
  automáticamente y permite **anular ventas** devolviendo la mercadería.
- 📦 **Organizar el catálogo** de productos y sus **categorías**, con alertas cuando el stock baja.
- 📋 **Controlar el inventario** registrando entradas de mercadería y siguiendo cada movimiento.
- 👥 **Conocer a tus clientes** y revisar su historial de compras.
- 📈 **Entender tu negocio** con un panel de indicadores y **reportes que se exportan a PDF**.
- 🔒 **Trabajar con seguridad**: inicio de sesión con roles, cambio de contraseña y una
  **bitácora** que deja registro de todo lo importante.
- 💾 **Cuidar tu información** creando y restaurando respaldos, además de un cómodo modo oscuro.

## 🧪 Cómo probarlo

**En línea (lo más fácil):** entra a [la versión publicada](https://t22ania.github.io/ctronics-sgc/)
e ingresa con `admin` / `admin123`.

**En tu computadora:** descarga este repositorio y abre el archivo **`c-tronics.html`** con doble
clic en cualquier navegador moderno. Listo, no hay más pasos.

> La primera vez carga datos de ejemplo (productos, clientes y ventas) para que puedas explorar.
> Puedes volver al estado inicial desde *Configuración → Reiniciar base de datos*.

## 🛠️ Cómo está hecho

Un único archivo con **HTML, CSS y JavaScript puro** — sin frameworks, sin instalación y sin
proceso de compilación. Los datos se guardan en el `localStorage` del navegador.

## 🚀 Publicación automática

El proyecto se publica solo. Cada vez que se sube un cambio, **GitHub Actions revisa que el código
no tenga errores** y, si todo está bien, **lo despliega automáticamente** en GitHub Pages. Así la
versión en línea siempre está al día y nunca se publica algo roto.

<details>
<summary>¿Cómo se configuró el despliegue? (para quien clone el proyecto)</summary>

El repositorio usa dos flujos de GitHub Actions encadenados:

- **`ci.yml` (Integración Continua):** valida `c-tronics.html` en cada push o Pull Request a `main`.
- **`cd.yml` (Despliegue):** cuando la validación pasa, publica el sitio en GitHub Pages.

Para activarlo en un repositorio nuevo: **Settings → Pages → Source: _GitHub Actions_**. No se
necesita una rama `gh-pages`; el sitio se sirve desde el artefacto que genera el flujo.
</details>

## 📚 Documentación

En la carpeta [`/docs`](docs) encontrarás los documentos de gestión del proyecto:

- 📨 [Catálogo de Solicitudes](docs/catalogo-solicitudes.md) — pedidos de acceso e información y sus
  tiempos de atención.
- 🔧 [Gestión de Cambios](docs/gestion-cambios.md) — cómo se aprueban y registran los cambios.
- 📊 [Plan de Capacidad](docs/plan-capacidad.md) — qué se vigila del rendimiento y sus límites.
- 🔁 [Retrospectiva del Sprint 6](docs/retrospectiva.md) — qué salió bien y qué mejorar.

## 🗒️ Novedades

**Versión 1.1.0** — esta entrega sumó la anulación de ventas con devolución de stock, la gestión
de categorías, el cambio y restablecimiento de contraseña, y la bitácora de actividad. También se
mejoraron los respaldos (con fecha y hora en el archivo) y se automatizó la publicación web.

**Versión 1.0.0** — primera versión: inicio de sesión, panel de indicadores, productos, inventario,
ventas con IGV, clientes, reportes en PDF, respaldos en JSON y modo oscuro.

---

Proyecto académico de **C-TRONICS SOLUCIONES** · Curso Integrador II · UTP · Uso educativo.
