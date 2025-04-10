# Proyecto Análisis de Algoritmos
## Mancala

### Integrantes
- Adrian Ruiz
- Gustavo Ortiz
- Leonardo Velázquez
- Tomas Martinez

## Modelo de Dominio
![image](https://github.com/user-attachments/assets/16e11e21-1803-42af-8d7f-8784554fbaf4)
El diagrama de clases describe la arquitectura del sistema orientado a objetos para la gestión de un juego de tablero Mancala.
El componente central es la clase GameService, que actúa como controlador principal, encargándose de iniciar el juego (start_game), obtener el estado actual (get_game), reiniciarlo (restart_game), realizar movimientos (make_movement), aplicar reglas de captura (capture_rule) y verificar si el juego ha finalizado (check_end_game). Esta clase contiene una instancia de Game, gestionando directamente el estado del juego.

