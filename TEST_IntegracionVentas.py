import unittest
from VENTAS2 import Tienda_video_juegos, Obsequio

class Test_system(unittest.TestCase):
    def setUp(self):
        lista_productos = {"playstation4": 600,
                           "xbox360": 400,
                           "wii": 200,
                           "callofdutty": 150,
                           "fifa2016": 100,
                           "uncharted4":200}
        self.tienda = Tienda_video_juegos(lista_productos)

    def test_fecha_descuento_5_porciento_contado(self):
        fecha = "20/05/2015"
        tipo_pago = "contado"
        lista_compras = ["wii", "fifa2016"]
        venta = self.tienda.venta(fecha, tipo_pago, lista_compras)
        self.assertEqual(venta["total_a_pagar"], 285)

    def test_fecha_descuento_5_porciento_monto(self):
        fecha = "20/05/2015"
        tipo_pago = "credito"
        lista_compras = ["wii", "fifa2016", "callofdutty"]
        venta = self.tienda.venta(fecha, tipo_pago, lista_compras)
        self.assertEqual(venta["total_a_pagar"], 427.5)

    def test_fecha_descuento_20_porciento(self):
        fecha = "20/11/2015"
        tipo_pago = "credito"
        lista_compras = ["wii", "fifa2016"]
        venta = self.tienda.venta(fecha, tipo_pago, lista_compras)
        self.assertEqual(venta["total_a_pagar"], 240)

    def test_fecha_descuento_30_porciento(self):
        fecha = "26/12/2015"
        tipo_pago = "credito"
        lista_compras = ["wii", "fifa2016"]
        venta = self.tienda.venta(fecha, tipo_pago, lista_compras)
        self.assertEqual(venta["total_a_pagar"], 210)

    def test_fecha_sin_descuento_diciembre(self):
        fecha = "16/12/2015"
        tipo_pago = "credito"
        lista_compras = ["wii", "fifa2016"]
        venta = self.tienda.venta(fecha, tipo_pago, lista_compras)
        self.assertEqual(venta["total_a_pagar"], 300)

    def test_fecha_descuento_50_porciento(self):
        fecha = "06/01/2015"
        tipo_pago = "credito"
        lista_compras = ["wii", "fifa2016"]
        venta = self.tienda.venta(fecha, tipo_pago, lista_compras)
        self.assertEqual(venta["total_a_pagar"], 150)

    def test_fecha_sin_descuento_enero(self):
        fecha = "16/01/2015"
        tipo_pago = "credito"
        lista_compras = ["wii", "fifa2016"]
        venta = self.tienda.venta(fecha, tipo_pago, lista_compras)
        self.assertEqual(venta["total_a_pagar"], 300)

    def test_elemento_compra_invalido(self):
        fecha = "16/01/2015"
        tipo_pago = "credito"
        lista_compras = ["wii", "caramelo"]
        venta = self.tienda.venta(fecha, tipo_pago, lista_compras)
        self.assertEqual(venta["total_a_pagar"], 0b0)

    def test_tipo_pago_invalido(self):
        fecha = "16/01/2015"
        tipo_pago = "fiado"
        lista_compras = ["wii", "fifa2016"]
        venta = self.tienda.venta(fecha, tipo_pago, lista_compras)
        self.assertEqual(venta["total_a_pagar"], 0b0)

    #### test unitarios Obsequio
    def test_compra_sin_obsequio(self):
        consumo = 350
        numero_obsequios = Obsequio.obtener_obsequio(consumo)
        self.assertEqual(numero_obsequios,0)

    def test_compra_1_obsequio(self):
        consumo = 500
        numero_obsequios = Obsequio.obtener_obsequio(consumo)
        self.assertEqual(numero_obsequios, 1)

    def test_compra_2_obsequios(self):
        consumo = 600
        numero_obsequios = Obsequio.obtener_obsequio(consumo)
        self.assertEqual(numero_obsequios, 2)

    def test_compra_3_obsequios(self):
        consumo = 601
        numero_obsequios = Obsequio.obtener_obsequio(consumo)
        self.assertEqual(numero_obsequios, 3)

    #integracion venta - Obsequio

    def test_0_obsequios_compra(self):
        fecha = "16/01/2015"
        tipo_pago = "credito"
        lista_compras = ["wii", "fifa2016"]
        venta = self.tienda.venta(fecha, tipo_pago, lista_compras)
        self.assertEqual(venta["obsequios"], 0)

    def test_1_obsequio_compra(self):
        fecha = "16/01/2015"
        tipo_pago = "credito"
        lista_compras = ["wii", "fifa2016", "callofdutty"]
        venta = self.tienda.venta(fecha, tipo_pago, lista_compras)
        self.assertEqual(venta["obsequios"], 1)

    def test_2_obsequios_compra(self):
        fecha = "16/01/2015"
        tipo_pago = "credito"
        lista_compras = ["callofdutty","xbox360"]
        venta = self.tienda.venta(fecha, tipo_pago, lista_compras)
        self.assertEqual(venta["obsequios"], 2)

    def test_3_obsequios_compra(self):
        fecha = "16/01/2015"
        tipo_pago = "credito"
        lista_compras = ["callofdutty", "playstation4"]
        venta = self.tienda.venta(fecha, tipo_pago, lista_compras)
        self.assertEqual(venta["obsequios"], 3)

if __name__ == '__main__':
	unittest.main()