# CatalogoVentas_Eva3

Aplicación Django para catálogo, control de stock y ventas, preparada para
consumo REST desde un cliente externo y despliegue en Vercel.

## Configuración

En desarrollo, define en `.env` las variables `host`, `port`, `database`,
`user`, `password` y `SECRET_KEY`. Para PostgreSQL se usan las credenciales de
Supabase. Las pruebas usan SQLite cuando `DJANGO_TESTING=1`.

Configura `CORS_ALLOWED_ORIGINS` como una lista de URLs separadas por comas.
Si no se define, solo se permiten los clientes locales en los puertos usuales.

## API

La API requiere JWT:

- `POST /api/token/`
- `POST /api/token/refresh/`
- `/api/productos/`
- `/api/producto-tallas/`
- `/api/clientes/`
- `/api/ventas/`
- `/api/venta-detalles/`

Envía el token de acceso como `Authorization: Bearer <token>`.
