from datetime import datetime

class Tienda_video_juegos(object):
    """clase que simula ser la tienda de videojuegos"""
    def __init__(self, lista_productos):
        """:param productos: es un diccionario
            {"callofduty":150,
             "fifa2016":100,
             "uncharted4":200,
             "playstation 4":600,
             "xbox360":400,
             "wii":200,}
            """
        self.productos = lista_productos
        self.total_ventas_octubre = 0
        self.total_ventas_noviembre = 0
        self.regalo_tarjetas = None

    def estudio_ventas(self, fecha, total_venta):
        """el estudio de ventas a realizarse solo tomara en cuenta las ventas realizadas en
           el periodo octubre - noviembre de 2015, y en base a eso toma la decision
           :param fecha: en que la compra fue registrada, en esta funcion solo se considerara
           estudiar las ventas del periodo establecido
           :param total_venta: el total de la venta realizada
           """
        _fecha = datetime.strptime(fecha, '%d/%m/%Y')

        fecha_esta_entre_octubre_noviembre_2015 =_fecha.year == 2015 and (_fecha.month in [10, 11])
        mes_es_octubre = _fecha.month == 10
        mes_es_noviembre = _fecha.month == 11
        fin_mes_noviembre = _fecha.day == 30

        if fecha_esta_entre_octubre_noviembre_2015:
            if mes_es_octubre:
                self.total_ventas_octubre += total_venta
            elif mes_es_noviembre:
                self.total_ventas_noviembre += total_venta
                if fin_mes_noviembre: #si es el ultimo dia de noviembre decido si sigo regalando tarjetas
                    self.regalo_tarjetas = self.total_ventas_noviembre > self.total_ventas_octubre

    def ventas_masivas(self,fecha,tipo_pago,varias_compras=None):
        """funcion extra para facilitar el estudio de ventas pudiendo ingresar varias ventas a la vez.
        En esta funcion se asume que los datos seran ingresados correctamente por cuestion de tiempo,
        ya la funcion de ventas normal se encarga de lidiar con los errores.
        :param varias_compras: es una lista de listas:
                            [["item1","item2",...,"itemn"],...,["item1","item2",...,"itemn"]]"""
        venta={}
        for list in varias_compras:
            venta = self.venta(fecha, tipo_pago, list)


    def venta(self, fecha, tipo_pago, lista_compras, tarjeta=None):
        """:param fecha: tiene el formato DD/MM/AAAA
           :param tipo_pago: cadena con el tipo de pago
           :param lista_compras: tiene el formato ["item1", "item2", ...]
        """
        venta = {}
        subtotal = 0
        descuento = 0
        _fecha = datetime.strptime(fecha, '%d/%m/%Y')

        tipo_pago_es_credito_o_contado = tipo_pago in ["credito", "contado"]


        if not tipo_pago_es_credito_o_contado:
            return {"total_a_pagar":0b0} #0b0 es codigo de error
        for item in lista_compras:
            try:
                subtotal += self.productos[item]
            except:
                return {"total_a_pagar":0b0}#0b0 es codigo de error
        numero_obsequios = Obsequio.obtener_obsequio(subtotal)

        if tarjeta:
            if Tarjeta.validarExpiracionTarjeta(tarjeta, _fecha):
                subtotal = tarjeta.usarParaDescuento(subtotal)
            else:
                tarjeta.desactivar()
        elif Tarjeta.cumple_condiciones_para_crear(self,_fecha,subtotal):
            tarjeta= Tarjeta(fecha_expedicion=_fecha)

        descuento = Descuento.total_descuento(subtotal, tipo_pago, fecha)
        self.estudio_ventas(fecha, subtotal)
        venta["total_a_pagar"] = subtotal - descuento
        venta["subtotal"] = subtotal
        venta["obsequios"] = numero_obsequios
        venta["tarjeta"] = tarjeta

        # print ' Subtotal: {}\n Descuento:{}\n Total a Pagar: {}'.format(subtotal, descuento, total)
        return venta

class Tarjeta(object):
    """
    Clase que modela la tarjeta de descuento en la tienda
    """


    def __init__(self, nombres=None, apellidos=None, codigo=None, saldo=20.0, fecha_expedicion=datetime.now()):
        """
        Constructor de la clase que recibe parametros para inicializarla
        :param nombres: Nombres de la persona a quien pertenece la tarjeta
        :param apellidos: Apellidos de la persona a quien pertenece la tarjeta
        :param codigo: Codigo de siete digitos numericos para identificar la tarjeta
        :param saldo_inicial: Saldo inicial que contiene la tarjeta
        """
        self.nombres = nombres
        self.apellidos = apellidos
        self.codigo = codigo
        self.fecha_expedicion = fecha_expedicion
        self.fecha_expiracion = self.fecha_expedicion.replace(year=self.fecha_expedicion.year + 1)
        self.saldo = saldo
        self.activada = True

    @classmethod
    def cumple_condiciones_para_crear(cls, tienda, fecha, subtotal):

        if subtotal > 400 and (fecha.month == 11 or tienda.regalo_tarjetas):
            return True
        else:
            return False

    def desactivar(self):
        self.activada = False

    def usarParaDescuento(self, valor):
        """
        Funcion que debita el valor del saldo que se pase como parametro
        :param valor: valor de la compra hecha
        :return:
        """
        if valor < self.saldo:
            return 0 #retorna 0 por que en este caso el valor de la compra seria menor a $0 y la tarjeta es de un solo uso
        else:
            valor = valor - self.saldo
            return valor

    @classmethod
    def validarExpiracionTarjeta(cls, tarjeta, fecha_hoy=datetime.now()):
        if tarjeta.fecha_expiracion < fecha_hoy:
            return False
        else:
            return True


class Descuento(object):
    """clase encargada de hacer los descuentos para la tienda de videojuegos"""

    @classmethod
    def total_descuento(cls, subtotal, tipo_pago, fecha):
        meses_descuento_5 = ["2", "3", "4", "5", "6", "7",
                             "8", "9", "10"] # meses en donde el descuento podria ser del 5%

        noviembre = "11" # mes en donde el descuento podria ser del 20%
        fecha_descuento_30 = "26/12" #fecha en donde el descuento es del 30%
        fecha_descuento_50 = "06/01" #fecha en donde el descuento es del 50%
        total_dcto = 0
        _fecha = datetime.strptime(fecha, '%d/%m/%Y')
        mes = str(_fecha.month)
        mes_y_dia = str(_fecha.strftime('%d/%m'))

        if mes in meses_descuento_5:
            if tipo_pago == "contado":
                total_dcto += 5
            if subtotal > 350:
                total_dcto += 5
        if mes == noviembre:
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
#     venta = tienda.venta(fecha, tipo_pago, lista_compras)
#     print venta["total_a_pagar"]