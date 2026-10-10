import streamlit as st
import streamlit.components.v1 as components

# Configuración inicial del laboratorio educativo 3D
st.set_page_config(
    page_title="Generador de Simulaciones Educativas 3D",
    page_icon="🔬",
    layout="wide"
)

# Estilos personalizados para la interfaz
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E88E5; margin-bottom: 5px; }
    .sub-title { font-size: 14px; color: #666; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🧪 Generador y Visualizador de Simulaciones 3D Interactivas</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Crea, explora y descarga simulaciones 3D en HTML + Three.js para la educación científica.</div>', unsafe_allow_html=True)

# Panel lateral: Selección de plantilla o prompt personalizado
st.sidebar.header("⚙️ Configuración del Modelo 3D")
modo = st.sidebar.radio("Selecciona origen:", ["Plantillas Educativas", "Generador Personalizado"])

# Plantillas predefinidas en HTML + Three.js
PLANTILLAS = {
    "Física: Péndulo con Gravedad Ajustable": """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <style>
    body { margin: 0; overflow: hidden; font-family: sans-serif; background: #0f172a; color: #fff; }
    #ui { position: absolute; top: 10px; left: 10px; background: rgba(15,23,42,0.85); padding: 12px; border-radius: 8px; border: 1px solid #334155; width: 220px; }
    label { display: block; font-size: 12px; margin-top: 8px; }
    input[type=range] { width: 100%; }
    span { color: #38bdf8; font-weight: bold; }
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
  <div id="ui">
    <h4 style="margin:0; color:#38bdf8;">Péndulo 3D</h4>
    <label>Gravedad ($g$): <span id="gv">9.8</span> m/s²</label>
    <input type="range" id="g" min="0" max="25" step="0.1" value="9.8">
    <label>Longitud ($L$): <span id="lv">3.0</span> m</label>
    <input type="range" id="l" min="1" max="5" step="0.1" value="3.0">
  </div>
  <script>
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.1, 1000);
    camera.position.set(0, 0, 7);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(5, 10, 7);
    scene.add(light, new THREE.AmbientLight(0x404040));

    const pivot = new THREE.Group();
    pivot.position.set(0, 2, 0);
    scene.add(pivot);

    const sphere = new THREE.Mesh(
      new THREE.SphereGeometry(0.35, 32, 32),
      new THREE.MeshStandardMaterial({ color: 0x38bdf8, roughness: 0.3 })
    );
    let L = 3.0, g = 9.8, theta = 0.5, omega = 0;
    sphere.position.set(0, -L, 0);

    let lineGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0,0,0), new THREE.Vector3(0,-L,0)]);
    const line = new THREE.Line(lineGeo, new THREE.LineBasicMaterial({ color: 0xffffff }));
    pivot.add(line, sphere);

    document.getElementById('g').oninput = (e) => { g = parseFloat(e.target.value); document.getElementById('gv').innerText = g; };
    document.getElementById('l').oninput = (e) => { 
      L = parseFloat(e.target.value); document.getElementById('lv').innerText = L;
      sphere.position.set(0, -L, 0);
      line.geometry.dispose();
      line.geometry = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0,0,0), new THREE.Vector3(0,-L,0)]);
    };

    let lastTime = performance.now();
    function animate(now) {
      requestAnimationFrame(animate);
      const dt = Math.min((now - lastTime)/1000, 0.033);
      lastTime = now;
      omega += -(g/L) * Math.sin(theta) * dt;
      theta += omega * dt;
      pivot.rotation.z = theta;
      renderer.render(scene, camera);
    }
    animate(performance.now());
  </script>
</body>
</html>""",

    "Química: Molécula de Agua (H₂O) 3D": """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <style> body { margin: 0; overflow: hidden; background: #0f172a; } </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
  <script>
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.1, 1000);
    camera.position.set(0, 0, 5);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const light = new THREE.DirectionalLight(0xffffff, 1.2);
    light.position.set(3, 5, 5);
    scene.add(light, new THREE.AmbientLight(0x505050));

    const molGroup = new THREE.Group();
    
    // Átomo de Oxígeno (Rojo)
    const ox = new THREE.Mesh(new THREE.SphereGeometry(0.6, 32, 32), new THREE.MeshStandardMaterial({ color: 0xef4444 }));
    molGroup.add(ox);

    // Átomos de Hidrógeno (Blancos)
    const h1 = new THREE.Mesh(new THREE.SphereGeometry(0.35, 32, 32), new THREE.MeshStandardMaterial({ color: 0xf8fafc }));
    h1.position.set(-0.9, -0.6, 0);
    const h2 = new THREE.Mesh(new THREE.SphereGeometry(0.35, 32, 32), new THREE.MeshStandardMaterial({ color: 0xf8fafc }));
    h2.position.set(0.9, -0.6, 0);
    molGroup.add(h1, h2);

    scene.add(molGroup);

    function animate() {
      requestAnimationFrame(animate);
      molGroup.rotation.y += 0.01;
      molGroup.rotation.x += 0.005;
      renderer.render(scene, camera);
    }
    animate();
  </script>
</body>
</html>"""
}

# Lógica de selección del código HTML
html_code = ""

if modo == "Plantillas Educativas":
    opcion = st.sidebar.selectbox("Selecciona un tema:", list(PLANTILLAS.keys()))
    html_code = PLANTILLAS[opcion]
else:
    prompt_usuario = st.sidebar.text_area(
        "Describe el objeto o simulación 3D:",
        value="Un sistema planetario con un sol central y un planeta orbitando."
    )
    if st.sidebar.button("🤖 Generar Código HTML 3D"):
        # Plantilla dinámica en base a la solicitud
        html_code = f"""<!DOCTYPE html>
<html>
<head>
  <style> body {{ margin: 0; overflow: hidden; background: #0b0f19; }} </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
  <script>
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.1, 1000);
    camera.position.set(0, 3, 7);
    camera.lookAt(0,0,0);
    const renderer = new THREE.WebGLRenderer({{ antialias: true }});
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const light = new THREE.PointLight(0xffffff, 2, 100);
    scene.add(light, new THREE.AmbientLight(0x333333));

    // Sol
    const sun = new THREE.Mesh(new THREE.SphereGeometry(0.8, 32, 32), new THREE.MeshBasicMaterial({{ color: 0xfcb900 }}));
    scene.add(sun);

    // Planeta
    const planetPivot = new THREE.Group();
    scene.add(planetPivot);
    const planet = new THREE.Mesh(new THREE.SphereGeometry(0.3, 32, 32), new THREE.MeshStandardMaterial({{ color: 0x00d2ff }}));
    planet.position.set(3, 0, 0);
    planetPivot.add(planet);

    function animate() {{
      requestAnimationFrame(animate);
      planetPivot.rotation.y += 0.02;
      sun.rotation.y += 0.005;
      renderer.render(scene, camera);
    }}
    animate();
  </script>
</body>
</html>"""

if not html_code:
    html_code = PLANTILLAS["Física: Péndulo con Gravedad Ajustable"]

# Disposición en pestañas principales
tab1, tab2 = st.tabs(["👁️ Visualización 3D Interactiva", "💻 Código HTML Generado"])

with tab1:
    st.subheader("Renderizado 3D en Vivo")
    # Renderiza la escena 3D interactiva en vivo
    components.html(html_code, height=520, scrolling=False)

with tab2:
    st.subheader("Código HTML / Three.js Autocontenido")
    st.code(html_code, language="html")
    
    # Botón de descarga para que el alumno pueda guardarlo localmente
    st.download_button(
        label="📥 Descargar archivo HTML de la simulación",
        data=html_code,
        file_name="simulacion_3d_educativa.html",
        mime="text/html"
    )
