# Sistema de Gestión de Biblioteca


##  Integrantes del Equipo

- **Johan Barragan** - Cédula: [1102635519]
- **Camilo Gutierrez** - Cédula: [1031177389:]
- **Mauricio Julio Mendoza** - Cédula: [cédula]
- **Hassler durley Trujillo beltran** - Cédula: [1003711485]

---
## Interfaz gráfica web (localhost)

1. Instala dependencias:

```bash
cd biblioteca_app
python3 -m pip install -r requirements.txt
```

2. Inicia el servidor web:

```bash
python3 web_app.py
```

3. Abre en tu navegador:

```text
http://localhost:5000
```

La interfaz permite gestionar libros, usuarios y préstamos utilizando la misma lógica de negocio y los mismos archivos JSON en `data/`.

## Principios SOLID aplicados

| Principio                     | Dónde se ve                                                          |
| ----------------------------- | -------------------------------------------------------------------- |
| **S** — Single Responsibility | Cada clase tiene una sola razón para cambiar                         |
| **O** — Open/Closed           | Para usar SQLite: crea `SqliteLibroRepository` sin tocar nada más    |
| **L** — Liskov Substitution   | `JsonLibroRepository` es intercambiable por cualquier implementación |
| **I** — Interface Segregation | Tres interfaces separadas; nadie recibe más de lo que usa            |
| **D** — Dependency Inversion  | `container.py` es el único lugar con clases concretas                |
