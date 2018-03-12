PENDIENTE = "PE"
RECHAZADO = "RC"
PAGADO = "PG"
CANCELADO = "CN"
DENEGADO = "DN"
PROCESO = 'PR_1'
PROCESO_2 = 'PR_2'
ORDER_VALIDATED = 'VAL'
ORDER_USED = 'USE'

TYPE_STATUS = (
    ("PG", "Pagado"),
    ("DN", "Denegado"),
    ("RC", "Rechazado"),
    ("PE", "Pendiente"),
    (PROCESO, "Proceso Paso 1"),
    (PROCESO_2, "Proceso Paso 2"),
    ("DES", "En Despacho"),
    ("CAM", "En Camino"),
    ("COM", "Completado"),
    ("CN", "Cancelado"),

)

ALMACEN = 'AL'
TYPE_STATUS_SHIPPING = (
    (ALMACEN, "En Almacén"),
    ("DS", "En Despacho"),
    ("EG", "Entregado"),
)
