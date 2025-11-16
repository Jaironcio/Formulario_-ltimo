// static/js/reporte.js

document.addEventListener('DOMContentLoaded', function () {
    
    // --- 1. Obtener Elementos ---
    const aplicarBtn = document.getElementById('aplicarFiltrosBtn');
    const resetBtn = document.getElementById('resetFiltrosBtn');
    
    const filtroFecha = document.getElementById('filtroFecha');
    const filtroTipo = document.getElementById('filtroTipoIncidencia');
    const filtroTurno = document.getElementById('filtroTurno');
    const filtroCentro = document.getElementById('filtroCentro');
    
    // --- 2. Poner los valores actuales en los filtros ---
    const currentParams = new URLSearchParams(window.location.search);
    
    filtroFecha.value = currentParams.get('fecha') || '';
    filtroTipo.value = currentParams.get('tipo') || '';
    filtroTurno.value = currentParams.get('turno') || '';
    filtroCentro.value = currentParams.get('centro') || '';

    // --- 3. Lógica de Botones de Filtro ---
    if (aplicarBtn) {
        aplicarBtn.addEventListener('click', function () {
            const params = new URLSearchParams();
            if (filtroFecha.value) { params.set('fecha', filtroFecha.value); }
            if (filtroTipo.value) { params.set('tipo', filtroTipo.value); }
            if (filtroTurno.value) { params.set('turno', filtroTurno.value); }
            if (filtroCentro.value) { params.set('centro', filtroCentro.value); }
            window.location.search = params.toString();
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', function () {
            window.location.pathname = '/reporte/';
        });
    }
    
    // --- 4. Actualizar contadores ---
    const incidenciasFiltradas = document.querySelectorAll('.incidencia-card').length;
    const incidenciasFiltradasHeader = document.getElementById('incidenciasFiltradasHeader');
    if (incidenciasFiltradasHeader) {
        incidenciasFiltradasHeader.textContent = incidenciasFiltradas;
    }

    // --- 5. Lógica de Botones CRUD (Eliminar) ---
    
    function getCsrfToken() {
        const tokenElement = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (tokenElement) { return tokenElement.value; }
        console.error('¡No se encontró el CSRF Token! Asegúrate de añadir {% csrf_token %} en reporte.html');
        return null;
    }

    const allDeleteButtons = document.querySelectorAll('.delete-btn');
    
    allDeleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const card = e.target.closest('.incidencia-card');
            const incidenciaId = e.target.dataset.id;
            const csrfToken = getCsrfToken();

            if (!csrfToken || !confirm(`¿Estás seguro de que quieres eliminar esta incidencia?`)) {
                return;
            }

            fetch(`/api/incidencia/${incidenciaId}/delete/`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': csrfToken }
            })
            .then(response => {
                if (response.ok) {
                    card.style.transition = 'all 0.5s ease';
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.8)';
                    setTimeout(() => {
                        card.remove();
                        const incidenciasActuales = document.querySelectorAll('.incidencia-card').length;
                        document.getElementById('incidenciasFiltradasHeader').textContent = incidenciasActuales;
                    }, 500);
                } else {
                    alert('Error: No se pudo eliminar la incidencia.');
                }
            })
            .catch(error => console.error('Error en el fetch DELETE:', error));
        });
    });

    // --- 6. NUEVO: Lógica de Exportar PDF (Avanzado 2x2) ---
    
    const pdfButton = document.getElementById('exportPdfBtn');

    if (pdfButton) {
        // Marcamos la función como 'async' para poder usar 'await'
        pdfButton.addEventListener('click', async function() {
            
            if (typeof window.html2canvas === 'undefined' || typeof window.jspdf === 'undefined') {
                alert('Error: Las librerías PDF no están cargadas.');
                return;
            }

            const { jsPDF } = window.jspdf;
            const allCards = document.querySelectorAll('.incidencia-card'); // Obtenemos todas las tarjetas
            
            if (allCards.length === 0) {
                alert('No hay incidencias para exportar.');
                return;
            }

            const originalText = pdfButton.innerHTML;
            pdfButton.innerHTML = 'Generando 0%...';
            pdfButton.disabled = true;

            const pdf = new jsPDF('p', 'mm', 'a4'); // PDF A4 (Portrait: 210 x 297 mm)
            const pageWidth = pdf.internal.pageSize.getWidth();
            const pageHeight = pdf.internal.pageSize.getHeight();
            
            // --- Configuración del Layout 2x2 ---
            const margin = 10; // Margen de 10mm
            const cardWidth = (pageWidth / 2) - (margin * 1.5); // Ancho de cada tarjeta
            
            let x = margin;
            let y = margin;
            
            // Usamos un bucle 'for' para poder usar 'await' dentro
            for (let i = 0; i < allCards.length; i++) {
                const card = allCards[i];
                
                // Actualizar progreso al usuario
                pdfButton.innerHTML = `Generando ${Math.round((i / allCards.length) * 100)}%...`;

                // 1. Fotografiar la tarjeta
                const canvas = await html2canvas(card, { scale: 2 }); // 'await' pausa el bucle
                const imgData = canvas.toDataURL('image/png');
                
                // 2. Calcular el alto proporcional de la imagen
                const imgProps = pdf.getImageProperties(imgData);
                const cardHeight = (imgProps.height * cardWidth) / imgProps.width;

                // 3. Revisar si la tarjeta cabe en la página actual
                if (y + cardHeight + margin > pageHeight) {
                    pdf.addPage(); // Si no cabe, añade página nueva
                    x = margin;    // Resetea X
                    y = margin;    // Resetea Y
                }

                // 4. Dibujar la imagen en el PDF
                pdf.addImage(imgData, 'PNG', x, y, cardWidth, cardHeight);
                
                // 5. Mover el "cursor" (x, y) a la siguiente posición
                if (i % 2 === 0) {
                    // Es la primera columna (impar), mover a la segunda
                    x = (pageWidth / 2) + (margin / 2);
                } else {
                    // Es la segunda columna (par), mover a la siguiente fila
                    x = margin;
                    y += cardHeight + margin;
                }
            }

            // 6. Guardar el PDF y restaurar el botón
            pdf.save('reporte_incidencias_2x2.pdf');
            pdfButton.innerHTML = originalText;
            pdfButton.disabled = false;
        });
    }

});