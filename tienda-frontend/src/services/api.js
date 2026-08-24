export const getProductos = async () => {
    const response = await fetch('/api/productos');
    if (!response.ok) {
        throw new Error('Error al comunicarse con la API');
    }
    return await response.json();
};

export const solicitarArrepentimiento = async (email, codigoCompra, detalle = '') => {
    const response = await fetch('/api/arrepentimiento', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email,
            codigo_compra: codigoCompra,
            detalle,
        }),
    });
    if (!response.ok) {
        throw new Error('Error al procesar la revocación de la compra');
    }
    return await response.json();
};