// Reporte Ejecutivo de Turno - Codigo separado para facilitar mantenimiento

document.addEventListener('DOMContentLoaded', function () {
    
    const reporteEjecutivoBtn = document.getElementById('exportReporteEjecutivoBtn');
    
    if (reporteEjecutivoBtn) {
        reporteEjecutivoBtn.addEventListener('click', function() {
            
            if (typeof window.jspdf === 'undefined') {
                alert('Error: La libreria jsPDF no esta cargada.');
                return;
            }
            
            const allCards = document.querySelectorAll('.incidencia-card-premium');
            
            const originalText = reporteEjecutivoBtn.innerHTML;
            reporteEjecutivoBtn.innerHTML = '📊 Generando...';
            reporteEjecutivoBtn.disabled = true;
            
            try {
                const { jsPDF } = window.jspdf;
                const pdf = new jsPDF('l', 'mm', 'a4');
                const pageWidth = pdf.internal.pageSize.getWidth();
                const pageHeight = pdf.internal.pageSize.getHeight();
                
                const colorPrimario = [0, 139, 139];
                const colorVerde = [40, 167, 69];
                const colorAmarillo = [255, 193, 7];
                const colorRojo = [220, 53, 69];
                const colorGris = [108, 117, 125];
                
                const centrosPCC = ['Liquiñe', 'Cipreses', 'Trafún'];
                const centrosData = {};
                const turnosData = { 'Mañana': 0, 'Tarde': 0, 'Noche': 0 };
                
                centrosPCC.forEach(centro => {
                    centrosData[centro] = { 
                        count: 0, 
                        tipos: new Set(), 
                        estanques: new Set(), 
                        turnos: new Set(), 
                        critico: false,
                        incidencias: []
                    };
                });
                
                allCards.forEach(card => {
                    const centroEl = card.querySelector('.centro-nombre');
                    const tipoFallaEl = card.querySelector('.falla-descripcion');
                    
                    // Buscar todos los items de ubicacion
                    const ubicacionItems = card.querySelectorAll('.ubicacion-item');
                    let moduloEl = null;
                    let estanqueEl = null;
                    let turnoEl = null;
                    
                    ubicacionItems.forEach(item => {
                        const label = item.querySelector('.ubi-label');
                        if (label) {
                            const labelText = label.textContent.trim();
                            if (labelText.includes('Módulo') || labelText.includes('Modulo')) {
                                moduloEl = item.querySelector('.ubi-value');
                            } else if (labelText.includes('Estanque')) {
                                estanqueEl = item.querySelector('.ubi-value');
                            } else if (labelText.includes('Turno')) {
                                turnoEl = item.querySelector('.ubi-value');
                            }
                        }
                    });
                    
                    const horaEl = card.querySelector('.hora-valor');
                    const kpiValueEl = card.querySelector('.kpi-value');
                    const kpiStatusEl = card.querySelector('.kpi-status');
                    
                    const centro = centroEl ? centroEl.textContent.trim() : '';
                    const tipoFalla = tipoFallaEl ? tipoFallaEl.textContent.trim() : 'Sin tipo';
                    let estanque = estanqueEl ? estanqueEl.textContent.trim() : '';
                    let modulo = moduloEl ? moduloEl.textContent.trim() : '';
                    const turno = turnoEl ? turnoEl.textContent.trim() : '';
                    const hora = horaEl ? horaEl.textContent.trim() : '--:--';
                    
                    // Limpiar valores N/A
                    if (estanque === 'N/A') estanque = '';
                    if (modulo === 'N/A') modulo = '';
                    
                    // Extraer solo el numero del estanque si viene con texto
                    if (estanque && estanque.includes('Estanque')) {
                        estanque = estanque.replace('Estanque', '').trim();
                    }
                    
                    // Extraer solo el numero del modulo si viene con texto
                    if (modulo && modulo.includes('Modulo')) {
                        modulo = modulo.replace('Modulo', '').trim();
                    }
                    
                    let tiempo = '--';
                    if (kpiValueEl) {
                        const kpiText = kpiValueEl.textContent.trim();
                        const tiempoMatch = kpiText.match(/(\d+)\s*min/);
                        if (tiempoMatch) tiempo = tiempoMatch[1];
                    }
                    
                    let estadoKPI = 'NO';
                    if (kpiStatusEl) {
                        const statusText = kpiStatusEl.textContent.trim();
                        if (statusText.includes('Cumple')) {
                            estadoKPI = 'OK';
                        } else {
                            estadoKPI = 'NO';
                            if (centrosPCC.includes(centro)) centrosData[centro].critico = true;
                        }
                    }
                    
                    if (turno && turnosData.hasOwnProperty(turno)) turnosData[turno]++;
                    
                    // Extraer parametros afectados con valores exactos
                    const parametrosEls = card.querySelectorAll('.param-item');
                    let parametrosDetalle = [];
                    parametrosEls.forEach(paramEl => {
                        const paramName = paramEl.querySelector('.param-name');
                        const paramVal = paramEl.querySelector('.param-val');
                        if (paramName && paramVal) {
                            const nombre = paramName.textContent.trim().replace(/[^a-zA-Z\s]/g, '').trim();
                            const valor = paramVal.textContent.trim();
                            if (nombre && valor) {
                                parametrosDetalle.push(nombre + ': ' + valor);
                            }
                        }
                    });
                    const parametrosTexto = parametrosDetalle.length > 0 ? parametrosDetalle.join(', ') : 'N/A';
                    
                    if (centrosPCC.includes(centro)) {
                        centrosData[centro].count++;
                        if (tipoFalla && tipoFalla !== 'Sin tipo') centrosData[centro].tipos.add(tipoFalla);
                        if (estanque && estanque !== 'N/A' && estanque !== '') centrosData[centro].estanques.add(estanque);
                        if (turno && turno !== 'N/A') centrosData[centro].turnos.add(turno);
                        
                        centrosData[centro].incidencias.push({
                            hora: hora, 
                            modulo: modulo, 
                            estanque: estanque,
                            tipo: tipoFalla, 
                            tiempo: tiempo, 
                            estado: estadoKPI,
                            parametros: parametrosTexto
                        });
                    }
                });
                
                const totalIncidencias = allCards.length;
                let estadoGeneral = 'NORMAL';
                let colorEstado = colorVerde;
                const hayCriticos = Object.values(centrosData).some(c => c.critico);
                
                if (totalIncidencias === 0) {
                    estadoGeneral = 'SIN NOVEDADES';
                } else if (hayCriticos || totalIncidencias > 10) {
                    estadoGeneral = 'ATENCION';
                    colorEstado = colorRojo;
                } else if (totalIncidencias > 5) {
                    estadoGeneral = 'MODERADO';
                    colorEstado = colorAmarillo;
                }
                
                pdf.setFillColor(...colorPrimario);
                pdf.rect(0, 0, pageWidth, 20, 'F');
                pdf.setTextColor(255, 255, 255);
                pdf.setFontSize(16);
                pdf.setFont('helvetica', 'bold');
                pdf.text('REPORTE EJECUTIVO TURNO - MONITOREO PCC', 10, 9);
                pdf.setFontSize(9);
                pdf.setFont('helvetica', 'normal');
                pdf.text('Sistema de Gestion y Monitoreo - CERMAQ CHILE', 10, 15);
                
                const fechaHoy = new Date();
                const fechaStr = fechaHoy.toLocaleDateString('es-CL');
                pdf.setFont('helvetica', 'bold');
                pdf.text('Fecha: ' + fechaStr, pageWidth - 70, 10);
                
                // Determinar turnos activos y sus horarios
                const turnosInfo = {
                    'Mañana': { horario: '08:30 - 17:30', count: turnosData['Mañana'] },
                    'Tarde': { horario: '14:30 - 00:00', count: turnosData['Tarde'] },
                    'Noche': { horario: '00:00 - 09:30', count: turnosData['Noche'] }
                };
                
                const turnosActivos = Object.keys(turnosInfo).filter(t => turnosInfo[t].count > 0);
                
                // Mostrar turno(s) debajo de la fecha
                if (turnosActivos.length > 0) {
                    pdf.setFont('helvetica', 'normal');
                    pdf.setFontSize(6.5);
                    pdf.setTextColor(255, 255, 255);
                    const turnosTexto = turnosActivos.map(t => t.toUpperCase() + ': ' + turnosInfo[t].horario).join(' | ');
                    pdf.text('Turno: ' + turnosTexto, pageWidth - 70, 15);
                }
                
                let y = 25;
                
                // KPIs
                const kpiHeight = 15, kpiWidth = 30, gap = 3;
                
                [[totalIncidencias, 'TOTAL', [240, 240, 240]], 
                 [turnosData['Mañana'], 'MAÑANA', [255, 248, 220]], 
                 [turnosData['Tarde'], 'TARDE', [255, 240, 220]], 
                 [turnosData['Noche'], 'NOCHE', [230, 230, 250]]].forEach((kpi, i) => {
                    pdf.setFillColor(...kpi[2]);
                    pdf.rect(10 + i * (kpiWidth + gap), y, kpiWidth, kpiHeight, 'F');
                    pdf.setDrawColor(200, 200, 200);
                    pdf.rect(10 + i * (kpiWidth + gap), y, kpiWidth, kpiHeight);
                    pdf.setTextColor(0, 0, 0);
                    pdf.setFontSize(8);
                    pdf.setFont('helvetica', 'normal');
                    pdf.text(kpi[1], 25 + i * (kpiWidth + gap), y + 5, { align: 'center' });
                    pdf.setFontSize(14);
                    pdf.setFont('helvetica', 'bold');
                    pdf.text(kpi[0].toString(), 25 + i * (kpiWidth + gap), y + 12, { align: 'center' });
                });
                
                y += kpiHeight + 5;
                pdf.setFontSize(9);
                pdf.setFont('helvetica', 'bold');
                pdf.setTextColor(0, 0, 0);
                pdf.text('RESUMEN POR CENTRO', 10, y);
                y += 3;
                
                const cardWidth = (pageWidth - 20 - gap * 2) / 3;
                const cardHeight = 35;
                
                centrosPCC.forEach((centro, index) => {
                    const data = centrosData[centro];
                    const x = 10 + index * (cardWidth + gap);
                    
                    pdf.setDrawColor(200, 200, 200);
                    pdf.setLineWidth(0.3);
                    pdf.rect(x, y, cardWidth, cardHeight);
                    pdf.setFillColor(...colorPrimario);
                    pdf.rect(x, y, cardWidth, 8, 'F');
                    pdf.setTextColor(255, 255, 255);
                    pdf.setFontSize(9);
                    pdf.setFont('helvetica', 'bold');
                    pdf.text(centro.toUpperCase(), x + cardWidth / 2, y + 5.5, { align: 'center' });
                    
                    let textY = y + 12;
                    pdf.setTextColor(0, 0, 0);
                    pdf.setFontSize(7);
                    
                    if (data.count === 0) {
                        pdf.setFont('helvetica', 'normal');
                        pdf.text('Sin incidencias', x + 2, textY);
                    } else {
                        pdf.setFont('helvetica', 'bold');
                        pdf.text(data.count + ' incidencia(s)', x + 2, textY);
                        textY += 4;
                        
                        if (data.turnos.size > 0) {
                            pdf.setFont('helvetica', 'bold');
                            pdf.text('Turno:', x + 2, textY);
                            pdf.setFont('helvetica', 'normal');
                            pdf.text(Array.from(data.turnos).join(', '), x + 12, textY);
                            textY += 3.5;
                        }
                        
                        if (data.estanques.size > 0) {
                            pdf.setFont('helvetica', 'bold');
                            pdf.text('Estanques:', x + 2, textY);
                            pdf.setFont('helvetica', 'normal');
                            const estanquesArr = Array.from(data.estanques).sort((a, b) => 
                                a.localeCompare(b, undefined, {numeric: true})
                            );
                            const estanquesText = estanquesArr.join(', ');
                            const lines = pdf.splitTextToSize(estanquesText, cardWidth - 22);
                            lines.forEach((line, idx) => {
                                pdf.text(line, x + (idx === 0 ? 20 : 2), textY);
                                if (idx < lines.length - 1) textY += 3;
                            });
                            textY += 4;
                        }
                        
                        if (data.tipos.size > 0) {
                            pdf.setFont('helvetica', 'bold');
                            pdf.setFontSize(6.5);
                            pdf.setTextColor(...colorRojo);
                            pdf.text('Fallas:', x + 2, textY);
                            textY += 3;
                            pdf.setFont('helvetica', 'normal');
                            Array.from(data.tipos).slice(0, 3).forEach(tipo => {
                                pdf.text('- ' + tipo.substring(0, 35), x + 2, textY);
                                textY += 3;
                            });
                            if (data.tipos.size > 3) {
                                pdf.text('y ' + (data.tipos.size - 3) + ' mas', x + 2, textY);
                            }
                        }
                    }
                });
                
                y += cardHeight + 5;
                
                pdf.setDrawColor(200, 200, 200);
                pdf.setLineWidth(0.5);
                pdf.line(10, y, pageWidth - 10, y);
                y += 4;
                
                pdf.setFontSize(9);
                pdf.setFont('helvetica', 'bold');
                pdf.setTextColor(0, 0, 0);
                pdf.text('DETALLE DE INCIDENCIAS', 10, y);
                y += 3;
                
                const colWidths = [10, 28, 15, 40, 70, 50, 20, 15];
                const headers = ['No.', 'Centro', 'Hora', 'Ubicacion', 'Tipo de Incidencia', 'Parametros Afectados', 'Tiempo', 'KPI'];
                
                pdf.setFillColor(...colorPrimario);
                pdf.rect(10, y, pageWidth - 20, 7, 'F');
                pdf.setTextColor(255, 255, 255);
                pdf.setFontSize(7);
                pdf.setFont('helvetica', 'bold');
                
                let xPos = 11;
                headers.forEach((header, i) => {
                    pdf.text(header, xPos, y + 4.5);
                    xPos += colWidths[i];
                });
                y += 7;
                
                pdf.setFont('helvetica', 'normal');
                pdf.setFontSize(6.5);
                pdf.setTextColor(0, 0, 0);
                
                let rowNum = 1;
                centrosPCC.forEach(centro => {
                    centrosData[centro].incidencias.forEach(inc => {
                        if (rowNum > 20) return;
                        
                        const rowHeight = 7;
                        
                        if (rowNum % 2 === 0) {
                            pdf.setFillColor(248, 249, 250);
                            pdf.rect(10, y - 2, pageWidth - 20, rowHeight, 'F');
                        }
                        
                        pdf.setDrawColor(230, 230, 230);
                        pdf.setLineWidth(0.1);
                        pdf.line(10, y + rowHeight - 2, pageWidth - 10, y + rowHeight - 2);
                        
                        xPos = 11;
                        pdf.text(rowNum.toString(), xPos, y + 3);
                        xPos += colWidths[0];
                        pdf.text(centro, xPos, y + 3);
                        xPos += colWidths[1];
                        pdf.text(inc.hora, xPos, y + 3);
                        xPos += colWidths[2];
                        
                        // Construir ubicacion con modulo y estanque
                        let ubicacionParts = [];
                        if (inc.modulo && inc.modulo !== 'N/A' && inc.modulo !== '') {
                            ubicacionParts.push('Modulo ' + inc.modulo);
                        }
                        if (inc.estanque && inc.estanque !== 'N/A' && inc.estanque !== '') {
                            ubicacionParts.push('Estanque ' + inc.estanque);
                        }
                        
                        const ubicacion = ubicacionParts.length > 0 ? ubicacionParts.join(' / ') : 'N/A';
                        
                        const ubicacionLines = pdf.splitTextToSize(ubicacion, colWidths[3] - 2);
                        pdf.text(ubicacionLines[0] || ubicacion, xPos, y + 3);
                        xPos += colWidths[3];
                        
                        const tipoLines = pdf.splitTextToSize(inc.tipo, colWidths[4] - 2);
                        pdf.text(tipoLines[0], xPos, y + 3);
                        xPos += colWidths[4];
                        
                        const paramLines = pdf.splitTextToSize(inc.parametros, colWidths[5] - 2);
                        pdf.text(paramLines[0], xPos, y + 3);
                        xPos += colWidths[5];
                        
                        pdf.text(inc.tiempo + ' min', xPos, y + 3);
                        xPos += colWidths[6];
                        
                        if (inc.estado === 'OK') {
                            pdf.setTextColor(...colorVerde);
                            pdf.text('OK', xPos, y + 3);
                        } else {
                            pdf.setTextColor(...colorRojo);
                            pdf.text('NO', xPos, y + 3);
                        }
                        pdf.setTextColor(0, 0, 0);
                        
                        y += rowHeight;
                        rowNum++;
                    });
                });
                
                if (totalIncidencias === 0) {
                    pdf.setFont('helvetica', 'italic');
                    pdf.setFontSize(8);
                    pdf.setTextColor(...colorGris);
                    pdf.text('No se registraron incidencias en el turno.', 10, y + 5);
                }
                
                const footerY = pageHeight - 8;
                pdf.setDrawColor(200, 200, 200);
                pdf.setLineWidth(0.3);
                pdf.line(10, footerY, pageWidth - 10, footerY);
                pdf.setFontSize(6);
                pdf.setFont('helvetica', 'italic');
                pdf.setTextColor(...colorGris);
                pdf.text('Generado automaticamente por Sistema de Monitoreo CERMAQ', 10, footerY + 4);
                pdf.text('Pagina 1 de 1', pageWidth - 30, footerY + 4);
                
                pdf.save('Reporte_Ejecutivo_Turno_' + fechaStr.replace(/\//g, '-') + '.pdf');
                
                reporteEjecutivoBtn.innerHTML = originalText;
                reporteEjecutivoBtn.disabled = false;
                
            } catch (error) {
                console.error('Error:', error);
                alert('Error al generar el reporte ejecutivo: ' + error.message);
                reporteEjecutivoBtn.innerHTML = originalText;
                reporteEjecutivoBtn.disabled = false;
            }
        });
    }
});
