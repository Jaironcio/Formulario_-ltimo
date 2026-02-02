// Sistema de Monitoreo de Sensores - Ideal Control
// Manejo de sesión y formulario dinámico

document.addEventListener('DOMContentLoaded', function() {
    // Variables globales
    let sensoresActuales = [];
    let sesionRegistros = [];
    
    // Elementos del DOM
    const centroSelect = document.getElementById('centro');
    const sistemaSelect = document.getElementById('sistema');
    const cargarSensoresBtn = document.getElementById('cargarSensoresBtn');
    const sensoresTable = document.getElementById('sensoresTable');
    const sensoresTableBody = document.getElementById('sensoresTableBody');
    const loadingMessage = document.getElementById('loadingMessage');
    const agregarAReporteBtn = document.getElementById('agregarAReporteBtn');
    const guardarReporteBtn = document.getElementById('guardarReporteBtn');
    const generarPDFBtn = document.getElementById('generarPDFBtn');
    const limpiarSesionBtn = document.getElementById('limpiarSesionBtn');
    const sessionList = document.getElementById('sessionList');
    const alertContainer = document.getElementById('alertContainer');
    
    // Event Listeners - con verificación de null
    if (centroSelect) centroSelect.addEventListener('change', cargarSistemas);
    if (sistemaSelect) sistemaSelect.addEventListener('change', habilitarBotonCargar);
    if (cargarSensoresBtn) cargarSensoresBtn.addEventListener('click', cargarSensores);
    if (agregarAReporteBtn) agregarAReporteBtn.addEventListener('click', agregarAReporte);
    if (guardarReporteBtn) guardarReporteBtn.addEventListener('click', guardarReporteCompleto);
    if (generarPDFBtn) generarPDFBtn.addEventListener('click', generarPDF);
    if (limpiarSesionBtn) limpiarSesionBtn.addEventListener('click', limpiarSesion);
    
    // Funciones
    function mostrarAlerta(mensaje, tipo = 'info') {
        if (!alertContainer) return;
        const alertClass = tipo === 'success' ? 'alert-success' : tipo === 'error' ? 'alert-error' : 'alert-info';
        alertContainer.innerHTML = `
            <div class="alert ${alertClass}">
                ${mensaje}
            </div>
        `;
        setTimeout(() => {
            if (alertContainer) alertContainer.innerHTML = '';
        }, 5000);
    }
    
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }
    
    async function cargarSistemas() {
        const centroId = centroSelect.value;
        
        if (!centroId) {
            sistemaSelect.innerHTML = '<option value="">Primero seleccione un centro</option>';
            sistemaSelect.disabled = true;
            cargarSensoresBtn.disabled = true;
            return;
        }
        
        try {
            const response = await fetch(`/api/sensores/sistemas/?centro_id=${centroId}`);
            const data = await response.json();
            
            if (data.error) {
                mostrarAlerta(data.error, 'error');
                return;
            }
            
            sistemaSelect.innerHTML = '<option value="">Seleccione sistema</option>';
            data.sistemas.forEach(sistema => {
                const option = document.createElement('option');
                option.value = sistema;
                option.textContent = sistema;
                sistemaSelect.appendChild(option);
            });
            
            sistemaSelect.disabled = false;
            
        } catch (error) {
            mostrarAlerta('Error al cargar sistemas: ' + error.message, 'error');
        }
    }
    
    function habilitarBotonCargar() {
        cargarSensoresBtn.disabled = !sistemaSelect.value;
    }
    
    async function cargarSensores() {
        const centroId = centroSelect.value;
        const sistema = sistemaSelect.value;
        
        if (!centroId || !sistema) {
            mostrarAlerta('Seleccione centro y sistema', 'error');
            return;
        }
        
        loadingMessage.style.display = 'block';
        sensoresTable.classList.remove('show');
        
        try {
            const response = await fetch(`/api/sensores/sensores/?centro_id=${centroId}&sistema=${sistema}`);
            const data = await response.json();
            
            if (data.error) {
                mostrarAlerta(data.error, 'error');
                loadingMessage.style.display = 'none';
                return;
            }
            
            sensoresActuales = data.sensores;
            renderizarSensores();
            
            loadingMessage.style.display = 'none';
            sensoresTable.classList.add('show');
            agregarAReporteBtn.style.display = 'inline-block';
            
        } catch (error) {
            mostrarAlerta('Error al cargar sensores: ' + error.message, 'error');
            loadingMessage.style.display = 'none';
        }
    }
    
    function renderizarSensores() {
        sensoresTableBody.innerHTML = '';
        
        sensoresActuales.forEach((sensor, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${sensor.equipo}</strong></td>
                <td>${sensor.tipo_medicion}</td>
                <td>
                    ${sensor.limite_min ? 'Min: ' + sensor.limite_min : ''} 
                    ${sensor.limite_max ? 'Max: ' + sensor.limite_max : ''}
                </td>
                <td>
                    <div class="estado-radio">
                        <label>
                            <input type="radio" name="estado_${index}" value="NORMAL" checked>
                            Normal
                        </label>
                        <label>
                            <input type="radio" name="estado_${index}" value="ALTO">
                            Alto
                        </label>
                        <label>
                            <input type="radio" name="estado_${index}" value="BAJO">
                            Bajo
                        </label>
                    </div>
                </td>
                <td>
                    <input type="text" 
                           id="obs_${index}" 
                           placeholder="Observación (opcional)"
                           style="width: 100%; padding: 6px; border: 1px solid #ddd; border-radius: 4px;">
                </td>
            `;
            sensoresTableBody.appendChild(row);
        });
    }
    
    function agregarAReporte() {
        const fecha = document.getElementById('fecha').value;
        const turno = document.getElementById('turno').value;
        const responsable = document.getElementById('responsable').value;
        const centroId = centroSelect.value;
        const centroNombre = centroSelect.options[centroSelect.selectedIndex].text;
        const sistema = sistemaSelect.value;
        
        if (!fecha || !turno || !responsable) {
            mostrarAlerta('Complete la información general (fecha, turno, responsable)', 'error');
            return;
        }
        
        if (!centroId || !sistema) {
            mostrarAlerta('Seleccione centro y sistema', 'error');
            return;
        }
        
        // Recopilar estados de sensores
        const registros = [];
        sensoresActuales.forEach((sensor, index) => {
            const estadoRadio = document.querySelector(`input[name="estado_${index}"]:checked`);
            const observacion = document.getElementById(`obs_${index}`).value;
            
            if (estadoRadio) {
                registros.push({
                    sensor_id: sensor.id,
                    sensor_nombre: sensor.equipo,
                    centro_id: centroId,
                    centro_nombre: centroNombre,
                    sistema: sistema,
                    estado: estadoRadio.value,
                    observacion: observacion,
                    tipo_medicion: sensor.tipo_medicion,
                    limites: `${sensor.limite_min || ''} - ${sensor.limite_max || ''}`
                });
            }
        });
        
        if (registros.length === 0) {
            mostrarAlerta('No hay sensores para agregar', 'error');
            return;
        }
        
        // Agregar a sesión
        sesionRegistros.push({
            centro: centroNombre,
            sistema: sistema,
            registros: registros,
            fecha: fecha,
            turno: turno,
            responsable: responsable
        });
        
        actualizarVistaSession();
        mostrarAlerta(`${registros.length} sensores de ${centroNombre} - ${sistema} agregados al reporte`, 'success');
        
        // Limpiar formulario para siguiente centro/sistema
        sensoresTable.classList.remove('show');
        agregarAReporteBtn.style.display = 'none';
        sistemaSelect.value = '';
        cargarSensoresBtn.disabled = true;
    }
    
    function actualizarVistaSession() {
        if (sesionRegistros.length === 0) {
            sessionList.innerHTML = '<p style="text-align: center; color: #6c757d;">No hay sensores agregados aún</p>';
            guardarReporteBtn.style.display = 'none';
            generarPDFBtn.style.display = 'none';
            limpiarSesionBtn.style.display = 'none';
            return;
        }
        
        let html = '';
        let totalSensores = 0;
        
        sesionRegistros.forEach((grupo, index) => {
            const normales = grupo.registros.filter(r => r.estado === 'NORMAL').length;
            const altos = grupo.registros.filter(r => r.estado === 'ALTO').length;
            const bajos = grupo.registros.filter(r => r.estado === 'BAJO').length;
            totalSensores += grupo.registros.length;
            
            html += `
                <div class="session-item">
                    <div class="session-item-info">
                        <strong>${grupo.centro} - ${grupo.sistema}</strong><br>
                        <small>${grupo.registros.length} sensores: 
                            <span class="badge badge-normal">${normales} Normal</span>
                            <span class="badge badge-alto">${altos} Alto</span>
                            <span class="badge badge-bajo">${bajos} Bajo</span>
                        </small>
                    </div>
                    <div class="session-item-actions">
                        <button class="btn btn-secondary" onclick="eliminarGrupo(${index})" style="padding: 6px 12px;">
                            Eliminar
                        </button>
                    </div>
                </div>
            `;
        });
        
        sessionList.innerHTML = `
            <div style="margin-bottom: 15px; padding: 10px; background: white; border-radius: 4px;">
                <strong>Total: ${totalSensores} sensores en ${sesionRegistros.length} grupo(s)</strong>
            </div>
            ${html}
        `;
        
        guardarReporteBtn.style.display = 'inline-block';
        generarPDFBtn.style.display = 'inline-block';
        limpiarSesionBtn.style.display = 'inline-block';
    }
    
    window.eliminarGrupo = function(index) {
        if (confirm('¿Eliminar este grupo de sensores?')) {
            sesionRegistros.splice(index, 1);
            actualizarVistaSession();
            mostrarAlerta('Grupo eliminado', 'info');
        }
    };
    
    async function guardarReporteCompleto() {
        if (sesionRegistros.length === 0) {
            mostrarAlerta('No hay sensores para guardar', 'error');
            return;
        }
        
        const fecha = document.getElementById('fecha').value;
        const turno = document.getElementById('turno').value;
        const responsable = document.getElementById('responsable').value;
        
        // Consolidar todos los registros
        const todosLosRegistros = [];
        sesionRegistros.forEach(grupo => {
            todosLosRegistros.push(...grupo.registros);
        });
        
        const datos = {
            fecha: fecha,
            turno: turno,
            responsable: responsable,
            registros: todosLosRegistros
        };
        
        guardarReporteBtn.disabled = true;
        guardarReporteBtn.textContent = 'Guardando...';
        
        try {
            const response = await fetch('/api/sensores/guardar/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify(datos)
            });
            
            const result = await response.json();
            
            if (result.success) {
                mostrarAlerta(result.mensaje, 'success');
                // Limpiar sesión después de guardar
                setTimeout(() => {
                    limpiarSesion();
                }, 2000);
            } else {
                mostrarAlerta(result.error || 'Error al guardar', 'error');
            }
            
        } catch (error) {
            mostrarAlerta('Error al guardar: ' + error.message, 'error');
        } finally {
            guardarReporteBtn.disabled = false;
            guardarReporteBtn.textContent = '💾 Guardar Reporte Completo';
        }
    }
    
    function generarPDF() {
        if (sesionRegistros.length === 0) {
            mostrarAlerta('No hay datos para generar PDF', 'error');
            return;
        }
        
        const fecha = document.getElementById('fecha').value;
        const turno = document.getElementById('turno').value;
        
        const { jsPDF } = window.jspdf;
        const pdf = new jsPDF('landscape', 'mm', 'a4');
        
        // Título
        pdf.setFontSize(16);
        pdf.setFont('helvetica', 'bold');
        pdf.text(`REPORTE DIARIO TURNO ${turno} ${fecha}`, 148, 15, { align: 'center' });
        
        pdf.setFontSize(12);
        pdf.setFont('helvetica', 'normal');
        pdf.text('INFORME DE ALERTAS - SISTEMAS DE MONITOREO', 148, 22, { align: 'center' });
        
        // Preparar datos para la tabla
        const tableData = [];
        sesionRegistros.forEach(grupo => {
            grupo.registros.forEach(reg => {
                if (reg.estado !== 'NORMAL') {  // Solo incidencias
                    tableData.push([
                        fecha,
                        reg.centro_nombre,
                        reg.sistema,
                        reg.equipo,
                        reg.tipo_medicion,
                        reg.limites,
                        reg.estado === 'ALTO' ? '1' : '0',
                        reg.estado === 'BAJO' ? '1' : '0'
                    ]);
                }
            });
        });
        
        // Generar tabla
        pdf.autoTable({
            startY: 30,
            head: [['FECHA', 'PISCICULTURA', 'SISTEMA', 'EQUIPO', 'TIPO DE MEDICIÓN', 'INCIDENCIA', 'TOTAL ALTO', 'TOTAL BAJO']],
            body: tableData,
            theme: 'grid',
            headStyles: {
                fillColor: [0, 139, 139],
                textColor: 255,
                fontStyle: 'bold',
                fontSize: 9
            },
            bodyStyles: {
                fontSize: 8
            },
            columnStyles: {
                0: { cellWidth: 25 },
                1: { cellWidth: 35 },
                2: { cellWidth: 45 },
                3: { cellWidth: 50 },
                4: { cellWidth: 35 },
                5: { cellWidth: 40 },
                6: { cellWidth: 20 },
                7: { cellWidth: 20 }
            }
        });
        
        // Guardar PDF
        pdf.save(`Reporte_Sensores_${turno}_${fecha}.pdf`);
        mostrarAlerta('PDF generado exitosamente', 'success');
    }
    
    function limpiarSesion() {
        if (sesionRegistros.length > 0 && !confirm('¿Limpiar todos los datos de la sesión?')) {
            return;
        }
        
        sesionRegistros = [];
        sensoresActuales = [];
        actualizarVistaSession();
        
        // Limpiar formulario
        sensoresTable.classList.remove('show');
        agregarAReporteBtn.style.display = 'none';
        centroSelect.value = '';
        sistemaSelect.value = '';
        sistemaSelect.disabled = true;
        cargarSensoresBtn.disabled = true;
        
        mostrarAlerta('Sesión limpiada', 'info');
    }
    
    // ============================================================================
    // FUNCIONALIDAD PARA VER REPORTES REGISTRADOS
    // ============================================================================
    
    const verReportesBtn = document.getElementById('verReportesBtn');
    const modalReportes = document.getElementById('modalReportes');
    const cerrarModalBtn = document.getElementById('cerrarModalBtn');
    const loadingReportes = document.getElementById('loadingReportes');
    const listaReportes = document.getElementById('listaReportes');
    const detalleReporte = document.getElementById('detalleReporte');
    const volverListaBtn = document.getElementById('volverListaBtn');
    const tituloDetalle = document.getElementById('tituloDetalle');
    const contenidoDetalle = document.getElementById('contenidoDetalle');
    
    verReportesBtn.addEventListener('click', abrirModalReportes);
    cerrarModalBtn.addEventListener('click', cerrarModal);
    volverListaBtn.addEventListener('click', volverALista);
    
    async function abrirModalReportes() {
        modalReportes.style.display = 'block';
        loadingReportes.style.display = 'block';
        listaReportes.innerHTML = '';
        detalleReporte.style.display = 'none';
        
        try {
            const response = await fetch('/api/sensores/listar/');
            const data = await response.json();
            
            if (data.success) {
                renderizarListaReportes(data.reportes);
            } else {
                listaReportes.innerHTML = '<p style="text-align: center; color: #e74c3c;">Error al cargar reportes</p>';
            }
        } catch (error) {
            listaReportes.innerHTML = '<p style="text-align: center; color: #e74c3c;">Error: ' + error.message + '</p>';
        } finally {
            loadingReportes.style.display = 'none';
        }
    }
    
    function renderizarListaReportes(reportes) {
        if (reportes.length === 0) {
            listaReportes.innerHTML = '<p style="text-align: center; color: #6c757d; padding: 40px;">No hay reportes registrados aún</p>';
            return;
        }
        
        let html = '<div style="display: grid; gap: 15px;">';
        
        reportes.forEach(reporte => {
            const incidencias = reporte.total_altos + reporte.total_bajos;
            html += `
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #008b8b; cursor: pointer; transition: all 0.3s;"
                     onmouseover="this.style.background='#e9ecef'" 
                     onmouseout="this.style.background='#f8f9fa'"
                     onclick="verDetalleReporte('${reporte.fecha}', '${reporte.turno}')">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                        <div>
                            <h4 style="margin: 0 0 5px 0; color: #333;">
                                📅 ${reporte.fecha} - Turno ${reporte.turno}
                            </h4>
                            <p style="margin: 0; color: #6c757d; font-size: 14px;">
                                👤 Responsable: ${reporte.responsable}
                            </p>
                        </div>
                        <div style="text-align: right;">
                            <span style="background: ${incidencias > 0 ? '#dc3545' : '#28a745'}; color: white; padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;">
                                ${incidencias} Incidencias
                            </span>
                        </div>
                    </div>
                    <div style="display: flex; gap: 15px; margin-top: 10px; font-size: 14px;">
                        <span>🏢 Centros: ${reporte.centros}</span>
                    </div>
                    <div style="display: flex; gap: 15px; margin-top: 10px; font-size: 13px;">
                        <span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 4px;">
                            ✓ ${reporte.total_normales} Normal
                        </span>
                        <span style="background: #dc3545; color: white; padding: 3px 8px; border-radius: 4px;">
                            ↑ ${reporte.total_altos} Alto
                        </span>
                        <span style="background: #ffc107; color: #333; padding: 3px 8px; border-radius: 4px;">
                            ↓ ${reporte.total_bajos} Bajo
                        </span>
                        <span style="color: #6c757d;">
                            📊 Total: ${reporte.total_sensores} sensores
                        </span>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        listaReportes.innerHTML = html;
    }
    
    window.verDetalleReporte = async function(fecha, turno) {
        listaReportes.style.display = 'none';
        detalleReporte.style.display = 'block';
        tituloDetalle.textContent = `Detalle del Reporte: ${fecha} - Turno ${turno}`;
        contenidoDetalle.innerHTML = '<p style="text-align: center; padding: 20px;">Cargando detalle...</p>';
        
        try {
            const response = await fetch(`/api/sensores/detalle/?fecha=${fecha}&turno=${turno}`);
            const data = await response.json();
            
            if (data.success) {
                renderizarDetalleReporte(data.registros);
            } else {
                contenidoDetalle.innerHTML = '<p style="color: #e74c3c;">Error al cargar detalle</p>';
            }
        } catch (error) {
            contenidoDetalle.innerHTML = '<p style="color: #e74c3c;">Error: ' + error.message + '</p>';
        }
    };
    
    function renderizarDetalleReporte(registros) {
        if (registros.length === 0) {
            contenidoDetalle.innerHTML = '<p style="text-align: center; color: #6c757d;">No hay registros</p>';
            return;
        }
        
        // Agrupar por centro y sistema
        const grupos = {};
        registros.forEach(reg => {
            const key = `${reg.centro} - ${reg.sistema}`;
            if (!grupos[key]) {
                grupos[key] = [];
            }
            grupos[key].push(reg);
        });
        
        let html = '';
        
        for (const [grupo, sensores] of Object.entries(grupos)) {
            const incidencias = sensores.filter(s => s.estado !== 'NORMAL').length;
            
            html += `
                <div style="background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
                    <h4 style="color: #008b8b; margin-top: 0; margin-bottom: 15px;">
                        ${grupo} 
                        <span style="font-size: 14px; color: #6c757d; font-weight: normal;">
                            (${sensores.length} sensores, ${incidencias} incidencias)
                        </span>
                    </h4>
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr style="background: #f8f9fa; border-bottom: 2px solid #e0e0e0;">
                                <th style="padding: 10px; text-align: left;">Equipo</th>
                                <th style="padding: 10px; text-align: left;">Tipo Medición</th>
                                <th style="padding: 10px; text-align: left;">Límites</th>
                                <th style="padding: 10px; text-align: center;">Estado</th>
                                <th style="padding: 10px; text-align: left;">Observación</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            sensores.forEach(sensor => {
                const estadoColor = sensor.estado === 'NORMAL' ? '#28a745' : 
                                   sensor.estado === 'ALTO' ? '#dc3545' : '#ffc107';
                const estadoTexto = sensor.estado === 'NORMAL' ? '✓ Normal' : 
                                   sensor.estado === 'ALTO' ? '↑ Alto' : '↓ Bajo';
                
                html += `
                    <tr style="border-bottom: 1px solid #e0e0e0;">
                        <td style="padding: 10px;">${sensor.equipo}</td>
                        <td style="padding: 10px;">${sensor.tipo_medicion}</td>
                        <td style="padding: 10px; font-size: 12px; color: #6c757d;">
                            ${sensor.limite_min || '-'} / ${sensor.limite_max || '-'}
                        </td>
                        <td style="padding: 10px; text-align: center;">
                            <span style="background: ${estadoColor}; color: white; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: bold;">
                                ${estadoTexto}
                            </span>
                        </td>
                        <td style="padding: 10px; font-size: 13px; color: #555;">
                            ${sensor.observacion || '-'}
                        </td>
                    </tr>
                `;
            });
            
            html += `
                        </tbody>
                    </table>
                </div>
            `;
        }
        
        contenidoDetalle.innerHTML = html;
    }
    
    function volverALista() {
        detalleReporte.style.display = 'none';
        listaReportes.style.display = 'block';
    }
    
    function cerrarModal() {
        modalReportes.style.display = 'none';
        detalleReporte.style.display = 'none';
        listaReportes.style.display = 'block';
    }
});
