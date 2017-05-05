from Event import Event
import pygame


class EventHandler(Event):
    """ Pygame Event handler """

    def __init__(self, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)
        #~ pygame.event.set_allowed(None)

    def suscribe(self, event_name, *args, **kwargs):
        pygame.event.set_allowed(event_name)
        return super(EventHandler, self).suscribe(event_name, *args, **kwargs)

    def deplete_suscription(self, name):
        super(EventHandler, self).deplete_suscription(name)
        pygame.event.set_blocked(name)

    def handle(self):
        for event in pygame.event.get():
            self.dispatch(event.type, event)

    def dispatch_event(self, ev):
        self.dispatch(ev.type, ev)

