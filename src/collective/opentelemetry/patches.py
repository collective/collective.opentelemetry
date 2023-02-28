from opentelemetry.trace import get_tracer


def apply_patches():
    tracer = get_tracer(__name__)

    # image scale generation
    from plone.namedfile import scaling
    scaling.scaleImage = tracer.start_as_current_span(
        "scaleImage [plone.namedfile.scaling]"
    )(scaling.scaleImage)

    # catalog indexing
    from Products.ZCatalog.Catalog import Catalog
    orig_catalogObject = Catalog.catalogObject
    orig_search = Catalog.search

    def trace_catalogObject(self, obj, uid, *args, **kw):
        with tracer.start_as_current_span(
            "catalogObject [Products.ZCatalog.Catalog]"
        ) as span:
            span.set_attribute("plone.zcatalog.uid", uid)
            return orig_catalogObject(self, obj, uid, *args, **kw)

    Catalog.catalogObject = trace_catalogObject

    # catalog queries
    def trace_search(self, query, sort_index=None, reverse=False, limit=None, merge=True):
        if isinstance(sort_index, list):
            sort_indexes = [index.id for index in sort_index]
        else:
            sort_indexes = sort_index.id if sort_index is not None else "None"
        with tracer.start_as_current_span(
            "search [Products.ZCatalog.Catalog]"
        ) as span:
            span.set_attribute("plone.zcatalog.query", str(query))
            span.set_attribute("plone.zcatalog.sort_indexes", sort_indexes)
            span.set_attribute("plone.zcatalog.reverse", reverse)
            span.set_attribute("plone.zcatalog.limit", str(limit))
            return orig_search(self, query, sort_index, reverse, limit, merge)

    Catalog.search = trace_search
