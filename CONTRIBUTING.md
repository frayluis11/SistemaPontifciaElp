# Guía de Contribución

¡Gracias por tu interés en contribuir al Sistema Pontificia ELP!

## 🤝 Código de Conducta

- Sé respetuoso con todos los colaboradores
- Proporciona retroalimentación constructiva
- Enfócate en lo mejor para el proyecto

## 🚀 Cómo Contribuir

### Reportar Bugs

1. Verifica que el bug no haya sido reportado
2. Abre un nuevo issue con:
   - Descripción clara del problema
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Capturas de pantalla si aplica
   - Versión del sistema

### Proponer Nuevas Funcionalidades

1. Abre un issue describiendo:
   - Problema que resuelve
   - Solución propuesta
   - Alternativas consideradas

### Pull Requests

1. **Fork el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/SistemaPontifciaElp.git
   cd SistemaPontifciaElp
   ```

2. **Crear una rama**
   ```bash
   git checkout -b feature/nombre-feature
   # o
   git checkout -b fix/nombre-bug
   ```

3. **Realizar cambios**
   - Sigue las convenciones de código
   - Escribe código limpio y documentado
   - Agrega tests si aplica

4. **Commit cambios**
   ```bash
   git add .
   git commit -m "feat: descripción del cambio"
   ```

   Usa los prefijos:
   - `feat:` nueva funcionalidad
   - `fix:` corrección de bug
   - `docs:` cambios en documentación
   - `style:` formato, punto y coma faltantes, etc
   - `refactor:` refactorización de código
   - `test:` agregar tests
   - `chore:` cambios en build, herramientas, etc

5. **Push y crear PR**
   ```bash
   git push origin feature/nombre-feature
   ```

   Luego crear Pull Request en GitHub

## 📝 Estándares de Código

### Python (Backend)

- Seguir PEP 8
- Usar type hints
- Documentar funciones con docstrings
- Máximo 88 caracteres por línea (Black formatter)

```python
def create_user(username: str, email: str) -> User:
    """
    Create a new user.
    
    Args:
        username: The username for the new user
        email: The email address
        
    Returns:
        User: The created user object
    """
    pass
```

### JavaScript/React (Frontend)

- Usar funciones de flecha para componentes
- PropTypes o TypeScript para validación
- Nombres descriptivos para variables y funciones
- Componentes pequeños y reutilizables

```jsx
const UserProfile = ({ user }) => {
  return (
    <div className="user-profile">
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  )
}
```

## 🧪 Testing

### Backend

```bash
cd backend
pytest tests/
```

### Frontend

```bash
cd frontend
npm test
```

## 📚 Documentación

- Actualiza README.md si cambias funcionalidad
- Documenta nuevas APIs en los docstrings
- Actualiza DEPLOYMENT.md si cambias configuración

## 🔍 Revisión de Código

Todos los PRs serán revisados antes de merge. Prepárate para:

- Responder preguntas sobre tu código
- Hacer ajustes según feedback
- Asegurar que pasan todos los tests

## 🎯 Prioridades Actuales

Ver Issues con las etiquetas:
- `good first issue`: Ideal para principiantes
- `help wanted`: Necesitamos ayuda
- `priority`: Alta prioridad

## 📞 Contacto

- Issues: [GitHub Issues](https://github.com/frayluis11/SistemaPontifciaElp/issues)
- Email: ti@pontificia.edu

## 📄 Licencia

Al contribuir, aceptas que tus contribuciones serán licenciadas bajo la misma licencia que el proyecto (MIT).
