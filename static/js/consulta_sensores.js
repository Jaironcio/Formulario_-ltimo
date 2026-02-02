// JavaScript para Consulta de Reportes de Sensores
// Generación de PDF similar al formato del usuario

// Función para expandir/colapsar detalles
function toggleDetalle(detalleId) {
    const detalle = document.getElementById(detalleId);
    const button = event.target;
    
    if (detalle.style.display === 'none') {
        detalle.style.display = 'block';
        button.textContent = button.textContent.replace('Ver Detalle', 'Ocultar Detalle');
        button.style.background = '#6c757d';
    } else {
        detalle.style.display = 'none';
        button.textContent = button.textContent.replace('Ocultar Detalle', 'Ver Detalle');
        button.style.background = '#17a2b8';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const exportPdfBtn = document.getElementById('exportPdfSensoresBtn');
    
    if (exportPdfBtn) {
        exportPdfBtn.addEventListener('click', generarPDFSensores);
    }
    
    function generarPDFSensores() {
        const registros = document.querySelectorAll('.sensor-item');
        
        if (registros.length === 0) {
            alert('No hay registros para generar el PDF. Por favor, aplica filtros para buscar registros.');
            return;
        }
        
        // Obtener información del primer registro para el título
        const primerRegistro = registros[0];
        const fecha = primerRegistro.dataset.fecha;
        const turno = primerRegistro.dataset.turno;
        
        const { jsPDF } = window.jspdf;
        const pdf = new jsPDF('landscape', 'mm', 'a4');
        
        // Título principal
        pdf.setFontSize(16);
        pdf.setFont('helvetica', 'bold');
        pdf.text(`REPORTE DIARIO TURNO ${turno} ${fecha}`, 148, 15, { align: 'center' });
        
        // Subtítulo
        pdf.setFontSize(12);
        pdf.setFont('helvetica', 'normal');
        pdf.text('INFORME DE ALERTAS - SISTEMAS DE MONITOREO', 148, 22, { align: 'center' });
        
        // Preparar datos para la tabla
        const tableData = [];
        
        registros.forEach(registro => {
            const fechaRaw = registro.dataset.fecha;
            const centro = registro.dataset.centro;
            const sistema = registro.dataset.sistema;
            const equipo = registro.dataset.equipo;
            const tipo = registro.dataset.tipo;
            const estado = registro.dataset.estado;
            const limites = registro.dataset.limites;
            const observacion = registro.dataset.observacion || '-';
            
            // Convertir fecha a formato español
            const [year, month, day] = fechaRaw.split('-');
            const meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
            const fechaES = `${day} ${meses[parseInt(month) - 1]}, ${year}`;
            
            // Solo agregar si hay incidencia (no normal)
            if (estado !== 'NORMAL') {
                const totalAlto = estado === 'ALTO' ? '1' : '0';
                const totalBajo = estado === 'BAJO' ? '1' : '0';
                
                tableData.push([
                    fechaES,
                    centro,
                    sistema,
                    equipo,
                    tipo,
                    `LIMITE ${limites}`,
                    observacion,
                    totalAlto,
                    totalBajo
                ]);
            }
        });
        
        // Si no hay incidencias, mostrar mensaje
        if (tableData.length === 0) {
            pdf.setFontSize(14);
            pdf.setTextColor(40, 167, 69);
            pdf.text('✓ No se registraron incidencias en este período', 148, 50, { align: 'center' });
            pdf.setTextColor(0, 0, 0);
            
            // Agregar resumen de sensores normales
            pdf.setFontSize(11);
            pdf.text(`Total de sensores monitoreados: ${registros.length}`, 148, 60, { align: 'center' });
            pdf.text('Todos los sensores operando dentro de los límites normales', 148, 67, { align: 'center' });
        } else {
            // Generar tabla con incidencias
            pdf.autoTable({
                startY: 30,
                head: [['FECHA', 'PISCICULTURA', 'SISTEMA', 'EQUIPO', 'TIPO DE MEDICIÓN', 'INCIDENCIA', 'OBSERVACIÓN', 'TOTAL ALTO', 'TOTAL BAJO']],
                body: tableData,
                theme: 'grid',
                headStyles: {
                    fillColor: [0, 139, 139],
                    textColor: 255,
                    fontStyle: 'bold',
                    fontSize: 8,
                    halign: 'center'
                },
                bodyStyles: {
                    fontSize: 7
                },
                columnStyles: {
                    0: { cellWidth: 22, halign: 'center' },
                    1: { cellWidth: 28 },
                    2: { cellWidth: 35 },
                    3: { cellWidth: 40 },
                    4: { cellWidth: 28 },
                    5: { cellWidth: 32 },
                    6: { cellWidth: 38 },
                    7: { cellWidth: 18, halign: 'center' },
                    8: { cellWidth: 18, halign: 'center' }
                },
                alternateRowStyles: {
                    fillColor: [245, 245, 245]
                }
            });
            
            // Agregar resumen al final
            const finalY = pdf.lastAutoTable.finalY + 10;
            pdf.setFontSize(10);
            pdf.setFont('helvetica', 'bold');
            pdf.text('RESUMEN:', 14, finalY);
            
            pdf.setFont('helvetica', 'normal');
            const totalIncidencias = tableData.length;
            const totalAltos = tableData.filter(row => row[6] === '1').length;
            const totalBajos = tableData.filter(row => row[7] === '1').length;
            
            pdf.text(`Total de incidencias: ${totalIncidencias}`, 14, finalY + 7);
            pdf.text(`Sensores sobre límite (ALTO): ${totalAltos}`, 14, finalY + 14);
            pdf.text(`Sensores bajo límite (BAJO): ${totalBajos}`, 14, finalY + 21);
            pdf.text(`Total sensores monitoreados: ${registros.length}`, 14, finalY + 28);
        }
        
        // Guardar PDF
        const nombreArchivo = `Reporte_Sensores_${turno}_${fecha}.pdf`;
        pdf.save(nombreArchivo);
        
        // Mostrar mensaje de éxito
        mostrarMensaje('PDF generado exitosamente', 'success');
    }
    
    function mostrarMensaje(mensaje, tipo) {
        const alertDiv = document.createElement('div');
        alertDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            background: ${tipo === 'success' ? '#28a745' : '#dc3545'};
            color: white;
            border-radius: 6px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            z-index: 10000;
            font-weight: 600;
        `;
        alertDiv.textContent = mensaje;
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }
});

// Función para eliminar registro
function eliminarRegistro(id) {
    if (!confirm('¿Estás seguro de que deseas eliminar este registro?')) {
        return;
    }
    
    fetch(`/api/sensores/eliminar/${id}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Registro eliminado correctamente');
            location.reload();
        } else {
            alert('Error al eliminar: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al eliminar el registro');
    });
}

// Función para editar registro
function editarRegistro(id, estadoActual, observacionActual) {
    const nuevoEstado = prompt('Ingrese el nuevo estado (NORMAL, ALTO, BAJO):', estadoActual);
    
    if (nuevoEstado === null) {
        return; // Usuario canceló
    }
    
    if (!['NORMAL', 'ALTO', 'BAJO'].includes(nuevoEstado.toUpperCase())) {
        alert('Estado inválido. Debe ser: NORMAL, ALTO o BAJO');
        return;
    }
    
    const nuevaObservacion = prompt('Ingrese la nueva observación:', observacionActual || '');
    
    if (nuevaObservacion === null) {
        return; // Usuario canceló
    }
    
    fetch(`/api/sensores/actualizar/${id}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            estado: nuevoEstado.toUpperCase(),
            observacion: nuevaObservacion
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Registro actualizado correctamente');
            location.reload();
        } else {
            alert('Error al actualizar: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al actualizar el registro');
    });
}

// Función para eliminar reporte completo (todos los sensores de una fecha y turno)
function eliminarReporteCompleto(fecha, turno) {
    if (!confirm(`¿Estás seguro de que deseas eliminar TODOS los registros del ${fecha} turno ${turno}?\n\nEsta acción no se puede deshacer.`)) {
        return;
    }
    
    fetch(`/api/sensores/eliminar-reporte/?fecha=${fecha}&turno=${turno}`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert('Error al eliminar reporte: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al eliminar el reporte completo');
    });
}

// Función para obtener el CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
