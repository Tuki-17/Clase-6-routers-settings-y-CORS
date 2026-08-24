import React from 'react';

export function ProductCard({ producto, onAddToCart }) {
    // Clasificar si es alimento fresco o tiene garantía
    const esAlimentoFresco = producto.garantia_meses === 0;

    // Advertencia de trampantojo para cumplir con Deber de Información (Art. 4)
    const obtenerAdvertencia = (nombre) => {
        if (nombre.toLowerCase().includes('hamburguesa')) {
            return 'Diseño dulce que imita una hamburguesa. Elaborado a base de banana y avena.';
        }
        if (nombre.toLowerCase().includes('esponja')) {
            return 'Diseño dulce que imita una esponja de cocina. Elaborado con bizcochuelo cítrico.';
        }
        if (nombre.toLowerCase().includes('huevo')) {
            return 'Diseño dulce que imita un huevo frito. Elaborado con gelatina y crema.';
        }
        if (nombre.toLowerCase().includes('vela')) {
            return 'Diseño dulce que imita una vela aromática. Elaborado con chocolate blanco y negro.';
        }
        if (nombre.toLowerCase().includes('tomate')) {
            return 'Diseño dulce que imita un tomate. Elaborado como alfajor de maicena premium.';
        }
        return 'Producto de pastelería creativa (trampantojo). 100% comestible y dulce.';
    };

    return (
        <div className="product-card">
            <div>
                <span className={`card-tag ${esAlimentoFresco ? 'tag-fresh' : ''}`}>
                    {esAlimentoFresco ? '🍰 Fresco / Dulce' : `🛡️ Garantía: ${producto.garantia_meses} m.`}
                </span>
                
                <h3 className="card-title">{producto.nombre}</h3>
                
                {/* Deber de información (Art. 4 y 9 Ley 24.240) */}
                <div className="deber-informacion">
                    <span>⚠️</span>
                    <span>{obtenerAdvertencia(producto.nombre)}</span>
                </div>
            </div>

            <div>
                {/* Desglose de precios y costos financieros */}
                <div className="price-block">
                    <p className="cash-price">
                        ${producto.precio_final.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </p>
                    <p className="installments-info">
                        {producto.cuotas_cantidad} cuotas de ${producto.cuotas_valor.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </p>
                    <div className="legal-details">
                        Precio Total Financiado (PTF): ${producto.precio_final.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}<br />
                        Costo Financiero Total (CFT): <strong>0,00%</strong> | TNA: 0,00% | TEA: 0,00%
                    </div>
                </div>

                {/* Stock sujeto a disponibilidad (Art. 7) */}
                <div className="stock-info">
                    <span>Stock: {producto.stock} u.</span>
                    <span style={{ color: 'var(--text-muted)' }}>Sujeto a disponibilidad</span>
                </div>

                <button 
                    className="btn btn-primary" 
                    style={{ width: '100%', justifyContent: 'center' }}
                    onClick={() => onAddToCart(producto)}
                    disabled={producto.stock <= 0}
                >
                    {producto.stock > 0 ? '🛒 Agregar al Carrito' : 'Sin Stock'}
                </button>
            </div>
        </div>
    );
}