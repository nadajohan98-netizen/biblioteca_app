# web_app.py - Aplicación Flask para BiblioSmart
from functools import wraps
from flask import Flask, redirect, render_template, request, url_for, flash, session

from biblioteca.container import build_services
from biblioteca.models.prestamo import EstadoPrestamo
from biblioteca.services import BibliotecaError


# ──────────────────────────────────────────
# CONFIGURACIÓN DE FLASK
# ──────────────────────────────────────────
app = Flask(__name__)
app.config["SECRET_KEY"] = "biblioteca-local-dev"

# Inicializar servicios (Inyección de Dependencias)
libro_srv, usuario_srv, prestamo_srv = build_services()


# ──────────────────────────────────────────
# DECORADOR DE LOGIN (¡DEFINIDO ANTES DE USARLO!)
# ──────────────────────────────────────────
def login_required(f):
    """Decorador para proteger rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_logueado' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ──────────────────────────────────────────
# FUNCIONES AUXILIARES
# ──────────────────────────────────────────
def _resumen_prestamos():
    """Genera un resumen legible de préstamos para la vista"""
    libros = {l.id: l for l in libro_srv.listar()}
    usuarios = {u.id: u for u in usuario_srv.listar()}
    resumen = []
    for p in prestamo_srv.listar_todos():
        libro = libros.get(p.libro_id)
        usuario = usuarios.get(p.usuario_id)
        resumen.append(
            {
                "id": p.id,
                "estado": p.estado,
                "fecha_prestamo": p.fecha_prestamo,
                "fecha_vencimiento": p.fecha_vencimiento,
                "fecha_devolucion": p.fecha_devolucion,
                "vencido": p.esta_vencido(),
                "libro_id": p.libro_id,
                "libro_titulo": libro.titulo if libro else "(libro eliminado)",
                "usuario_id": p.usuario_id,
                "usuario_nombre": usuario.nombre if usuario else "(usuario eliminado)",
            }
        )
    return resumen


# ──────────────────────────────────────────
# RUTAS PRINCIPALES (PROTEGIDAS CON LOGIN)
# ──────────────────────────────────────────

@app.get("/")
@login_required  # ✅ Protegida: requiere login
def index():
    libros = libro_srv.listar()
    usuarios = usuario_srv.listar()
    prestamos = _resumen_prestamos()

    return render_template(
        "index.html",
        libros=libros,
        usuarios=usuarios,
        prestamos=prestamos,
        estado_activo=EstadoPrestamo.ACTIVO.value,
    )


# ──────────────────────────────────────────
# RUTAS DE LIBROS
# ──────────────────────────────────────────

@app.post("/libros")
@login_required
def crear_libro():
    try:
        libro_srv.crear(
            request.form.get("titulo", "").strip(),
            request.form.get("autor", "").strip(),
            request.form.get("isbn", "").strip(),
            int(request.form.get("stock", "0")),
        )
        flash("Libro creado correctamente.", "ok")
    except (ValueError, BibliotecaError) as exc:
        flash(f"No se pudo crear el libro: {exc}", "error")
    return redirect(url_for("index"))


@app.post("/libros/editar")
@login_required
def editar_libro():
    try:
        libro_srv.editar(
            request.form.get("libro_id", "").strip(),
            titulo=request.form.get("titulo") or None,
            autor=request.form.get("autor") or None,
            stock_total=(
                int(request.form["stock_total"])
                if request.form.get("stock_total", "").strip()
                else None
            ),
        )
        flash("Libro actualizado.", "ok")
    except (ValueError, BibliotecaError) as exc:
        flash(f"No se pudo editar el libro: {exc}", "error")
    return redirect(url_for("index"))


@app.post("/libros/eliminar")
@login_required
def eliminar_libro():
    try:
        libro_srv.eliminar(request.form.get("libro_id", "").strip())
        flash("Libro eliminado.", "ok")
    except BibliotecaError as exc:
        flash(f"No se pudo eliminar el libro: {exc}", "error")
    return redirect(url_for("index"))


# ──────────────────────────────────────────
# RUTAS DE USUARIOS
# ──────────────────────────────────────────

@app.post("/usuarios")
@login_required
def crear_usuario():
    try:
        limite_str = request.form.get("max_prestamos", "").strip()
        limite = int(limite_str) if limite_str else 3
        usuario_srv.registrar(
            request.form.get("nombre", "").strip(),
            request.form.get("email", "").strip(),
            max_prestamos=limite,
        )
        flash("Usuario registrado.", "ok")
    except (ValueError, BibliotecaError) as exc:
        flash(f"No se pudo registrar el usuario: {exc}", "error")
    return redirect(url_for("index"))


@app.post("/usuarios/editar")
@login_required
def editar_usuario():
    try:
        limite_raw = request.form.get("max_prestamos", "").strip()
        limite = int(limite_raw) if limite_raw else None
        usuario_srv.editar(
            request.form.get("usuario_id", "").strip(),
            nombre=request.form.get("nombre") or None,
            max_prestamos=limite,
        )
        flash("Usuario actualizado.", "ok")
    except (ValueError, BibliotecaError) as exc:
        flash(f"No se pudo editar el usuario: {exc}", "error")
    return redirect(url_for("index"))


@app.post("/usuarios/desactivar")
@login_required
def desactivar_usuario():
    try:
        usuario_srv.desactivar(request.form.get("usuario_id", "").strip())
        flash("Usuario desactivado.", "ok")
    except BibliotecaError as exc:
        flash(f"No se pudo desactivar el usuario: {exc}", "error")
    return redirect(url_for("index"))


# ──────────────────────────────────────────
# RUTAS DE PRÉSTAMOS
# ──────────────────────────────────────────

@app.post("/prestamos")
@login_required
def crear_prestamo():
    try:
        prestamo_srv.prestar(
            request.form.get("usuario_id", "").strip(),
            request.form.get("libro_id", "").strip(),
        )
        flash("Préstamo realizado.", "ok")
    except BibliotecaError as exc:
        flash(f"No se pudo realizar el préstamo: {exc}", "error")
    return redirect(url_for("index"))


@app.post("/prestamos/devolver")
@login_required
def devolver_prestamo():
    try:
        prestamo_srv.devolver(request.form.get("prestamo_id", "").strip())
        flash("Devolución registrada.", "ok")
    except BibliotecaError as exc:
        flash(f"No se pudo devolver el libro: {exc}", "error")
    return redirect(url_for("index"))


# ──────────────────────────────────────────
# RUTAS DE AUTENTICACIÓN (PÚBLICAS - NO requieren login)
# ──────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Muestra el formulario de login y procesa el inicio de sesión"""
    if request.method == 'POST':
        email_ingresado = request.form.get('email', '').strip()
        
        # Buscar si el usuario existe en la base de datos
        usuarios = usuario_srv.listar()
        usuario_encontrado = next((u for u in usuarios if u.email == email_ingresado), None)
        
        if usuario_encontrado:
            # Guardar sesión
            session['usuario_logueado'] = usuario_encontrado.nombre
            session['rol'] = 'admin' if 'admin' in email_ingresado else 'usuario'
            flash(f"Bienvenido, {usuario_encontrado.nombre}!", "success")
            return redirect(url_for('index'))
        else:
            flash("Correo no encontrado. Intenta con admin@biblio.com", "danger")
            
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Cierra la sesión del usuario"""
    session.pop('usuario_logueado', None)
    session.pop('rol', None)
    flash("Sesión cerrada correctamente.", "ok")
    return redirect(url_for('login'))


# ──────────────────────────────────────────
# PUNTO DE ENTRADA
# ──────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)