# Proyecto Análisis de Algoritmos
## Mancala

### Integrantes
- Adrian Ruiz
- Gustavo Ortiz
- Leonardo Velázquez
- Tomas Martinez

## Modelo de Dominio
![image](https://github.com/user-attachments/assets/16e11e21-1803-42af-8d7f-8784554fbaf4)

El diagrama de clases describe la arquitectura del sistema orientado a objetos para la gestión de un juego de tablero Mancala.<br/>
El componente central es la clase GameService, que actúa como controlador principal, encargándose de iniciar el juego (start_game), obtener el estado actual (get_game), reiniciarlo (restart_game), realizar movimientos (make_movement), aplicar reglas de captura (capture_rule) y verificar si el juego ha finalizado (check_end_game). Esta clase contiene una instancia de Game, gestionando directamente el estado del juego.

## Arquitectura del Sistema
![Componentes drawio(1)](https://github.com/user-attachments/assets/4e4433f8-1cb4-49e5-8158-79217287eff6)

Este sistema se divide en dos contenedores principales dentro de la capa de presentación.<br/>El primer contenedor es WEB Development, un componente desarrollado en Angular, cuya función es el manejo de la interfaz web. A través de esta interfaz los usuarios pueden interactuar con el sistema de forma intuitiva y accesible.<br/>El segundo contenedor es MancalaMicroservice, un componente implementado con FastAPI, responsable de ejecutar toda la lógica necesaria para satisfacer los requerimientos del juego Mancala. Ambos componentes se comunican mediante llamadas a API, lo que permite una separación clara entre la lógica de presentación y la lógica del negocio.

