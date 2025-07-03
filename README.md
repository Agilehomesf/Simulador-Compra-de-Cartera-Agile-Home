# Simulador de Compra de Cartera Hipotecaria - Agile Home

Un simulador web que permite a los usuarios comparar diferentes opciones de compra de cartera hipotecaria entre múltiples bancos colombianos, calculando ahorros potenciales y facilitando la toma de decisiones financieras.

## Características

- **Comparación Múltiple**: Compara ofertas de 5 bancos principales de Colombia
- **Cálculos Precisos**: Simulación de pagos mensuales y ahorros totales
- **Interfaz Intuitiva**: Diseño responsivo con los colores de Agile Home
- **Contacto Directo**: Integración con WhatsApp para contactar asesores
- **Validación Completa**: Validación de formularios y lógica de negocio

## Bancos Incluidos

- **Banco de Bogotá**: 9.95% (campaña) - 12.68%
- **BBVA**: 12.95% - 15.79% (VIS), desde 14.92% (No VIS)
- **Itau**: 11.71% - 12.40%
- **Banco de Occidente**: 10.85% - 16.16%
- **Caja Social**: 10.00% - 16.60%

## Tecnologías

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Estilos**: Bootstrap 5, CSS personalizado
- **Fuentes**: Google Fonts (Poppins)
- **Iconos**: Bootstrap Icons

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/simulador-cartera-hipotecaria.git
cd simulador-cartera-hipotecaria
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno (opcional):
```bash
export SESSION_SECRET="tu-clave-secreta"
export WHATSAPP_NUMBER="57300XXXXXXX"
```

4. Ejecuta la aplicación:
```bash
python main.py
```

La aplicación estará disponible en `http://localhost:5000`

## Estructura del Proyecto

```
simulador-cartera-hipotecaria/
├── static/
│   ├── css/
│   │   └── style.css          # Estilos personalizados
│   └── js/
│       └── calculator.js      # Lógica del calculador
├── templates/
│   └── index.html             # Plantilla principal
├── app.py                     # Aplicación Flask principal
├── main.py                    # Punto de entrada
├── requirements.txt           # Dependencias Python
├── replit.md                  # Documentación del proyecto
└── README.md                  # Este archivo
```

## Uso

1. **Ingresa los datos de tu hipoteca actual**:
   - Valor del inmueble
   - Saldo de la cartera a comprar
   - Plazo inicial y restante (en meses)
   - Tasa efectiva anual actual
   - Valor de seguros
   - Plazo deseado para la nueva cartera

2. **Selecciona los bancos a comparar**:
   - Puedes seleccionar todos o solo algunos bancos
   - Cada banco muestra sus rangos de tasas

3. **Obtén los resultados**:
   - Comparación de cuotas mensuales
   - Cálculo de ahorros mensuales y totales
   - Opción de contactar directamente cada banco

## Configuración

### Variables de Entorno

- `SESSION_SECRET`: Clave secreta para sesiones de Flask
- `WHATSAPP_NUMBER`: Número de WhatsApp para contacto (formato: 57300XXXXXXX)

### Personalización

- **Colores**: Modifica las variables CSS en `static/css/style.css`
- **Bancos**: Actualiza el diccionario `BANKS` en `app.py`
- **Textos**: Edita los textos en `templates/index.html`

## Contribución

1. Fork el proyecto
2. Crea una rama para tu función (`git checkout -b feature/nueva-funcion`)
3. Commit tus cambios (`git commit -am 'Agrega nueva función'`)
4. Push a la rama (`git push origin feature/nueva-funcion`)
5. Crea un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Para soporte técnico o consultas sobre el simulador, contacta a tu asesor Agile Home.

---

**Agile Home** - Tu aliado en el camino hacia la casa de tus sueños