const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

// Creación de un objeto FormData para manejar los datos y el archivo a enviar
let data = new FormData();

// Agregando datos de la persona al objeto FormData
data.append('persona[nombre]', 'Victor');
data.append('persona[año]', '1981');
data.append('persona[mes]', '3');
data.append('persona[dia]', '23');

// Opcionalmente, si quieres añadir más datos de hora, ciudad, y país, puedes hacerlo aquí
// data.append('persona[hora]', '17');
// data.append('persona[minuto]', '0');
// data.append('persona[ciudad]', 'Manizales');
// data.append('persona[pais]', 'CO');

// Agregando el archivo de imagen para la persona
// Asegúrate de que la ruta de la imagen sea correcta
data.append('file', fs.createReadStream('imagen.jpg'));

// Realizando una solicitud POST a la API
// Se envía el objeto FormData que incluye tanto los datos como el archivo
axios.post('http://localhost:5000/perfil', data, {
    headers: data.getHeaders() // Estableciendo los encabezados adecuados para el tipo de datos
})
.then(response => {
    // Manejo exitoso de la respuesta
    console.log('Perfil de la persona:', response.data);
})
.catch(error => {
    // Manejo de errores en caso de que la solicitud falle
    console.error('Hubo un error al obtener el perfil de la persona', error);
});