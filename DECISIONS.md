# Registro de Decisiones Técnicas

Este documento registra las decisiones arquitectónicas y técnicas tomadas durante el desarrollo.


## 1. Arquitectura: Layered + Service Layer

**Fecha:** 2025-11-01

**Contexto:** Necesitaba elegir entre arquitectura en capas simple, feature-based o clean architecture.

**Decisión:** Implementar arquitectura en capas con capa de servicios adicional.

**Razones:**
- Balance entre simplicidad y escalabilidad
- Separación clara de responsabilidades (router → service → repository)
- Facilita implementación del sistema de permisos en la capa de servicio
- Estándar de la industria sin caer en sobre-ingenieria
- Permite orquestar operaciones complejas (ejemplo: crear post + asignar tags)
- Routers delgados = más fácil de leer

**Alternativas consideradas:**
- Layered simple: Más rápida pero mezcla lógica de negocio en routers
- Feature-based: Buena modularidad pero relaciones entre entidades menos claras
- Clean Architecture: Complejidad excesiva para el contexto de la prueba

**Trade-offs aceptados:**
- Supone un mayor timpo de desarrollo vs arquitectura simple
- Una capa adicional de abstracción


**Estructura previa para la arquitectura escogida**

``Nota: puede ser ligeramente diferente en el proyecto.``

```
proyecto/
├── api/
│   └── routers/       # Solo routing
│
├── services/          # Lógica de negocio
│   ├── user_service.py
│   ├── post_service.py
│   └── auth_service.py
│
├── repositories/       # Acceso a datos
│   ├── base.py
│   ├── user_repository.py
│   └── post_repository.py
│
├── models/             # SQLAlchemy
├── schemas/            # Pydantic
└── core/               # Infraestructura
```

## 2. Primary key: UUID vs Int(Autoincrement)

**Fecha:** 2025-11-01

**Contexto:** Necesitaba decidir como identificar los recursos en las tablas de la base de datos.

**Decisión:** Usar Autoincrement(integer).

**Razones:**
- **Sistemas Centralizados**: La aplicación usa una única base de datos (monolito) donde la generación secuencial es simple y controlada
- **Prioridad al Rendimiento**: Se requiere la máxima velocidad en inserciones, joins e indexación (son claves naturalmente ordenadas)
- **Legibilidad y Debugging**: Los IDs se exponen frecuentemente a usuarios internos o se usan para depuración manual (ej: "Ticket #123")
- **Bajo Uso de Espacio**: En tablas muy grandes, el ahorro de 8 bytes por fila es significativo

**Alternativas consideradas:**
- UUID: pero no existe una necesidad imperativa de unicidad global o sistemas distribuidos

**Trade-offs aceptados:**
- No es Único Globalmente (colisiones en sistemas distribuidos)
- Predecible (riesgo de enumeración/seguridad)
- Depende de la base de datos para la generación