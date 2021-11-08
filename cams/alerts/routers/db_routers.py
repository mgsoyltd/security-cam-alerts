
class AlertsRouter:

    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'alerts'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to alerts.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'alerts'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to alerts.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'alerts'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'alerts' database.
        """
        if app_label in self.route_app_labels:
            return db == 'alerts'
        return None