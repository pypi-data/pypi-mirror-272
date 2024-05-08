# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from zeep import Client, Settings
from requests import Session
from zeep.transports import Transport
import logging
import os

__all__ = ["ClientOMIE"]


class CustomTransport(Transport):

    def post_xml(self, address, envelope, headers):
        """
        Modifica la dirección aquí antes de enviar la petición
        """
        new_address = address.replace("www.mercado.omie.es", "www.pruebas.omie.es")
        return super(CustomTransport, self).post_xml(new_address, envelope, headers)

    def post(self, address, message, headers):
        """
        Modifica la dirección aquí para peticiones POST si es necesario
        """
        new_address = address.replace("www.mercado.omie.es", "www.pruebas.omie.es")
        return super(CustomTransport, self).post(new_address, message, headers)

    def get(self, address, params, headers):
        """
        Modifica la dirección aquí para peticiones GET si es necesario
        """
        new_address = address.replace("www.mercado.omie.es", "www.pruebas.omie.es")
        return super(CustomTransport, self).get(new_address, params, headers)


CustomTransport()


class ClientOMIE(Client, Settings):

    @staticmethod
    def _validate_certs(crt_path, crt_key):
        """
        Método de validación de certificado y clave de OMIE
        :param crt_path: ruta del certificado de OMIE para poder hacer consultas
        :param crt_key: ruta del fichero clave de OMIE para poder hacer consultas
        :return: Retorna las rutas del certificado y de la clave de OMIE. Si las rutas están vacías salta una excepción
        """
        import os
        crt_path = crt_path or os.environ.get('OMIE_CERT')
        crt_key = crt_key or os.environ.get('OMIE_KEY')

        if not crt_path or not crt_key:
            raise EnvironmentError("OMIE_CERT and OMIE_KEY env variables are required")
        return crt_path, crt_key

    def __init__(self, crt_path=None, crt_key=None):
        crt_path, crt_key = self._validate_certs(crt_path, crt_key)
        self.settings = Settings(strict=False, xml_huge_tree=True)
        logging.basicConfig(level=logging.INFO)
        session = Session()
        # TODO set to true before push to pypi
        session.verify = False

        session.cert = (crt_path, crt_key)
        self.pruebasTransport = CustomTransport(session=session)

        # Set services path
        self.path = os.path.dirname(__file__) + '/services'

    def get_cliente(self, servicio):
        """
        - Nos devuelve el cliente del fichero deseado pasándole el nombre de la llamada del servicio
        :param servicio: String con el nombre de la llamada del servicio
        :return: - Nos devuelve el cliente del fichero deseado pasándole el nombre de la llamada del servicio
                 - Si no existe el servicio, saltará una excepción
        """
        servicios = {
            'ServicioConsultaMercados': self.path + '/ServicioConsultaMercados.wsdl',
            'ServicioConsultaMensajesActivos': self.path + '/ServicioConsultaMercados.wsdl',
            'ServicioConsultaDirectorioConsultas': self.path + '/ServiciosConsultas.wsdl',
            'ServicioConsultaConfiguracionConsulta': self.path + '/ServiciosConsultas.wsdl',
            'ServicioEjecucionConsultaEncolumnada': self.path + '/ServiciosConsultas.wsdl',
            'ServicioEjecucionConsultaAnexo': self.path + '/ServiciosConsultas.wsdl',
            'ServicioEjecucionConsultaPrograma': self.path + '/ServiciosConsultas.wsdl',
            'ServicioConsultaTiposFicheros': self.path + '/ServiciosConsultasAuxiliares.wsdl',
            'ServicioConsultaNuevosFicheros': self.path + '/ServiciosConsultasAuxiliares.wsdl',
            'ServicioConsultaNuevosFicherosLiq': self.path + '/ServiciosConsultasAuxiliares.wsdl',
            'ServicioConsultaNuevosFicherosFact': self.path + '/ServiciosConsultasAuxiliares.wsdl',
            'ServicioConsultaIdiomas': self.path + '/ServiciosIdiomas.wsdl',
            'ServicioSeleccionIdioma': self.path + '/ServiciosIdiomas.wsdl',
            'ServicioConsultaCertificado': self.path + '/ServiciosConsultaDocumento.wsdl',
            'ServicioConsultaFactura': self.path + '/ServiciosConsultaDocumento.wsdl',
        }

        url = servicios.get(servicio, self.path + '/{}.wsdl'.format(servicio))
        try:
            cliente = Client(url, settings=self.settings, transport=self.pruebasTransport)
            return getattr(cliente.service, servicio)
        except Exception as e:
            raise Exception("Error al obtener el servicio '{}'. ERROR: {}".format(servicio, e))

    def __getattribute__(self, servicio):
        """
        - Se obtienen los datos de la llamada al método 'servicio'
        [Si servicio = ServicioConsultaDatosUsuario, se obtienen
         los datos para la llamada: cliente.service.ServicioConsultaDatosUsuario()]

        :param servicio: String con el nombre del servicio que deseamos llamar.
        :return: - Nos devolverá los datos del servicio deseado.
        """
        try:
            res = object.__getattribute__(self, servicio)
            return res
        except AttributeError:
            try:
                resultado = self.get_cliente(servicio)
                return resultado
            except Exception as e:
                raise e

    def __repr__(self):
        return 'ClientOMIE: {}'.format(id(self))


if __name__ == "__main__":
    client = ClientOMIE(
        crt_path='/home/aorellana/proyectos/OMIE/omie-base/omie/data/omie.cert',
        crt_key='/home/aorellana/proyectos/OMIE/omie-base/omie/data/omie.key'
    )

    result = client.ServicioConsultaFactura()
    print(result)
