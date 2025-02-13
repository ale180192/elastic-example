

## Aquitectura de todo el sistema

### Arquitectura de Doble Write:

En este enfoque, cuando la aplicación necesita escribir datos, realiza dos operaciones de escritura separadas: una en la base de datos principal y otra en Elasticsearch.
La escritura se realiza de forma síncrona o casi síncrona en ambos sistemas.
Las ventajas incluyen la consistencia inmediata de los datos y la simplicidad de implementación.
Las desventajas son el mayor acoplamiento entre sistemas, mayor latencia en las operaciones de escritura, y posibles problemas de consistencia si una de las escrituras falla.

### Change Data Capture (CDC):

Este enfoque captura los cambios que ocurren en la base de datos principal y los replica en Elasticsearch de forma asíncrona.
Funciona monitoreando los logs de transacciones o binarios de la base de datos para detectar cambios.
Las ventajas incluyen menor acoplamiento entre sistemas, mejor rendimiento en escrituras, y capacidad de reconstruir el estado de Elasticsearch desde los logs históricos.
Las desventajas son una mayor complejidad en la implementación y una consistencia eventual en lugar de inmediata.

##### Algunas tecnologías comunes para implementar CDC:

- Debezium para bases de datos como MySQL, PostgreSQL, MongoDB
- Maxwell's daemon para MySQL
- Kafka Connect con conectores CDC
- Herramientas nativas como AWS DMS


##### Posible arquitectura

- Es usada por Netflix, Uber, LinkedIn, Walmart, Zalando, etc

`Postgres → Debezium → Kafka → Kafka Connect → Elasticsearch`

- Postgres (datos relacionales)
  → Debezium (convierte a JSON con estructura original)
  → Kafka (almacena eventos)
  → Kafka Streams (transformaciones complejas/enriquecimiento) [opcional]
  → Kafka Connect con ES Connector (mapeo final y transformaciones para ES)
  → Elasticsearch (indexación)

###### Flujo:

- Debezium lee los cambios del WAL de Postgres
- Los publica como eventos en tópicos de Kafka
- Kafka Connect consume estos eventos
- Los transforma al formato necesario para Elasticsearch
- Los escribe en Elasticsearch

###### Casos de uso adicionales que permite:

- Replicar datos a múltiples destinos además de Elasticsearch
- Implementar Event Sourcing
- Análisis en tiempo real con otras herramientas
- Auditoría y logging de cambios
- Sincronización con otros sistemas



## Elasticsearch Cluster Architecture Guide

### 1.- Hot-Warm Architecture

##### Hot Nodes
- Contienen datos recientes y frecuentemente accedidos
- Usan hardware más potente (más RAM, SSDs)
- Optimizados para escrituras y búsquedas frecuentes
- Típicamente más costosos

##### Warm Nodes

- Almacenan datos históricos menos accedidos
- Usan hardware más económico (HDDs, menos RAM)
- Optimizados para lectura
- Mejor relación costo/GB


### 2.- Multi-tenant vs Índices Separados:

##### 1.- Multi-tenant Approach

- Un índice compartido por múltiples clientes
- Usa campo de cliente como discriminador
- **Ventajas:**
    - Mejor utilización de recursos
    - Menos overhead de gestión
    - Más eficiente para clientes pequeños

- **Desventajas:**
    - Riesgo de "noisy neighbor"
    - Más complejo de escalar selectivamente
    - Difícil aislar problemas por cliente

##### 2.- Separated Indices Approach

- Un índice por cada cliente
- Ventajas:
  - Mejor aislamiento entre clientes
  - Facilita escalar por cliente
  - Menor sobrecarga de gestión


### 3.- Diseño de Índices:

##### Time-Based Indices

```txt
Índices por Tiempo:
logs-2024.02
logs-2024.03
logs-2024.04
```

- Facilita el manejo de retención
- Mejor para datos time-series
- Permite borrar datos antiguos fácilmente

##### Índices por Cliente:

```txt
Índices por Cliente:
client1-logs
client2-logs
client3-logs
```

- Mejor aislamiento
- Más fácil de respaldar por cliente
- Control de recursos por cliente

### Estrategia de Aliases y Rollover:

##### Aliases:

- Proporcionan abstracción sobre índices físicos
- Permiten cambios transparentes
- Facilitan migraciones

```txt
# Ejemplo de uso de aliases
logs-write -> logs-000001  (escritura)
logs-read  -> logs-000001, logs-000002  (lectura)
```

##### Rollover:

- Basado en tiempo: cada día/semana/mes
- Basado en tamaño: cuando alcanza cierto GB
- Basado en documentos: número máximo de docs

La elección entre estas estrategias depende de:

- Volumen de datos
- Patrones de acceso
- Requisitos de aislamiento
- Presupuesto
- Necesidades de mantenimiento

### Estrategias de Indexación 

Diseño de índices para diferentes casos de uso:

- Índices optimizados para búsqueda full-text
- Índices para analítica y reportes
- Índices para machine learning


Políticas de retención y lifecycle

- ILM (Index Lifecycle Management)
- Rollover policies
- Data tiers


Estrategias de replicación

- Número de shards y replicas
- Cross-cluster replication si es necesario



### Mapping para Casos Específicos

Diseño de mapping para order to cash:

- Campos de texto con múltiples analyzers
- Campos numéricos con doc_values
- Campos de fecha con formatos específicos


Mappings dinámicos vs explícitos

- Cuándo usar runtime fields
- Templates para nuevos índices


Optimizaciones específicas para:

- Búsqueda de texto en facturas/órdenes
- Agregaciones para reportes financieros
- Campos calculados para métricas de negocio







