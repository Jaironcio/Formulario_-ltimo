// static/js/formulario.js

document.addEventListener('DOMContentLoaded', function () {

    // --- 1. OBTENER LOS ELEMENTOS ---
    const formElement = document.getElementById('incidenciaForm');
    const MODO_EDICION = formElement.dataset.incidenciaId !== '';
    const INCIDENCIA_ID = formElement.dataset.incidenciaId;

    const seccionModulos = document.getElementById('section-modulos-estanques');
    const seccionRiesgos = document.getElementById('section-evaluacion-riesgos');
    const seccionOperario = document.getElementById('section-contacto-operario');
    
    const centroSelect = document.getElementById('centro');
    const moduloSelect = document.getElementById('modulo');
    const estanqueSelect = document.getElementById('estanque');
    const operarioSelect = document.getElementById('operarioContacto');
    
    const tiempoResolucionInput = document.getElementById('tiempoResolucion');
    const submitButton = document.getElementById('submitForm');
    
    const operarioInfoDiv = document.getElementById('info-operario-selected');
    const operarioNombreSpan = document.getElementById('operario-nombre-display');
    const operarioCargoSpan = document.getElementById('operario-cargo-display');
    const operarioTelefonoSpan = document.getElementById('operario-telefono-display');

    
    // --- 2. FUNCIONES AYUDANTES ---

    function rellenarSelectSimple(selectElement, items, prompt) {
        selectElement.innerHTML = ''; 
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = prompt;
        selectElement.appendChild(defaultOption);
        items.forEach(item => {
            const option = document.createElement('option');
            option.value = item; 
            option.textContent = item;
            selectElement.appendChild(option);
        });
    }

    function rellenarSelectOperarios(items) {
        operarioSelect.innerHTML = '';
        operarioSelect.removeAttribute('required');
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Seleccione un operario';
        operarioSelect.appendChild(defaultOption);
        items.forEach(op => {
            const option = document.createElement('option');
            option.value = op.id;
            option.textContent = op.nombre;
            operarioSelect.appendChild(option);
        });
    }

    function validarInputComa(e) {
        let value = e.target.value;
        value = value.replace(/[^0-9,]/g, ''); 
        const firstCommaIndex = value.indexOf(',');
        if (firstCommaIndex !== -1) {
            let partAfterComma = value.substring(firstCommaIndex + 1);
            partAfterComma = partAfterComma.replace(/,/g, '');
            value = value.substring(0, firstCommaIndex + 1) + partAfterComma;
        }
        e.target.value = value;
    }

    function setupParametroCascada(checkId, nivelSelectId, valorInputId) {
        const check = document.getElementById(checkId);
        const card = document.getElementById('card-' + checkId);
        const fieldsDiv = card ? card.querySelector('.parametro-fields') : null;
        const valorInput = valorInputId ? document.getElementById(valorInputId) : null;

        if (!check || !card || !fieldsDiv) {
            console.warn('Faltan elementos para la cascada del parámetro:', checkId);
            return () => {};
        }

        function toggleCheck() {
            if (check.checked) {
                card.classList.add('active');
                fieldsDiv.classList.remove('hidden-input');
            } else {
                card.classList.remove('active');
                fieldsDiv.classList.add('hidden-input');
            }
        }

        check.addEventListener('change', toggleCheck);

        if (valorInput) {
            valorInput.addEventListener('input', validarInputComa);
        }
        
        return toggleCheck;
    }

    // --- 3. LÓGICA DE POBLAR MENÚS ---
    
    function poblarOperarios() {
        const centroId = centroSelect.value;
        if (centroId && window.DATOS_OPERARIOS && window.DATOS_OPERARIOS[centroId]) {
            rellenarSelectOperarios(window.DATOS_OPERARIOS[centroId]);
        } else {
            rellenarSelectOperarios([]);
        }
    }

    function poblarModulos() {
        if (!window.DATOS_MODULOS) { return; }
        const centroId = centroSelect.value;
        if (centroId && window.DATOS_MODULOS[centroId]) {
            const modulosDelCentro = window.DATOS_MODULOS[centroId];
            const nombresDeModulos = Object.keys(modulosDelCentro);
            rellenarSelectSimple(moduloSelect, nombresDeModulos, 'Seleccione un módulo');
        } else {
            rellenarSelectSimple(moduloSelect, [], 'Seleccione un módulo');
        }
        rellenarSelectSimple(estanqueSelect, [], 'Seleccione un estanque');
    }

    function poblarEstanques() {
        if (!window.DATOS_MODULOS) { return; }
        const centroId = centroSelect.value;
        const moduloNombre = moduloSelect.value;
        if (centroId && moduloNombre && window.DATOS_MODULOS[centroId] && window.DATOS_MODULOS[centroId][moduloNombre]) {
            const estanquesDelModulo = window.DATOS_MODULOS[centroId][moduloNombre];
            rellenarSelectSimple(estanqueSelect, estanquesDelModulo, 'Seleccione un estanque');
        } else {
            rellenarSelectSimple(estanqueSelect, [], 'Seleccione un estanque');
        }
    }

    // --- 4. LÓGICA DE EVENTOS ---
    
    centroSelect.addEventListener('change', function() {
        const centroId = centroSelect.value;
        if (centroId) {
            seccionModulos.classList.remove('hidden');
            poblarOperarios();
            poblarModulos();
        } else {
            seccionModulos.classList.add('hidden');
            poblarOperarios();
            poblarModulos();
        }
        if (!MODO_EDICION) {
            seccionRiesgos.classList.add('hidden');
            seccionOperario.classList.add('hidden');
        }
        operarioInfoDiv.classList.add('info-operario-hidden');
    });

    moduloSelect.addEventListener('change', poblarEstanques);

    // --- 5. LÓGICA DE PARÁMETROS ---
    const toggleOxigeno = setupParametroCascada('oxigeno', 'oxigenoNivel', 'valorOxigeno');
    const toggleTemperatura = setupParametroCascada('temperatura', 'temperaturaNivel', 'valorTemperatura');
    const toggleTurbidez = setupParametroCascada('turbidez', 'turbidezNivel', 'valorTurbidez');
    const toggleConductividad = setupParametroCascada('conductividad', 'conductividadNivel');

    // --- 6. LÓGICA DE CASCADA ---
    function mostrarSeccionRiesgos() {
        if (!seccionModulos.classList.contains('hidden')) {
            seccionRiesgos.classList.remove('hidden');
        }
    }

    estanqueSelect.addEventListener('change', function() {
        if (estanqueSelect.value) { mostrarSeccionRiesgos(); } 
        else if (!MODO_EDICION) { seccionRiesgos.classList.add('hidden'); }
    });

    tiempoResolucionInput.addEventListener('input', function() {
        if (tiempoResolucionInput.value) {
            seccionOperario.classList.remove('hidden');
        } else if (!MODO_EDICION) {
            seccionOperario.classList.add('hidden');
        }
    });

    // --- 7. LÓGICA DE MOSTRAR INFO OPERARIO ---
    operarioSelect.addEventListener('change', function() {
        const operarioId = operarioSelect.value;
        const centroId = centroSelect.value;
        if (operarioId && centroId && window.DATOS_OPERARIOS && window.DATOS_OPERARIOS[centroId]) {
            const operarios = window.DATOS_OPERARIOS[centroId];
            const operario = operarios.find(op => op.id == operarioId);
            if (operario) {
                operarioNombreSpan.textContent = operario.nombre;
                operarioCargoSpan.textContent = operario.cargo;
                operarioTelefonoSpan.textContent = operario.telefono;
                operarioInfoDiv.classList.remove('info-operario-hidden');
            }
        } else {
            operarioInfoDiv.classList.add('info-operario-hidden');
        }
    });

    // --- 8. LÓGICA DE MODO EDICIÓN ---
    if (MODO_EDICION && window.INCIDENCIA_A_EDITAR) {
        const data = window.INCIDENCIA_A_EDITAR;
        
        poblarOperarios();
        poblarModulos();
        
        if (data.operario_contacto_id) {
            operarioSelect.value = data.operario_contacto_id;
            operarioSelect.dispatchEvent(new Event('change')); 
        }
        
        if (data.modulo) {
            if (!Array.from(moduloSelect.options).some(opt => opt.value === data.modulo)) {
                const opt = document.createElement('option');
                opt.value = data.modulo;
                opt.textContent = data.modulo;
                moduloSelect.appendChild(opt);
            }
            moduloSelect.value = data.modulo;
            poblarEstanques();
            
            if (data.estanque) {
                if (!Array.from(estanqueSelect.options).some(opt => opt.value === data.estanque)) {
                    const opt = document.createElement('option');
                    opt.value = data.estanque;
                    opt.textContent = data.estanque;
                    estanqueSelect.appendChild(opt);
                }
                estanqueSelect.value = data.estanque;
            }
        }

        data.parametros_afectados.forEach(paramId => {
            if (paramId) {
                const check = document.getElementById(paramId);
                if (check) {
                    check.checked = true;
                }
            }
        });
        
        toggleOxigeno();
        toggleTemperatura();
        toggleTurbidez();
        toggleConductividad();
    }

    // --- 9. LÓGICA DE ENVIAR FORMULARIO ---
    
    function getCsrfToken() {
        return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    }

    submitButton.addEventListener('click', function() {
        
        const csrfToken = getCsrfToken();
        if (!csrfToken) {
            alert('Error de seguridad. (CSRF Token missing)');
            return;
        }

        submitButton.disabled = true;
        submitButton.textContent = 'Guardando...';

        const parametros = Array.from(document.querySelectorAll('input[name="parametros"]:checked'))
                                .map(cb => cb.value)
                                .join(',');

        const riesgoPeces = document.getElementById('riesgoPeces').value === 'si';
        const perdidaEconomica = document.getElementById('perdidaEconomica').value === 'si';
        const riesgoPersonas = document.getElementById('riesgoPersonas').value === 'si';
        
        const data = {
            fecha_hora: document.getElementById('fechaHora').value,
            turno: document.getElementById('turno').value,
            centro: document.getElementById('centro').value || null,
            tipo_incidencia: 'modulos',
            modulo: document.getElementById('modulo').value,
            estanque: document.getElementById('estanque').value,
            parametros_afectados: parametros,
            oxigeno_nivel: document.getElementById('oxigenoNivel').value,
            oxigeno_valor: document.getElementById('valorOxigeno').value,
            temperatura_nivel: document.getElementById('temperaturaNivel').value,
            temperatura_valor: document.getElementById('valorTemperatura').value,
            conductividad_nivel: document.getElementById('conductividadNivel').value,
            turbidez_nivel: document.getElementById('turbidezNivel').value,
            turbidez_valor: document.getElementById('valorTurbidez').value,
            tiempo_resolucion: document.getElementById('tiempoResolucion').value || null,
            riesgo_peces: riesgoPeces,
            perdida_economica: perdidaEconomica,
            riesgo_personas: riesgoPersonas,
            observacion: document.getElementById('observacion').value,
            operario_contacto: document.getElementById('operarioContacto').value || null,
            tipo_incidencia_normalizada: document.getElementById('tipoIncidenciaNormalizada').value,
        };

        let url = '/api/registrar-incidencia/';
        let method = 'POST';
        
        if (MODO_EDICION) {
            url = `/api/incidencia/${INCIDENCIA_ID}/update/`;
            method = 'PUT';
        }

        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) { return response.json(); }
            return response.json().then(errorData => {
                throw new Error(JSON.stringify(errorData));
            });
        })
        .then(result => {
            if (MODO_EDICION) {
                alert('¡Incidencia actualizada con éxito!');
                window.location.href = '/reporte/';
            } else {
                alert('¡Incidencia registrada con éxito!');
                formElement.reset();
                window.location.reload();
            }
        })
        .catch(error => {
            console.error('Error al guardar:', error.message);
            alert('ERROR: No se pudo guardar la incidencia. Revisa la consola (F12).\n' + error.message);
            submitButton.disabled = false;
            submitButton.textContent = MODO_EDICION ? 'Actualizar Incidencia' : 'Registrar Incidencia';
        });

    });

});
