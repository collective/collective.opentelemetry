# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE
    PloneSandboxLayer,
)
from plone.testing import z2

import collective.opentelemetry


class CollectiveOpentelemetryLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.opentelemetry)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.opentelemetry:default')


COLLECTIVE_OPENTELEMETRY_FIXTURE = CollectiveOpentelemetryLayer()


COLLECTIVE_OPENTELEMETRY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_OPENTELEMETRY_FIXTURE,),
    name='CollectiveOpentelemetryLayer:IntegrationTesting',
)


COLLECTIVE_OPENTELEMETRY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_OPENTELEMETRY_FIXTURE,),
    name='CollectiveOpentelemetryLayer:FunctionalTesting',
)


COLLECTIVE_OPENTELEMETRY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_OPENTELEMETRY_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveOpentelemetryLayer:AcceptanceTesting',
)
