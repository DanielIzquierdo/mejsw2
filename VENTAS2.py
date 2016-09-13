from datetime import datetime
class Tienda_video_juegos(object):
    """clase que simula ser la tienda de videojuegos"""
    def __init__(self, lista_productos):
        """lista productos es un diccionario:
            {"callofduty":150,
             "fifa2016":100,
             "uncharted4":200,
             "playstation 4":600,
             "xbox360":400,
             "wii":200,}
            """
        self.productos = lista_productos

    def venta(self, fecha, tipo_pago, lista_compras):
        """:param fecha: tiene el formato DD/MM/AAAA
           :param tipo_pago: cadena con el tipo de pago
           :param lista_compras: tiene el formato ["item1", "item2", ...]
        """
        venta = {}
        subtotal = 0
        descuento = 0
        if tipo_pago not in ["credito", "contado"]:
            return 0b0
        for item in lista_compras:
            try:
                subtotal += self.productos[item]
            except:
                return 0b0
        numero_obsequios = Obsequio.obtener_obsequio(subtotal)
        descuento = Descuento.total_descuento(subtotal, tipo_pago, fecha)
        venta["total_a_pagar"] = subtotal - descuento
        venta["subtotal"] = subtotal
        venta["obsequios"] = numero_obsequios
        # print ' Subtotal: {}\n Descuento:{}\n Total a Pagar: {}'.format(subtotal, descuento, total)
        return venta



class Descuento(object):
    """clase encargada de hacer los descuentos para la tienda de videojuegos"""

    @classmethod
    def total_descuento(cls, subtotal, tipo_pago, fecha):
        fecha_descuento_5 = ["2", "3", "4", "5", "6", "7",
                             "8", "9", "10"]

        fecha_descuento_20 = "11"
        fecha_descuento_30 = "26/12"
        fecha_descuento_50 = "06/01"
        total_dcto = 0
        _fecha = datetime.strptime(fecha, '%d/%m/%Y')
        mes = str(_fecha.month)
        mes_y_dia = str(_fecha.strftime('%d/%m'))

        if mes in fecha_descuento_5:
            if tipo_pago == "contado":
                total_dcto += 5
            if subtotal > 350:
                total_dcto += 5
        if mes == fecha_descuento_20:
            total_dcto += 20
        if mes_y_dia == fecha_descuento_30:
            total_dcto += 30
        if mes_y_dia == fecha_descuento_50:
            total_dcto += 50
        total_dcto = (total_dcto/100.0) * subtotal

        return total_dcto

class Obsequio(object):
    """clase que determina la cantidad de obsequios otorgados en cada venta"""
    @classmethod
    def obtener_obsequio(cls, consumo):
        n_obsequio=0
        if consumo > 600:
            n_obsequio = 3
        elif consumo > 500 and consumo <= 600:
            n_obsequio = 2
        elif consumo > 350 and consumo <= 500:
            n_obsequio = 1

        return n_obsequio


# if __name__ == "__main__":
#     lista_productos = {"playstation4":  600,
#                        "xbox360": 400,
#                        "wii": 200,
#                        "callofdutty": 150,
#                        "fifa2016": 100,
#                        "uncharted4":200}
#     tienda = Tienda_video_juegos(lista_productos)
#     fecha="20/05/2015"
#     tipo_pago="credito"
#     lista_compras=["wii","fifa2016"]
#     total_a_pagar = tienda.venta(fecha, tipo_pago, lista_compras)