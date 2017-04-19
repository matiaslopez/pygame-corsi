'''
Created on May 22, 2011

@author: mariano
'''

class Event( object ):
    '''
    Clase que puede guardarse una lista de suscriptores
    '''
    def __init__( self ):
        '''
        Inicia con 0 subscriptores
        '''
        self.suscriptors = {}

    def suscribe( self, name, suscriptor ):
        if name in self.suscriptors:
            self.suscriptors[name].append( suscriptor )
        else:
            self.suscriptors[name] = [suscriptor]
        return Suscription( self, name, suscriptor )

    def dispatch( self, name, obj = None ):
        if obj is None:
            obj = self
        elif id( obj ) == id( self ):
            raise Error()
        if name in self.suscriptors:
            [ suscriptor( obj ) for suscriptor in self.suscriptors[name]]

    def unsuscribe( self, name, suscriptor ):
        self.suscriptors[name].remove( suscriptor )
        if not self.suscriptors[name]:
            self.deplete_suscription(name)

    def deplete_suscription(self, name):
        pass

class Suscription( object ):
    def __init__( self, event, name, suscriptor ):
        self.event = event
        self.name = name
        self.suscriptor = suscriptor

    def unsuscribe( self ):
        self.event.unsuscribe( self.name, self.suscriptor )
