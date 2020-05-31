//Definit per l'equip A1

var mongoose = require('mongoose'),
    Schema   = mongoose.Schema;

var cocheSchema = new Schema({
  id_coche: String, //identificador del coche
  puntOrigencotxe: String, //node inicial on es localitza el cotxe, pàrking
  puntOrigen: String, //node on es troba el client
  puntDesti: String, //node on es dirigeix el client
  puntActual: String, //node actual
  estado: String, //ocupado, cargando, disponible, buscando
  id_pasajero: String //identificación del pasajero
},{collection:'coches'});
//});

module.exports = mongoose.model('coche', cocheSchema);
