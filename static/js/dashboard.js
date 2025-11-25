// static/js/dashboard.js

(function(
    chartCentroLabels, chartCentroData,
    chartTendenciaLabels, chartTendenciaData,
    chartTiposData,
    chartOperarioLabels, chartOperarioData,
    chartClasificacionLabels, chartClasificacionData,
    chartCategoriasLabels, chartCategoriasData
) {
    
    document.addEventListener('DOMContentLoaded', function() {
        
        // --- SECCIONES 1-6: LÓGICA DE GRÁFICOS ---
        
        // --- 1. Gráfico "Incidencias por Centro" (Barras) ---
        const ctxCentro = document.getElementById('chartIncidenciasCentro');
        if (ctxCentro && chartCentroLabels && chartCentroData) {
            if (chartCentroData.length === 0) {
                ctxCentro.parentElement.innerHTML = "<h2>📊 Incidencias por Centro</h2><p class='loading-message'>No hay datos.</p>";
            } else {
                new Chart(ctxCentro, {
                    type: 'bar',
                    data: { labels: chartCentroLabels, datasets: [{ label: 'N° de Incidencias', data: chartCentroData, backgroundColor: 'rgba(0, 139, 139, 0.7)', borderWidth: 1 }] },
                    options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }, plugins: { legend: { display: false } } }
                });
            }
        }
        
        // --- 2. Gráfico "Tendencia Temporal" (Líneas) ---
        const ctxTendencia = document.getElementById('chartTendencia');
        if (ctxTendencia && chartTendenciaLabels && chartTendenciaData) {
            if (chartTendenciaData.length === 0) {
                ctxTendencia.parentElement.innerHTML = "<h2>📈 Tendencia Temporal</h2><p class='loading-message'>No hay datos.</p>";
            } else {
                new Chart(ctxTendencia, {
                    type: 'line',
                    data: { labels: chartTendenciaLabels, datasets: [{ label: 'N° de Incidencias', data: chartTendenciaData, fill: true, backgroundColor: 'rgba(0, 139, 139, 0.2)', borderColor: 'rgba(0, 139, 139, 1)', tension: 0.1 }] },
                    options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }, plugins: { legend: { display: false } } }
                });
            }
        }

        // --- 3. Gráfico "Tipos de Incidencia" (Doughnut) ---
        const ctxTipos = document.getElementById('chartTipos');
        if (ctxTipos && chartTiposData) {
            if (chartTiposData.every(item => item === 0)) {
                ctxTipos.parentElement.innerHTML = "<h2>🔄 Tipos de Incidencia</h2><p class='loading-message'>No hay datos.</p>";
            } else {
                new Chart(ctxTipos, {
                    type: 'doughnut',
                    data: { labels: ['Módulos/Estanques', 'Sensores'], datasets: [{ data: chartTiposData, backgroundColor: ['rgba(0, 139, 139, 0.7)', 'rgba(255, 159, 64, 0.7)'], borderWidth: 2 }] },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } }
                });
            }
        }

        // --- 4. Gráfico "Operarios" (Barras Horizontales) ---
        const ctxOperarios = document.getElementById('chartOperarios');
        if (ctxOperarios && chartOperarioLabels && chartOperarioData) {
            if (chartOperarioData.length === 0) {
                ctxOperarios.parentElement.innerHTML = "<h2>👥 Operarios que Más Responden</h2><p class='loading-message'>No hay datos.</p>";
            } else {
                new Chart(ctxOperarios, {
                    type: 'bar',
                    data: { labels: chartOperarioLabels, datasets: [{ label: 'N° de Respuestas', data: chartOperarioData, backgroundColor: 'rgba(75, 192, 192, 0.7)', borderWidth: 1 }] },
                    options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, scales: { x: { beginAtZero: true, ticks: { stepSize: 1 } } }, plugins: { legend: { display: false } } }
                });
            }
        }

        // --- 5. Gráfico "Clasificación" (Pie) ---
        const ctxClasificacion = document.getElementById('chartClasificacion');
        if (ctxClasificacion && chartClasificacionLabels && chartClasificacionData) {
            if (chartClasificacionData.length === 0) {
                ctxClasificacion.parentElement.innerHTML = "<h2>🏷️ Clasificación de Incidencias</h2><p class='loading-message'>No hay datos.</p>";
            } else {
                new Chart(ctxClasificacion, {
                    type: 'pie',
                    data: { labels: chartClasificacionLabels, datasets: [{ data: chartClasificacionData, backgroundColor: ['rgba(255, 99, 132, 0.7)','rgba(54, 162, 235, 0.7)','rgba(255, 206, 86, 0.7)','rgba(75, 192, 192, 0.7)','rgba(153, 102, 255, 0.7)','rgba(255, 159, 64, 0.7)'], borderWidth: 1 }] },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } }
                });
            }
        }

        // --- 6. NUEVO: Gráfico "Categorías" (Pie) ---
        const ctxCategorias = document.getElementById('chartCategorias');
        if (ctxCategorias && chartCategoriasLabels && chartCategoriasData) {
            // Verificar si hay datos (suma > 0)
            const sumaCategorias = chartCategoriasData.reduce((a, b) => a + b, 0);
            
            if (sumaCategorias === 0) {
                ctxCategorias.parentElement.innerHTML = "<h3>Distribución por Categoría Mayor</h3><p class='loading-message'>No hay datos.</p>";
            } else {
                new Chart(ctxCategorias, {
                    type: 'pie',
                    data: { 
                        labels: chartCategoriasLabels, 
                        datasets: [{ 
                            data: chartCategoriasData, 
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.8)',  // Falla Operacional (Rojo)
                                'rgba(54, 162, 235, 0.8)',  // Falla Sensores (Azul)
                                'rgba(255, 206, 86, 0.8)',  // Eléctricos (Amarillo)
                                'rgba(75, 192, 192, 0.8)',  // Normal (Verde)
                                'rgba(153, 102, 255, 0.8)', // Sin Comunicación (Morado)
                                'rgba(201, 203, 207, 0.8)'  // Otros (Gris)
                            ], 
                            borderWidth: 1 
                        }] 
                    },
                    options: { 
                        responsive: true, 
                        maintainAspectRatio: false, 
                        plugins: { legend: { position: 'bottom' } } 
                    }
                });
            }
        }

        // --- 7. Lógica de Filtros (Sin cambios) ---
        const actualizarBtn = document.getElementById('actualizarDashboard');
        const filtroFecha = document.getElementById('dashboardFiltroFecha');
        const filtroCentro = document.getElementById('dashboardFiltroCentro');

        if (actualizarBtn) {
            actualizarBtn.addEventListener('click', function() {
                const params = new URLSearchParams();
                if (filtroFecha.value && filtroFecha.value !== 'all') {
                    params.set('periodo', filtroFecha.value);
                }
                if (filtroCentro.value) {
                    params.set('centro', filtroCentro.value);
                }
                window.location.search = params.toString();
            });
        }

        // --- 7. Exportar Dashboard a PDF (LÓGICA CORREGIDA) ---
        const exportPdfBtn = document.getElementById('exportDashboardPdfBtn');
        if (exportPdfBtn) {
            
            exportPdfBtn.addEventListener('click', async function() {
                
                if (typeof window.html2canvas === 'undefined' || typeof window.jspdf === 'undefined') {
                    alert('Error: Librerías PDF no están cargadas.');
                    return;
                }

                // 1. Elementos a capturar (¡Ahora incluimos los títulos!)
                const elementsToCapture = [
                    document.querySelector('.dashboard-container h1'),
                    document.querySelector('.dashboard-container .dashboard-subtitle'),
                    document.querySelector('.metrics-grid'),
                    document.querySelector('.charts-grid'),
                    document.querySelector('.kpi-section')
                ];

                const originalText = exportPdfBtn.innerHTML;
                exportPdfBtn.innerHTML = 'Generando...';
                exportPdfBtn.disabled = true;

                const { jsPDF } = window.jspdf;
                const pdf = new jsPDF('p', 'mm', 'a4');
                const pageWidth = pdf.internal.pageSize.getWidth();
                const pageHeight = pdf.internal.pageSize.getHeight();
                const margin = 15;
                const contentWidth = pageWidth - (margin * 2);
                let yCursor = margin; // El "cursor" que baja por la página

                try {
                    // Función helper para añadir secciones
                    async function addSection(element) {
                        if (!element) return; // Si el elemento no existe, saltar
                        
                        // Tomamos la "foto"
                        const canvas = await html2canvas(element, { scale: 2 });
                        const imgData = canvas.toDataURL('image/png');
                        
                        // Calculamos el alto proporcional
                        const imgProps = pdf.getImageProperties(imgData);
                        const imgHeight = (imgProps.height * contentWidth) / imgProps.width;

                        // Revisar si cabe en la página actual
                        if (yCursor + imgHeight > pageHeight - margin) {
                            pdf.addPage(); // Si no cabe, página nueva
                            yCursor = margin; // Resetear cursor
                        }
                        
                        // Añadir la "foto" al PDF
                        pdf.addImage(imgData, 'PNG', margin, yCursor, contentWidth, imgHeight);
                        
                        // --- ESTA ES LA CORRECCIÓN ---
                        // Reducimos el espacio entre secciones
                        if (element.tagName === 'H1' || element.tagName === 'P') {
                             yCursor += imgHeight + 5; // Menos espacio después de títulos
                        } else {
                             yCursor += imgHeight + 10; // Espacio normal después de un bloque
                        }
                    }

                    // 2. Capturar y añadir cada sección en orden
                    for (const el of elementsToCapture) {
                        await addSection(el);
                    }

                    // 3. Guardar el PDF
                    pdf.save('dashboard_reporte.pdf');

                } catch (e) {
                    console.error("Error al generar el PDF:", e);
                    alert("Hubo un error al generar el PDF.");
                } finally {
                    // 4. Restaurar el botón
                    exportPdfBtn.innerHTML = originalText;
                    exportPdfBtn.disabled = false;
                }
            });
        }

    });

})(
    window.CHART_CENTRO_LABELS, window.CHART_CENTRO_DATA,
    window.CHART_TENDENCIA_LABELS, window.CHART_TENDENCIA_DATA,
    window.CHART_TIPOS_DATA,
    window.CHART_OPERARIO_LABELS, window.CHART_OPERARIO_DATA,
    window.CHART_CLASIFICACION_LABELS, window.CHART_CLASIFICACION_DATA,
    window.CHART_CATEGORIAS_LABELS, window.CHART_CATEGORIAS_DATA
);