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

**Alternativas consideradas:**
- Layered simple: Más rápida pero mezcla lógica de negocio en routers
- Feature-based: Buena modularidad pero relaciones entre entidades menos claras
- Clean Architecture: Excesiva para el contexto de la prueba

**Trade-offs aceptados:**
- Supone un mayor timpo de desarrollo vs arquitectura simple
- Una capa adicional de abstracción
