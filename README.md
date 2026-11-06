# CatalogoVentas_Eva3

Aplicacion Django para catalogo de productos, control de stock y registro de
ventas. Incluye interfaz web responsive, Django Admin personalizado y API REST
protegida con JWT.

## Produccion

- Web y API: `https://cuidatuventa.vercel.app`
- API base: `https://cuidatuventa.vercel.app/api/`

La URL puede cambiar si se configura otro dominio en Vercel. El dominio
publico se controla mediante `ALLOWED_HOSTS`, `VERCEL_URL` y
`VERCEL_BRANCH_URL`.

## Configuracion local

1. Crea un entorno virtual e instala dependencias:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Define en `.env` las variables de PostgreSQL y seguridad:

   ```env
   host=...
   port=5432
   database=postgres
   user=...
   password=...
   SECRET_KEY=una-clave-larga-y-privada
   DEBUG=true
   ALLOWED_HOSTS=localhost,127.0.0.1
   CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
   ```

   No subas `.env` ni credenciales al repositorio. En pruebas automatizadas se
   puede usar `DJANGO_TESTING=1`, que utiliza SQLite en memoria.

3. Ejecuta migraciones y servidor:

   ```powershell
   python manage.py migrate
   python manage.py runserver 127.0.0.1:8000
   ```

## API REST

Todos los endpoints de escritura requieren autenticacion JWT. El catalogo
permite lectura publica; modificar productos o tallas requiere usuario
autenticado.

| Metodo | Endpoint | Acceso | Descripcion |
|---|---|---|---|
| POST | `/api/token/` | Publico | Obtiene access y refresh token |
| POST | `/api/token/refresh/` | Publico | Renueva el access token |
| GET | `/api/productos/` | Publico | Lista productos activos con tallas |
| POST/PATCH/DELETE | `/api/productos/` | JWT | Gestiona productos |
| GET | `/api/producto-tallas/` | Publico | Consulta stock por talla |
| POST/PATCH/DELETE | `/api/producto-tallas/` | JWT | Gestiona tallas y stock |
| GET/POST/PATCH/DELETE | `/api/clientes/` | JWT | Gestiona clientes |
| GET/POST | `/api/ventas/` | JWT | Consulta o registra ventas |
| GET/POST/PATCH/DELETE | `/api/venta-detalles/` | JWT | Gestiona detalles con stock atomico |

### Autenticarse

```bash
curl -X POST https://cuidatuventa.vercel.app/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"TU_PASSWORD"}'
```

Usa el valor `access` en las siguientes peticiones:

```bash
curl https://cuidatuventa.vercel.app/api/productos/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

### Registrar una venta atomica

El endpoint valida cada talla, bloquea producto y talla con `select_for_update`
y revierte toda la operacion si un item no tiene stock.

```bash
curl -X POST https://cuidatuventa.vercel.app/api/ventas/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rut_cliente": "12345678-9",
    "items": [
      {"producto": 1, "talla": 2, "cantidad": 1}
    ]
  }'
```

La respuesta incluye `cliente_detalle`, `detalles`, `total` y `fecha` para
evitar peticiones adicionales del cliente consumidor.

## Django Admin

Ingresa en `/admin/` con un superusuario. El espacio esta personalizado con
branding SNEAK//CTRL e incluye:

- Productos con busqueda por nombre, codigo y descripcion, filtros de estado,
  acciones para activar/desactivar y recalcular stock.
- Tallas editables dentro del producto mediante inline y gestionables desde su
  propio listado.
- Clientes con busqueda por RUT, nombre, telefono y correo.
- Ventas con inline de detalles, calculo automatico de total, busqueda por
  cliente/producto y reporte acumulado por rango de fechas.

## Verificacion

```powershell
$env:DJANGO_TESTING='1'
python manage.py check
python manage.py test inventario
```
