PENDIENTE = "PE"
RECHAZADO = "RC"
PAGADO = "PG"
CANCELADO = "CN"
DENEGADO = "DN"
PROCESO = 'PR_1'
PROCESO_2 = 'PR_2'
ORDER_VALIDATED = 'VAL'
ORDER_USED = 'USE'
REEMBOLSO = 'RE'
TYPE_STATUS = (
    (PROCESO, "Pendiente"),
    ("RC", "Rechazado"),
    ("PG", "Pagado"),
    # ("PE", "Pendiente"),
    # (PROCESO_2, "Proceso Paso 2"),
    ("RE", "Reembolso"),

)

ALMACEN = 'AL'
TYPE_STATUS_SHIPPING = (
    (ALMACEN, "En Almacén"),
    ("DS", "En Despacho"),
    ("EG", "Entregado"),
)
